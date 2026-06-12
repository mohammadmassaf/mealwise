import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createMealPlan } from "../api/meals";
import type { PreferenceRequest } from "../types";

const DIET_OPTIONS = ["None", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean"];
const CUISINE_OPTIONS = ["Italian", "Asian", "Mexican", "Mediterranean", "American", "Indian", "Middle Eastern"];

export default function PlannerPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [days, setDays] = useState(7);
  const [prepTime, setPrepTime] = useState(45);
  const [calories, setCalories] = useState(2300);
  const [diet, setDiet] = useState("None");
  const [allergies, setAllergies] = useState("");
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [startDate, setStartDate] = useState("");
  const [notes, setNotes] = useState("");

  function toggleCuisine(c: string) {
    setSelectedCuisines((prev) =>
      prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const prefs: PreferenceRequest = {
      days,
      prep_time: prepTime,
      calories_per_day: calories,
      diet: diet === "None" ? undefined : diet,
      allergies: allergies ? allergies.split(",").map((s) => s.trim()) : undefined,
      cuisines: selectedCuisines.length ? selectedCuisines : undefined,
      start_date: startDate || undefined,
      notes: notes.trim() || undefined,
    };
    try {
      const result = await createMealPlan(prefs);
      navigate(`/plan/${result.id}`);
    } catch {
      setError("Failed to generate meal plan. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="planner-page">
      <div className="planner-header">
        <h1>Build your meal plan</h1>
        <p>Tell us your preferences and we'll create a personalized plan using AI.</p>
      </div>

      <form onSubmit={handleSubmit} className="planner-form">
        <div className="form-grid">
          <div className="form-group">
            <label>Number of days</label>
            <div className="range-row">
              <input type="range" min={1} max={14} value={days} onChange={(e) => setDays(+e.target.value)} />
              <span className="range-value">{days} days</span>
            </div>
          </div>

          <div className="form-group">
            <label>Max prep time</label>
            <div className="range-row">
              <input type="range" min={10} max={120} step={5} value={prepTime} onChange={(e) => setPrepTime(+e.target.value)} />
              <span className="range-value">{prepTime} min</span>
            </div>
          </div>

          <div className="form-group">
            <label>Daily calorie target</label>
            <div className="range-row">
              <input type="range" min={1200} max={4000} step={100} value={calories} onChange={(e) => setCalories(+e.target.value)} />
              <span className="range-value">{calories} kcal</span>
            </div>
          </div>

          <div className="form-group">
            <label>Start date <span className="optional">(optional)</span></label>
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </div>

          <div className="form-group">
            <label>Diet type</label>
            <select value={diet} onChange={(e) => setDiet(e.target.value)}>
              {DIET_OPTIONS.map((d) => <option key={d}>{d}</option>)}
            </select>
          </div>

          <div className="form-group">
            <label>Allergies <span className="optional">(comma-separated)</span></label>
            <input
              type="text"
              placeholder="e.g. peanuts, shellfish"
              value={allergies}
              onChange={(e) => setAllergies(e.target.value)}
            />
          </div>
        </div>

        <div className="form-group">
          <label>
            Special notes <span className="optional">(optional)</span>
          </label>
          <textarea
            className="notes-input"
            rows={3}
            placeholder="e.g. I prefer high-protein breakfasts, avoid spicy food at dinner, use seasonal vegetables…"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Preferred cuisines</label>
          <div className="cuisine-chips">
            {CUISINE_OPTIONS.map((c) => (
              <button
                key={c}
                type="button"
                className={`chip ${selectedCuisines.includes(c) ? "chip-active" : ""}`}
                onClick={() => toggleCuisine(c)}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="form-error">{error}</p>}

        <button type="submit" className="btn btn-primary btn-large" disabled={loading}>
          {loading ? (
            <span className="btn-loading">
              <span className="spinner" /> Generating your plan…
            </span>
          ) : (
            "Generate meal plan"
          )}
        </button>
      </form>
    </div>
  );
}
