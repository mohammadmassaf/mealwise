import client from "./client";
import type { MealPlan, PlanResponse, PlanSummary, PreferenceRequest } from "../types";

export async function getMyPlans(): Promise<PlanSummary[]> {
  const { data } = await client.get("/meals/my-plans");
  return data;
}

export async function createMealPlan(prefs: PreferenceRequest): Promise<PlanResponse> {
  const { data } = await client.post("/meals/preferences", prefs);
  return data;
}

export async function getMealPlan(id: string): Promise<MealPlan> {
  const { data } = await client.get(`/meals/meal-plan/${id}`);
  return data;
}

export async function regenerateDay(
  planId: string,
  day: number,
  preferences: PreferenceRequest
): Promise<MealPlan> {
  const { data } = await client.post(`/meals/meal-plan/${planId}/regenerate-day`, {
    day,
    preferences,
  });
  return data;
}
