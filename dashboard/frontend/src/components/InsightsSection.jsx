import React, { useState } from 'react';
import { AlertTriangle, Wrench, TrendingUp, ChevronDown, ChevronRight } from 'lucide-react';

const InsightCard = ({ title, subtitle, icon: Icon, type, children, defaultExpanded = true }) => {
    const [expanded, setExpanded] = useState(defaultExpanded);

    return (
        <div className={`insight-card-premium ${type}-card`}>
            <div className="card-header-premium" onClick={() => setExpanded(!expanded)}>
                <div className="card-title-group">
                    <div className={`card-icon ${type}`}>
                        <Icon size={20} />
                    </div>
                    <div>
                        <h3>{title}</h3>
                        <span className="card-subtitle">{subtitle}</span>
                    </div>
                </div>
                <div className="expand-icon">
                    {expanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                </div>
            </div>
            <div className={`card-body-premium ${!expanded ? 'collapsed' : ''}`}>
                <div className="insight-content">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default function InsightsSection() {
    return (
        <section className="insights-section" id="insights">
            <div className="insights-header">
                <div className="header-content">
                    <div className="header-icon">💡</div>
                    <div className="header-text">
                        <h2>Manufacturing Quality Insights & Recommendations</h2>
                        <p className="section-subtitle">Root Cause Analysis and Strategic Action Plan</p>
                    </div>
                </div>
            </div>

            <div className="insights-grid-premium">
                {/* Card 1: Critical Findings */}
                <InsightCard
                    title="Top Critical Findings"
                    subtitle="Root Cause Analysis (RCA)"
                    icon={AlertTriangle}
                    type="critical"
                >
                    <ul className="insight-list">
                        <li>
                            <strong>Brake System:</strong> Material composition too weak + Q3 batch BRK-2025-Q3-001 at 100% defect rate
                        </li>
                        <li>
                            <strong>Transmission:</strong> Cooler undersized + brazing fin defect from Supplier B (18–22% defect rate)
                        </li>
                        <li>
                            <strong>Engine Control:</strong> ECU firmware v2.1 fault + Supplier C sensors failing early
                        </li>
                        <li>
                            <strong>Thermostat:</strong> Supplier E unauthorized wax formulation change (95% defect rate)
                        </li>
                    </ul>
                </InsightCard>

                {/* Card 2: Recommendations */}
                <InsightCard
                    title="High-Impact Recommendations"
                    subtitle="Corrective & Preventive Actions (CAPA)"
                    icon={Wrench}
                    type="recommendations"
                >
                    <ul className="insight-list">
                        <li>
                            <strong>Upgrade brake pad material</strong> + increase rotor thermal mass
                            <br /><span style={{ fontSize: '12px', opacity: 0.8, color: 'var(--text-secondary)' }}>Expected: –92% failures</span>
                        </li>
                        <li>
                            <strong>Redesign transmission cooler</strong> + upgrade ATF specification
                            <br /><span style={{ fontSize: '12px', opacity: 0.8, color: 'var(--text-secondary)' }}>Expected: –85% failures</span>
                        </li>
                        <li>
                            <strong>Deploy ECU firmware v2.4</strong> + upgrade O2 sensor spec
                            <br /><span style={{ fontSize: '12px', opacity: 0.8, color: 'var(--text-secondary)' }}>Expected: –78% failures</span>
                        </li>
                        <li>
                            <strong>Redesign thermostat valve</strong> + tighten housing tolerance
                            <br /><span style={{ fontSize: '12px', opacity: 0.8, color: 'var(--text-secondary)' }}>Expected: –88% failures</span>
                        </li>
                    </ul>
                </InsightCard>

                {/* Card 3: Executive Summary */}
                <InsightCard
                    title="Executive Summary & ROI"
                    subtitle="Strategic Actions & Financial Impact"
                    icon={TrendingUp}
                    type="summary"
                >
                    <ul className="insight-list">
                        <li><strong>Critical suppliers requiring intervention:</strong> A, B, C, E</li>
                        <li><strong>Affected manufacturing batches:</strong> 7</li>
                        <li><strong>Fleet-wide projected failure reduction:</strong> 45–62%</li>
                        <li><strong>12-month ROI:</strong> <span style={{ color: 'var(--status-success)', fontWeight: 700 }}>38–68%</span></li>
                        <li><strong>Payback period:</strong> 14–24 months</li>
                    </ul>
                </InsightCard>
            </div>
        </section>
    );
}
