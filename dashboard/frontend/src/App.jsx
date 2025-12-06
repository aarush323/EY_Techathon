import { Routes, Route } from 'react-router-dom';
import { DashboardProvider } from './context/DashboardContext';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import InsightsPage from './pages/InsightsPage';
import VisualizationsPage from './pages/VisualizationsPage';
import TablesPage from './pages/TablesPage';
import RecommendationsPage from './pages/RecommendationsPage';

function App() {
  return (
    <DashboardProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="insights" element={<InsightsPage />} />
          <Route path="visualizations" element={<VisualizationsPage />} />
          <Route path="tables" element={<TablesPage />} />
          <Route path="recommendations" element={<RecommendationsPage />} />
        </Route>
      </Routes>
    </DashboardProvider>
  );
}

export default App;
