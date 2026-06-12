# MealWise

An AI-powered meal planning web app. Give it your dietary preferences, calorie goals, and any special instructions — it generates a personalized multi-day meal plan with recipes, ingredient lists, and USDA-verified nutrition data. You can regenerate individual days without touching the rest of the plan.

## Features

- AI-generated meal plans (breakfast, lunch, dinner, snack per day)
- Calorie counts verified against the USDA FDC food database
- Supports diet types, allergies, cuisine preferences, prep time limits, and free-text notes
- Regenerate any single day independently
- View all previously generated plans
- JWT authentication

## Tech stack

### Backend
- **FastAPI** — REST API
- **SQLAlchemy** + **Alembic** — ORM and database migrations
- **PostgreSQL** — database
- **Google Gemini 2.5 Flash** — meal plan generation with function calling
- **USDA FDC API** — nutrition data lookup

### Frontend
- **React 19** + **TypeScript** + **Vite**
- **React Router** — client-side routing
- **TanStack Query** — server state and caching
- **Axios** — HTTP client

## Project structure

```
mealwise/
├── backend/
│   └── app/
│       ├── core/          # Config, database session
│       ├── models/        # SQLAlchemy ORM models + Pydantic schemas
│       ├── routers/       # API route handlers (auth, meals)
│       └── services/      # Business logic (planner, parser, repository, prompts, nutrition)
├── alembic/               # Database migrations
└── frontend/
    └── src/
        ├── api/           # Axios API calls
        ├── components/    # Navbar, MealCard, DayColumn, ProtectedRoute
        ├── context/       # Auth context
        ├── pages/         # Landing, Login, Register, Planner, MealPlan, MyPlans
        └── types/         # Shared TypeScript types
```

## Getting started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL

### Environment variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@localhost/mealwise
SECRET_key=your_jwt_secret
USDA_KEY=your_usda_fdc_api_key
```

### Backend

```bash
# Create and activate a virtual environment (WSL/Linux)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## API overview

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | — | Create account |
| POST | `/auth/login` | — | Log in, receive JWT |
| GET | `/meals/my-plans` | JWT | List all your meal plans |
| POST | `/meals/preferences` | JWT | Generate a new meal plan |
| GET | `/meals/meal-plan/{id}` | JWT | Retrieve a meal plan |
| POST | `/meals/meal-plan/{id}/regenerate-day` | JWT | Regenerate a single day |
