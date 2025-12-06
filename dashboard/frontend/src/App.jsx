import React from 'react';
import Header from './components/Header';
import KPIGrid from './components/KPIGrid';
import ChartsGrid from './components/ChartsGrid';
import InsightsSection from './components/InsightsSection';
import TablesSection from './components/TablesSection';
import useDashboardData from './hooks/useDashboardData';

// Placeholder Quick Nav Component
const QuickNav = () => (
  <nav className="quick-nav">
    <a href="#visualizations" className="nav-btn">📊 Visualizations</a>
    <a href="#tables" className="nav-btn">📋 Data Tables</a>
    <a href="#insights" className="nav-btn">💡 Insights & Recommendations</a>
  </nav>
);

function App() {
  const { data, loading, error } = useDashboardData();

  const structuredData = data?.structuredData || {};
  const tables = data?.tables || [];

  if (error) {
    return (
      <div className="dashboard-container">
        <Header />
        <div style={{ padding: '40px', textAlign: 'center', color: '#ff7675' }}>
          <h3>⚠️ Unable to load dashboard data</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Header />

      {/* KPI Cards */}
      <KPIGrid kpis={structuredData.kpis} loading={loading} />

      {/* Navigation */}
      <QuickNav />

      {/* Charts Section */}
      <ChartsGrid data={structuredData} loading={loading} />

      {/* Insights Section (Premium 3-Card) */}
      <InsightsSection />

      {/* Tables Section */}
      <TablesSection tables={tables} fleetData={structuredData.fleet} />
    </div>
  );
}

export default App;
