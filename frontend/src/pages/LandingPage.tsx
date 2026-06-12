import { Link } from "react-router-dom";
import { Salad, Zap, RefreshCw, BarChart2 } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="landing">
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">AI-powered meal planning</div>
          <h1>Eat well, every day — without the effort</h1>
          <p>
            MealWise generates personalized weekly meal plans based on your diet, allergies,
            and calorie goals. Powered by Gemini AI and real nutrition data.
          </p>
          <div className="hero-actions">
            <Link to="/register" className="btn btn-primary btn-large">Get started free</Link>
            <Link to="/login" className="btn btn-outline btn-large">Log in</Link>
          </div>
        </div>
        <div className="hero-visual">
          <Salad size={180} strokeWidth={0.8} />
        </div>
      </section>

      <section className="features">
        <h2>Everything you need to eat smarter</h2>
        <div className="features-grid">
          <div className="feature-card">
            <Zap size={32} />
            <h3>AI-generated plans</h3>
            <p>Gemini builds a full week of meals tailored to your preferences in seconds.</p>
          </div>
          <div className="feature-card">
            <BarChart2 size={32} />
            <h3>Real nutrition data</h3>
            <p>Calorie counts are verified against the USDA food database — not guessed.</p>
          </div>
          <div className="feature-card">
            <RefreshCw size={32} />
            <h3>Regenerate any day</h3>
            <p>Don't like Tuesday? Regenerate just that day without touching the rest.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
