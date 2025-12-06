// =====================================================
// THEME SWITCHER — LIGHT/DARK MODE
// Executes IMMEDIATELY before any DOM content loads
// =====================================================

// IMMEDIATE EXECUTION - Apply theme before page renders
const savedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
document.documentElement.setAttribute('data-theme', initialTheme);

// Theme management after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');

    if (!toggleButton) {
        console.warn('Theme toggle button not found');
        return;
    }

    // Toggle theme function
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        console.log(`Theme switched to: ${newTheme}`);
    }

    // Attach click handler
    toggleButton.addEventListener('click', toggleTheme);
    console.log('Theme toggle initialized');

    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            const systemTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', systemTheme);
        }
    });
});
