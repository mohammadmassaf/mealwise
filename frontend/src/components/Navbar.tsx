import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Salad, LogOut, CalendarDays } from "lucide-react";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <Salad size={28} />
        <span>MealWise</span>
      </Link>
      <div className="navbar-actions">
        {isAuthenticated ? (
          <>
            <Link to="/my-plans" className="btn btn-ghost">
              <CalendarDays size={16} /> My Plans
            </Link>
            <Link to="/planner" className="btn btn-outline">New Plan</Link>
            <button onClick={handleLogout} className="btn btn-ghost" title="Logout">
              <LogOut size={18} />
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-outline">Login</Link>
            <Link to="/register" className="btn btn-primary">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
}
