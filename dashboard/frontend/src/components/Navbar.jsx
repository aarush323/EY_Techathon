import { NavLink } from 'react-router-dom';
import { Activity } from 'lucide-react';

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                {/* Logo */}
                <NavLink to="/" className="navbar-brand">
                    <div className="navbar-logo">
                        <Activity size={24} />
                    </div>
                    <span className="navbar-title">CareCrew</span>
                </NavLink>

                {/* Navigation Links */}
                <div className="navbar-links">
                    <NavLink
                        to="/"
                        className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}
                        end
                    >
                        Home
                    </NavLink>
                    <NavLink
                        to="/insights"
                        className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}
                    >
                        Insights
                    </NavLink>
                    <NavLink
                        to="/visualizations"
                        className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}
                    >
                        Visualizations
                    </NavLink>
                    <NavLink
                        to="/tables"
                        className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}
                    >
                        Data Tables
                    </NavLink>
                    <NavLink
                        to="/recommendations"
                        className={({ isActive }) => `navbar-link ${isActive ? 'active' : ''}`}
                    >
                        Recommendations
                    </NavLink>
                </div>
            </div>
        </nav>
    );
}
