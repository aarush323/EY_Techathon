import React, { useEffect, useState } from 'react';
import { Sun, Moon, Activity } from 'lucide-react';

export default function Header() {
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    const currentDate = new Date().toLocaleDateString('en-US');

    return (
        <header className="top-bar">
            <div className="logo-section">
                <div className="brand">
                    <div className="brand-icon">
                        <Activity size={24} color="currentColor" />
                    </div>
                    <span className="brand-name">CareCrew</span>
                </div>
            </div>
            <div className="header-controls">
                <div className="status-container">
                    <div className="status-dot"></div>
                    <span className="status-text">Live</span>
                </div>
                <div className="date-container">
                    <span className="date-label">Updated</span>
                    <span className="date-value">{currentDate}</span>
                </div>
                <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
                    {theme === 'light' ? <Sun size={18} /> : <Moon size={18} />}
                </button>
            </div>
        </header>
    );
}
