import { useDashboard } from '../context/DashboardContext';
import KPIGrid from '../components/KPIGrid';
import ChartsGrid from '../components/ChartsGrid';

export default function VisualizationsPage() {
    const { structuredData, loading } = useDashboard();

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">📊 Visualizations</h1>
                <p className="page-subtitle">
                    Real-time analytics and performance metrics for your fleet
                </p>
            </div>

            {/* KPI Cards */}
            <KPIGrid kpis={structuredData.kpis} loading={loading} />

            {/* Charts */}
            <ChartsGrid data={structuredData} loading={loading} />
        </div>
    );
}
