from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.meal import RegisterRequest , LoginRequest 
from app.models.db_models import Users 
from pwdlib import PasswordHash

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(request: RegisterRequest ,db: Session = Depends(get_db)):
    # 1. Accept email + password from request body
    email = request.email
    password = request.password
    # 2. Check if email already exists in DB
    existing = db.query(Users).filter(Users.email == email).first()
    if existing: raise  HTTPException(status_code=400, detail="Email already registered")
    # 3. Hash the password
    password_hash = PasswordHash.recommended()
    hashed = password_hash.hash(password)
    # 4. Save new user to DB
    user = Users(email = email, password = hashed )
    db.add(user)
    db.commit()
    db.refresh(user)
    # 5. Return success
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(db: Session = Depends(get_db)):
    # 1. Accept email + password
    # 2. Look up user by email
    # 3. Verify password against hash
    # 4. Generate and return JWT token
    pass