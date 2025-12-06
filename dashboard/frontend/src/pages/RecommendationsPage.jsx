import { useState } from 'react';
import { Wrench, ChevronDown, ChevronRight, CheckCircle } from 'lucide-react';

const RecommendationCard = ({ title, subtitle, icon: Icon, type, children, defaultExpanded = true }) => {
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

export default function RecommendationsPage() {
    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">🔧 Recommendations</h1>
                <p className="page-subtitle">
                    Corrective & Preventive Actions (CAPA) with Expected Impact
                </p>
            </div>

            <div className="recommendations-content">
                {/* High-Impact Recommendations Card */}
                <RecommendationCard
                    title="High-Impact Recommendations"
                    subtitle="Corrective & Preventive Actions (CAPA)"
                    icon={Wrench}
                    type="recommendations"
                >
                    <ul className="insight-list">
                        <li>
                            <strong>Upgrade brake pad material</strong> + increase rotor thermal mass
                            <br /><span className="impact-text">Expected: –92% failures</span>
                        </li>
                        <li>
                            <strong>Redesign transmission cooler</strong> + upgrade ATF specification
                            <br /><span className="impact-text">Expected: –85% failures</span>
                        </li>
                        <li>
                            <strong>Deploy ECU firmware v2.4</strong> + upgrade O2 sensor spec
                            <br /><span className="impact-text">Expected: –78% failures</span>
                        </li>
                        <li>
                            <strong>Redesign thermostat valve</strong> + tighten housing tolerance
                            <br /><span className="impact-text">Expected: –88% failures</span>
                        </li>
                    </ul>
                </RecommendationCard>

                {/* Priority Actions Card */}
                <RecommendationCard
                    title="Immediate Priority Actions"
                    subtitle="What to do this week"
                    icon={CheckCircle}
                    type="summary"
                >
                    <ul className="insight-list priority-list">
                        <li>
                            <span className="priority-badge high">HIGH</span>
                            Contact Supplier E regarding unauthorized wax formulation change
                        </li>
                        <li>
                            <span className="priority-badge high">HIGH</span>
                            Quarantine batch BRK-2025-Q3-001 (100% defect rate)
                        </li>
                        <li>
                            <span className="priority-badge medium">MEDIUM</span>
                            Schedule firmware update campaign for ECU v2.4 deployment
                        </li>
                        <li>
                            <span className="priority-badge medium">MEDIUM</span>
                            Initiate supplier audit for Supplier B (brazing fin defects)
                        </li>
                        <li>
                            <span className="priority-badge low">LOW</span>
                            Review ATF specification upgrade timeline with engineering
                        </li>
                    </ul>
                </RecommendationCard>
            </div>
        </div>
    );
}
