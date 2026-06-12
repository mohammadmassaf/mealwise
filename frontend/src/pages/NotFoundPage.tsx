import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="plan-error">
      <h1 style={{ fontSize: "4rem", margin: 0 }}>404</h1>
      <p>This page doesn't exist.</p>
      <Link to="/" className="btn btn-primary">Go home</Link>
    </div>
  );
}
