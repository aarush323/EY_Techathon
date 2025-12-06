import { useState, useEffect } from 'react';
import { processMarkdownPipeline } from '../utils/dashboardLogic';

export default function useDashboardData() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                console.log('Fetching dashboard data...');
                // Use relative path to leverage Vite proxy in dev, and relative in prod
                const response = await fetch('/api/dashboard');
                if (!response.ok) throw new Error('Network response was not ok');

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
