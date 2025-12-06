import { createContext, useContext } from 'react';
import useDashboardData from '../hooks/useDashboardData';

const DashboardContext = createContext(null);

export function DashboardProvider({ children }) {
    const { data, loading, error } = useDashboardData();

    const structuredData = data?.structuredData || {};
    const tables = data?.tables || [];

    return (
        <DashboardContext.Provider value={{ data, structuredData, tables, loading, error }}>
            {children}
        </DashboardContext.Provider>
    );
}

export function useDashboard() {
    const context = useContext(DashboardContext);
    if (!context) {
        throw new Error('useDashboard must be used within a DashboardProvider');
    }
    return context;
}
