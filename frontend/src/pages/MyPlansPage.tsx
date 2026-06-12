import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getMyPlans } from "../api/meals";
import { CalendarDays, ChevronRight, PlusCircle } from "lucide-react";

export default function MyPlansPage() {
  const navigate = useNavigate();

  const { data: plans, isLoading, error } = useQuery({
    queryKey: ["my-plans"],
    queryFn: getMyPlans,
  });

  if (isLoading) {
    return (
      <div className="plan-loading">
        <div className="spinner large" />
        <p>Loading your plans…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="plan-error">
        <p>Could not load your plans.</p>
      </div>
    );
  }

  return (
    <div className="myplans-page">
      <div className="myplans-header">
        <h1>My meal plans</h1>
        <button className="btn btn-primary" onClick={() => navigate("/planner")}>
          <PlusCircle size={16} /> New plan
        </button>
      </div>

      {plans && plans.length === 0 ? (
        <div className="myplans-empty">
          <CalendarDays size={56} strokeWidth={1} />
          <h2>No plans yet</h2>
          <p>Generate your first meal plan to get started.</p>
          <button className="btn btn-primary btn-large" onClick={() => navigate("/planner")}>
            Create a plan
          </button>
        </div>
      ) : (
        <div className="myplans-list">
          {plans?.map((plan) => {
            const dateLabel = plan.start_date
              ? new Date(plan.start_date).toLocaleDateString("en-US", {
                  weekday: "long",
                  month: "long",
                  day: "numeric",
                  year: "numeric",
                })
              : "No start date";

            return (
              <button
                key={plan.id}
                className="plan-row"
                onClick={() => navigate(`/plan/${plan.id}`)}
              >
                <div className="plan-row-icon">
                  <CalendarDays size={20} />
                </div>
                <div className="plan-row-info">
                  <span className="plan-row-title">{plan.num_days}-day plan</span>
                  <span className="plan-row-date">{dateLabel}</span>
                </div>
                <ChevronRight size={18} className="plan-row-arrow" />
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
