export interface Ingredient {
  name: string;
}

export interface Meal {
  name: string;
  calories: number;
  time_to_cook: number;
  recipe: string;
  ing: Ingredient[];
}

export interface DayPlan {
  day: string;
  meals: Meal[];
}

export interface MealPlan {
  num_days: number;
  start_date: string | null;
  days: DayPlan[];
}

export interface PlanResponse {
  id: string;
  plan: MealPlan;
}

export interface PlanSummary {
  id: number;
  num_days: number;
  start_date: string | null;
}

export interface PreferenceRequest {
  days: number;
  prep_time?: number;
  allergies?: string[];
  cuisines?: string[];
  diet?: string;
  calories_per_day?: number;
  start_date?: string;
  notes?: string;
}
