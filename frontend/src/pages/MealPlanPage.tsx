import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getMealPlan, regenerateDay } from "../api/meals";
import DayColumn from "../components/DayColumn";
import type { PreferenceRequest } from "../types";

export default function MealPlanPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [regeneratingDay, setRegeneratingDay] = useState<number | null>(null);

  const { data: plan, isLoading, error } = useQuery({
    queryKey: ["plan", id],
    queryFn: () => getMealPlan(id!),
    enabled: !!id,
  });

  const regenMutation = useMutation({
    mutationFn: ({ day, prefs }: { day: number; prefs: PreferenceRequest }) =>
      regenerateDay(id!, day, prefs),
    onSuccess: (updated) => {
      queryClient.setQueryData(["plan", id], updated);
      setRegeneratingDay(null);
    },
    onError: () => setRegeneratingDay(null),
  });

  function handleRegenerate(dayIndex: number) {
    if (!plan) return;
    setRegeneratingDay(dayIndex);
    const prefs: PreferenceRequest = { days: plan.num_days };
    regenMutation.mutate({ day: dayIndex + 1, prefs });
  }

  if (isLoading) {
    return (
      <div className="plan-loading">
        <div className="spinner large" />
        <p>Loading your meal plan…</p>
      </div>
    );
  }

  if (error || !plan) {
    return (
      <div className="plan-error">
        <p>Could not load this meal plan.</p>
        <button className="btn btn-primary" onClick={() => navigate("/planner")}>
          Create new plan
        </button>
      </div>
    );
  }

  return (
    <div className="plan-page">
      <div className="plan-header">
        <div>
          <h1>Your meal plan</h1>
          {plan.start_date && (
            <p className="plan-date">Starting {new Date(plan.start_date).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}</p>
          )}
        </div>
        <button className="btn btn-outline" onClick={() => navigate("/planner")}>
          New plan
        </button>
      </div>

      <div className="days-grid">
        {plan.days.map((day, i) => (
          <DayColumn
            key={i}
            dayPlan={day}
            dayIndex={i}
            onRegenerate={handleRegenerate}
            regenerating={regeneratingDay === i}
          />
        ))}
      </div>
    </div>
  );
}
