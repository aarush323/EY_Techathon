# React Dashboard Frontend

This is the React migration of the dashboard, consuming the Python backend API.

## Setup & Run

1.  **Install Dependencies** (if not already done):
    ```bash
    npm install
    ```

2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    This will start the frontend at `http://localhost:5173`.
    The proxy is configured to forward `/api` requests to `http://localhost:5000` (your running Python backend).

3.  **Build for Production**:
    ```bash
    npm run build
    ```
    The output will be in `dist/`.

## Architecture
- **Vite + React**: Fast build tool and framework.
- **Chart.js**: For visualizations (ChartGrid).
- **Styles**: `index.css` contains the ported premium logic from `styles.css`.
- **Parsing**: `src/utils/dashboardLogic.js` contains the ported parsing logic.
- **Components**: `src/components/` contains the modularized UI.
