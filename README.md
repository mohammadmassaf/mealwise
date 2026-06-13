# MealWise

AI-powered meal planner that generates personalized multi-day meal plans with recipes, ingredient lists, and USDA-verified nutrition data.

Built as a learning project to explore FastAPI, LLMs with function calling, and SQLAlchemy — the backend calls Google Gemini to produce structured meal plans, cross-checks calorie counts against the USDA FDC food database, and stores everything in PostgreSQL so you can revisit past plans.

## Tech stack

**Backend** — FastAPI · SQLAlchemy · PostgreSQL · Google Gemini 2.5 Flash · USDA FDC API · PyJWT  
**Frontend** — React 19 · TypeScript · Vite · React Router · TanStack Query · Axios

## Getting started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL running locally
- [Google Gemini API key](https://aistudio.google.com/apikey) (free tier: 20 req/day)
- [USDA FDC API key](https://fdc.nal.usda.gov/api-guide.html) (free, instant)

### 1. Clone and configure

```bash
git clone https://github.com/mohammadmassaf/mealwise.git
cd mealwise
```

Create `.env` in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@localhost/mealwise
SECRET_key=your_jwt_secret          # any long random string
USDA_KEY=your_usda_fdc_api_key
CORS_ORIGINS=http://localhost:5173
```

### 2. Backend

```bash
# From project root (Linux/WSL)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd backend
uvicorn app.main:app --reload
# Tables are created automatically on first start
```

API runs at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
cp .env.example .env          # default points to http://localhost:8000
npm install
npm run dev
```

App runs at `http://localhost:5173`

## Usage example

**Register and generate a 3-day plan:**

```bash
# Register
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "secret123"}'

# Log in — grab the token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "secret123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Generate a meal plan
curl -s -X POST http://localhost:8000/meals/preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "num_days": 3,
    "calorie_goal": 2000,
    "diet_preference": "high protein",
    "cuisine": ["Mediterranean", "Japanese"],
    "allergies": ["nuts"],
    "max_prep_time": 30,
    "notes": "make breakfasts quick, under 10 minutes"
  }'
```

Response (truncated):

```json
{
  "plan_id": 1,
  "start_date": "2026-06-13",
  "days": [
    {
      "day": "Day 1",
      "meals": [
        {
          "name": "Greek Yogurt with Berries",
          "calories": 320,
          "time_to_cook": 5,
          "recipe": "Mix 200g Greek yogurt with fresh berries and a drizzle of honey.",
          "ingredients": ["Greek yogurt", "mixed berries", "honey"]
        }
      ]
    }
  ]
}
```

## API reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | — | Create account |
| POST | `/auth/login` | — | Log in, receive JWT |
| GET | `/meals/my-plans` | JWT | List all your meal plans |
| POST | `/meals/preferences` | JWT | Generate a new meal plan |
| GET | `/meals/meal-plan/{id}` | JWT | Retrieve a saved meal plan |
| POST | `/meals/meal-plan/{id}/regenerate-day` | JWT | Regenerate one day |

## Deployment

- **Backend** — Render (free tier). Uses the `render.yaml` blueprint in this repo.
- **Frontend** — Vercel. Set `VITE_API_URL` to your Render service URL and `CORS_ORIGINS` in Render to your Vercel URL.

Live demo: [mealwise-iota.vercel.app](https://mealwise-iota.vercel.app)

## Project structure

```
mealwise/
├── backend/
│   └── app/
│       ├── core/        # Config, database session
│       ├── models/      # SQLAlchemy ORM models + Pydantic schemas
│       ├── routers/     # Route handlers (auth, meals)
│       └── services/    # Planner, parser, repository, prompts, nutrition
└── frontend/
    └── src/
        ├── api/         # Axios client + API calls
        ├── components/  # Navbar, MealCard, DayColumn, ProtectedRoute
        ├── context/     # Auth context (JWT storage)
        ├── pages/       # Landing, Login, Register, Planner, MealPlan, MyPlans
        └── types/       # Shared TypeScript types
```
