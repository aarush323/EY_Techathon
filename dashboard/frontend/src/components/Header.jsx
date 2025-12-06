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
        <header class="top-bar">
            <div class="logo-section">
                <div class="brand">
                    <div class="brand-icon">
                        <Activity size={24} color="currentColor" />
                    </div>
                    <span class="brand-name">CareCrew</span>
                </div>
            </div>
            <div class="header-controls">
                <div class="status-container">
                    <div class="status-dot"></div>
                    <span class="status-text">Live</span>
                </div>
                <div class="date-container">
                    <span class="date-label">Updated</span>
                    <span class="date-value">{currentDate}</span>
                </div>
                <button class="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
                    {theme === 'light' ? <Sun size={18} /> : <Moon size={18} />}
                </button>
            </div>
        </header>
    );
}
