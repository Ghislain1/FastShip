import { Link } from "@tanstack/react-router";

export default function Navbar() {
    return (
        <nav style={{ display: "flex", gap: "15px" }}>
            <Link to="/">Home</Link>
            <Link to="/services">Services</Link>
            <Link to="/partners">Partner</Link>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
        </nav>
    );
}