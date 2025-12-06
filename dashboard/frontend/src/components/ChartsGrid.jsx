import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
import PropTypes from 'prop-types';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const ChartCard = ({ title, metric, children, wide = false }) => (
    <div className={`chart-card ${wide ? 'wide' : ''}`}>
        <div className="card-header">
            <h3>{title}</h3>
            {metric && <span className="trend-badge positive">{metric}</span>}
        </div>
        <div className={`chart-container ${title.includes('Priority') ? 'donut-container' : ''}`}>
            {children}
        </div>
    </div>
);

export default function ChartsGrid({ data, loading }) {
    if (loading) {
        return <div className="charts-grid"><p>Loading charts...</p></div>;
    }

    const fleet = data?.fleet || {};
    const failures = data?.failures || {};
    const scheduling = data?.scheduling || {};
    const engagement = data?.engagement || {};

    // --- 1. Fleet Health Trend (Mock data generation as in original script.js) ---
    const healthLabels = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'];
    const healthValues = [92, 91, 89, 88, 85, 87]; // Simplified for demo
    const healthTrendData = {
        labels: healthLabels,
        datasets: [
            {
                label: 'Fleet Health Score',
                data: healthValues,
                fill: true,
                backgroundColor: 'rgba(99,102,241,0.18)',
                borderColor: 'rgba(99,102,241,1)',
                borderWidth: 2.8,
                tension: 0.28,
                pointRadius: 4,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: 'rgba(99,102,241,1)',
                pointBorderWidth: 2
            }
        ]
    };

    // --- 2. Priority Distribution ---
    const priorityData = {
        labels: ['Healthy', 'Warning', 'Critical'],
        datasets: [{
            data: [fleet.healthy || 12, fleet.warning || 5, fleet.critical || 3],
            backgroundColor: ['#00b894', '#fdcb6e', '#ff7675'],
            borderWidth: 0
        }]
    };

    // --- 3. Component Failures ---
    const predictions = failures.predictions || [];
    const riskMap = {};
    if (predictions.length > 0) {
        predictions.forEach(p => {
            if (p.component && p.failure_probability) {
                riskMap[p.component] = Math.max(riskMap[p.component] || 0, p.failure_probability);
            }
        });
    } else {
        riskMap['Engine'] = 45;
        riskMap['Brakes'] = 30;
        riskMap['Transmission'] = 25;
    }

    const failureData = {
        labels: Object.keys(riskMap),
        datasets: [{
            label: 'Max Failure Probability (%)',
            data: Object.values(riskMap),
            backgroundColor: '#6c63ff',
            borderRadius: 4
        }]
    };

    // --- 4. Service Workload ---
    const centers = scheduling.service_centers || [];
    const centerLabels = centers.length ? centers.map(c => c.name.replace(' Service Center', '')) : ['Mumbai', 'Delhi', 'Bangalore'];
    const centerData = centers.length ? centers.map(c => Math.round((c.appointments_today / c.capacity) * 100)) : [60, 80, 45];

    const workloadData = {
        labels: centerLabels,
        datasets: [{
            label: 'Utilization (%)',
            data: centerData,
            backgroundColor: '#a29bfe',
            borderRadius: 4
        }]
    };

    // --- 5. Engagement Channels ---
    const methods = engagement.communication_methods || {};
    const channelLabels = Object.keys(methods).length ? Object.keys(methods).map(k => k.replace(/_/g, ' ').toUpperCase()) : ['SMS', 'EMAIL', 'APP', 'CALL'];
    const channelData = Object.keys(methods).length ? Object.values(methods) : [45, 30, 20, 5];

    const engagementData = {
        labels: channelLabels,
        datasets: [{
            label: 'Engagements',
            data: channelData,
            backgroundColor: ['#6c63ff', '#00b894', '#fdcb6e', '#ff7675'],
            borderRadius: 4
        }]
    };

    // Common Options
    const standardOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } }, y: { beginAtZero: true } }
    };

    return (
        <section className="charts-grid" id="visualizations">
            <ChartCard title="Fleet Health Score Trend" metric="+2.3% vs Nov" wide>
                <Line data={healthTrendData} options={{ ...standardOptions, scales: { y: { min: 50, max: 100 } } }} />
            </ChartCard>

            <ChartCard title="Priority Distribution">
                <Doughnut
                    data={priorityData}
                    options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '70%',
                        plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, boxWidth: 8 } } }
                    }}
                />
            </ChartCard>

            <ChartCard title="Component Failures">
                <Bar data={failureData} options={{ ...standardOptions, scales: { y: { max: 100 } } }} />
            </ChartCard>

            <ChartCard title="Service Workload">
                <Bar data={workloadData} options={{ ...standardOptions, indexAxis: 'y', scales: { x: { max: 100 } } }} />
            </ChartCard>

            <ChartCard title="Engagement Channels">
                <Bar data={engagementData} options={standardOptions} />
            </ChartCard>
        </section>
    );
}

ChartCard.propTypes = {
    title: PropTypes.string.isRequired,
    metric: PropTypes.string,
    children: PropTypes.node.isRequired,
    wide: PropTypes.bool
};

ChartsGrid.propTypes = {
    data: PropTypes.object,
    loading: PropTypes.bool
};
