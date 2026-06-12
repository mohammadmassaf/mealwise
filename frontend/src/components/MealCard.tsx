import { useState } from "react";
import { Clock, Flame, ChevronDown, ChevronUp, RefreshCw } from "lucide-react";
import type { Meal } from "../types";

interface Props {
  meal: Meal;
  label: string;
  onRegenerate?: () => void;
  regenerating?: boolean;
}

export default function MealCard({ meal, label, onRegenerate, regenerating }: Props) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="meal-card">
      <div className="meal-card-header">
        <span className="meal-label">{label}</span>
        {onRegenerate && (
          <button
            className="btn-icon"
            onClick={onRegenerate}
            disabled={regenerating}
            title="Regenerate this day"
          >
            <RefreshCw size={15} className={regenerating ? "spinning" : ""} />
          </button>
        )}
      </div>
      <h3 className="meal-name">{meal.name}</h3>
      <div className="meal-meta">
        <span><Flame size={14} /> {meal.calories} kcal</span>
        <span><Clock size={14} /> {meal.time_to_cook} min</span>
      </div>

      <div className="meal-ingredients">
        {meal.ing.map((ing, i) => (
          <span key={i} className="ingredient-tag">{ing.name}</span>
        ))}
      </div>

      <button className="recipe-toggle" onClick={() => setExpanded(!expanded)}>
        Recipe {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>

      {expanded && (
        <div className="recipe-text">
          {meal.recipe.split(/step \d+:/i).filter(Boolean).map((step, i) => (
            <p key={i}><strong>Step {i + 1}:</strong> {step.trim()}</p>
          ))}
        </div>
      )}
    </div>
  );
}
