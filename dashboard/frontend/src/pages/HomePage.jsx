import { Link } from 'react-router-dom';
import { BarChart3, Lightbulb, Table2, Wrench, ArrowRight } from 'lucide-react';

export default function HomePage() {
    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <h1 className="hero-title">
                        <span className="hero-brand">CareCrew</span>
                        <span className="hero-tagline">Autonomous Predictive Maintenance for Automotive Fleets</span>
                    </h1>
                    <p className="hero-description">
                        Predict failures before they happen. Optimize service scheduling.
                        Feed actionable insights back to manufacturing. Increase customer retention
                        while reducing unexpected breakdowns.
                    </p>
                    <div className="hero-actions">
                        <Link to="/insights" className="btn btn-primary">
                            View Insights
                            <ArrowRight size={18} />
                        </Link>
                        <Link to="/visualizations" className="btn btn-secondary">
                            View Visualizations
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon insights">
                            <Lightbulb size={24} />
                        </div>
                        <h3 className="feature-title">Insights & Recommendations</h3>
                        <p className="feature-description">
                            AI-powered root cause analysis identifies critical issues and provides
                            actionable CAPA recommendations with projected ROI.
                        </p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon visualizations">
                            <BarChart3 size={24} />
                        </div>
                        <h3 className="feature-title">Visual Analytics</h3>
                        <p className="feature-description">
                            Real-time dashboards track fleet health scores, component failures,
                            service workloads, and customer engagement channels.
                        </p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon tables">
                            <Table2 size={24} />
                        </div>
                        <h3 className="feature-title">Data Tables & Auditability</h3>
                        <p className="feature-description">
                            Complete data transparency with sortable tables, maintenance logs,
                            and cost breakdowns for full audit trails.
                        </p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon manufacturing">
                            <Wrench size={24} />
                        </div>
                        <h3 className="feature-title">Manufacturing Feedback Loop</h3>
                        <p className="feature-description">
                            Connect field failure data to production lines. Identify supplier
                            issues and batch defects before they escalate.
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
}
