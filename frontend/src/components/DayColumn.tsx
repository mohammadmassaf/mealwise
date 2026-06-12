import MealCard from "./MealCard";
import type { DayPlan } from "../types";

const MEAL_LABELS = ["Breakfast", "Lunch", "Dinner", "Snack"];

interface Props {
  dayPlan: DayPlan;
  dayIndex: number;
  onRegenerate: (dayIndex: number) => void;
  regenerating: boolean;
}

export default function DayColumn({ dayPlan, dayIndex, onRegenerate, regenerating }: Props) {
  const totalCalories = dayPlan.meals.reduce((sum, m) => sum + m.calories, 0);

  return (
    <div className="day-column">
      <div className="day-header">
        <h2 className="day-name">{dayPlan.day}</h2>
        <span className="day-calories">{Math.round(totalCalories)} kcal total</span>
        <button
          className="btn btn-outline btn-sm"
          onClick={() => onRegenerate(dayIndex)}
          disabled={regenerating}
        >
          {regenerating ? "Regenerating…" : "Regenerate day"}
        </button>
      </div>
      <div className="meal-list">
        {dayPlan.meals.map((meal, i) => (
          <MealCard key={i} meal={meal} label={MEAL_LABELS[i] ?? `Meal ${i + 1}`} />
        ))}
      </div>
    </div>
  );
}
