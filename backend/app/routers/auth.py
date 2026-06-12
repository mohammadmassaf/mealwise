from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.meal import RegisterRequest, LoginRequest
from app.models.db_models import Users
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Module-level singleton — no need to reconstruct on every request
password_hash = PasswordHash.recommended()

TOKEN_EXPIRY_DAYS = 7


@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = password_hash.hash(request.password)
    user = Users(email=request.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.email == request.email).first()
    # Use a generic message so attackers can't enumerate valid emails
    if not existing or not password_hash.verify(request.password, existing.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    exp = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS)
    token = jwt.encode({"sub": str(existing.user_id), "exp": exp}, settings.secret_key, algorithm="HS256")
    return {"access_token": token}



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Users:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError :
        raise HTTPException(status_code=401, detail="Invalid token") 
    user = db.get(Users , int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    return user
    