import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import { useDashboard } from '../context/DashboardContext';

export default function Layout() {
    const { error } = useDashboard();

    return (
        <div className="app-layout">
            <Navbar />
            <main className="main-content">
                {error ? (
                    <div className="error-container">
                        <div className="error-card">
                            <h3>⚠️ Unable to load dashboard data</h3>
                            <p>{error}</p>
                        </div>
                    </div>
                ) : (
                    <Outlet />
                )}
            </main>
        </div>
    );
}
