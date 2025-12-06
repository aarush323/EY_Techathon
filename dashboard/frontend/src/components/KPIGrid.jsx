import React from 'react';
import { Activity, Users, Settings, ThumbsUp, TrendingUp } from 'lucide-react';
import PropTypes from 'prop-types';

const KPIItem = ({ title, value, unit, trend, icon: Icon, color }) => (
    <div className="kpi-card">
        <div className="kpi-icon-wrapper" style={{ backgroundColor: `var(--${color}-light)`, color: `var(--${color})` }}>
            <Icon size={24} />
        </div>
        <div className="kpi-content">
            <div className="kpi-header">
                <span className="kpi-title">{title}</span>
                {trend && (
                    <span className={`trend-badge ${trend > 0 ? 'positive' : 'negative'}`}>
                        {trend > 0 ? '+' : ''}{trend}%
                    </span>
                )}
            </div>
            <div className="kpi-value-group">
                <span className="kpi-value">{value}</span>
                {unit && <span className="kpi-unit">{unit}</span>}
            </div>
        </div>
    </div>
);

KPIItem.propTypes = {
    title: PropTypes.string.isRequired,
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    unit: PropTypes.string,
    trend: PropTypes.number,
    icon: PropTypes.elementType.isRequired,
    color: PropTypes.string.isRequired
};

export default function KPIGrid({ kpis, loading }) {
    if (loading) {
        return (
            <section className="kpi-grid">
                {[1, 2, 3, 4, 5].map((i) => (
                    <div key={i} className="kpi-card skeleton" style={{ height: '120px' }}></div>
                ))}
            </section>
        );
    }

    // Default values to prevent crash if data is missing
    const {
        fleetHealthScore = 0,
        criticalVehicles = 0,
        serviceCenterUtilization = 0,
        customerSatisfaction = 0,
        costSavings = 0
    } = kpis || {};

    return (
        <section className="kpi-grid">
            <KPIItem
                title="Fleet Health Score"
                value={fleetHealthScore}
                unit="%"
                icon={Activity}
                color="status-success"
            />
            <KPIItem
                title="Critical Vehicles"
                value={criticalVehicles}
                icon={TrendingUp}
                color="status-critical"
            />
            <KPIItem
                title="Utilization"
                value={serviceCenterUtilization}
                unit="%"
                icon={Settings}
                color="status-warning"
            />
            <KPIItem
                title="Satisfaction"
                value={customerSatisfaction}
                unit="%"
                icon={ThumbsUp}
                color="primary"
            />
            <KPIItem
                title="Cost Savings"
                value={`$${(costSavings / 1000).toFixed(1)}k`}
                icon={Users}
                color="accent"
            />
        </section>
    );
}

KPIGrid.propTypes = {
    kpis: PropTypes.object,
    loading: PropTypes.bool
};
