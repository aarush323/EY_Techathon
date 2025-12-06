import { useState, useEffect } from 'react';
import { processMarkdownPipeline } from '../utils/dashboardLogic';

// Configurable API base URL - empty in dev (Vite proxy handles /api), set in prod
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export default function useDashboardData() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            const url = `${API_BASE_URL}/api/dashboard`;
            try {
                console.log('Fetching dashboard data from:', url);
                const response = await fetch(url);
                if (!response.ok) {
                    console.error('Dashboard fetch failed:', response.status, response.statusText, response.url);
                    throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
                }

                const jsonData = await response.json();

                if (jsonData.report_text) {
                    const result = processMarkdownPipeline(jsonData.report_text);
                    if (result) {
                        setData(result); // { structuredData, tables }
                    } else {
                        throw new Error('Markdown processing failed');
                    }
                } else {
                    // Fallback if already JSON
                    setData({ structuredData: jsonData, tables: [] });
                }
            } catch (err) {
                console.error(err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, []);

    return { data, loading, error };
}
