import { useDashboard } from '../context/DashboardContext';
import TablesSection from '../components/TablesSection';

export default function TablesPage() {
    const { tables, structuredData } = useDashboard();

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">📋 Data Tables</h1>
                <p className="page-subtitle">
                    Complete data analysis with sortable tables and maintenance logs
                </p>
            </div>

            <TablesSection tables={tables} fleetData={structuredData.fleet} />
        </div>
    );
}
