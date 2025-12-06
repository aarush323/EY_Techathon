# React Migration Implementation Plan

## Goal
Convert the existing vanilla JS dashboard to a React application without modifying the backend (`app.py`) or Python files. The React app will run as a separate frontend service consuming the existing API.

## Architecture
- **Framework**: React (via Vite for fast setup)
- **Styling**: Port existing `styles.css` to global CSS.
- **State Management**: React `useState` / `useEffect` context for global theme.
- **Charts**: `react-chartjs-2` + `chart.js`.
- **Parsing**: Port `script.js` logic to helper functions.

## Components Structure
```
src/
  components/
    Header.jsx          # Logo, Status, Date, Theme Toggle
    KPIGrid.jsx         # The top 5 metrics cards
    ChartsGrid.jsx      # Wrapper for all charts
    InsightsSection.jsx # The Premium 3-card layout (Hardcoded/Parsed logic)
    TablesSection.jsx   # Data Analysis & Maintenance Table
    Dashboard.jsx       # Main container
  hooks/
    useDashboardData.js # Fetching & State logic
  utils/
    formatters.js       # formatCurrency, etc.
    parsers.js          # Logic from script.js (renderKPIs logic, etc.)
  App.jsx               # Root component (Theme logic)
  main.jsx              # Entry point
  index.css             # Ported styles.css
```

## Parsing Logic Migration
- **KPIs**: Port `renderKPIs` logic to `KPIGrid.jsx`.
- **Charts**: Port `renderCharts` logic to `ChartsGrid.jsx`. Use `react-chartjs-2`.
- **Insights**: Port the **hardcoded** `renderInsights` function to `InsightsSection.jsx`.
- **Tables**: Port `renderTables` and `renderMaintenanceTable` logic.

## Dependencies
- `react`, `react-dom`
- `chart.js`, `react-chartjs-2`
- `marked` (if needed for markdown fallback)
- `lodash` (for data manips)
- `lucide-react` (for icons, replacing unicode/svgs where appropriate or keeping SVGs)

## Step-by-Step Plan
1.  **Initialize React App**: Create `frontend` directory with Vite.
2.  **Migrate Styles**: Copy `styles.css` content to `frontend/src/index.css`.
3.  **Setup Utilities**: Extract logic from `script.js` into `frontend/src/utils/dashboardLogic.js`.
4.  **Create Components**: Build each section component.
5.  **Implement Data Fetching**: Create hook to fetch from `http://localhost:5000/api/generate_report`.
6.  **Verify**: Ensure UI looks identical and data loads correctly.

## User Action Required
- Run `npm install` and `npm run dev` in the new `frontend` directory.
- Backend `app.py` continues running on port 5000.
