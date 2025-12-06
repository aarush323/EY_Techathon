import React from 'react';
import PropTypes from 'prop-types';
import { calculateTableRelevance, detectTableIcon, generateTableTitle, calculateMaintenanceRow } from '../utils/dashboardLogic';

// Dynamic Table Component
const DynamicTable = ({ table }) => {
    const icon = detectTableIcon(table);
    const title = generateTableTitle(table);

    if (!table.rows || table.rows.length === 0) return null;

    return (
        <div className="table-section">
            <div className="section-header">
                <h3>{icon} {title}</h3>
            </div>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            {table.headers.map((h, i) => (
                                <th key={i}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {table.rows.map((row, rIdx) => (
                            <tr key={rIdx}>
                                {table.headers.map((h, cIdx) => (
                                    <td key={cIdx} dangerouslySetInnerHTML={{ __html: formatCell(row[h], h) }}></td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

// Helper for cell formatting (re-impl of formatTableCell from script.js)
function formatCell(value, header) {
    if (!value || value === '-') return '-';
    const strVal = String(value);
    const lowHeader = header.toLowerCase();

    // Badges
    if (lowHeader.includes('status')) return `<span class="badge badge-status-${strVal.toLowerCase()}">${strVal}</span>`;
    if (lowHeader.includes('priority')) return `<span class="badge badge-${strVal.toLowerCase()}">${strVal}</span>`;
    if (strVal.includes('%')) {
        const num = parseFloat(strVal);
        let color = 'info';
        if (num > 80) color = 'success';
        else if (num < 30) color = 'danger';
        return `<span class="badge badge-${color}">${strVal}</span>`;
    }
    return strVal;
}

export default function TablesSection({ tables, fleetData }) {
    // Sort tables by relevance
    const sortedTables = [...(tables || [])].map(t => ({
        ...t,
        score: calculateTableRelevance(t)
    })).sort((a, b) => b.score - a.score);

    // Maintenance Table Data
    const maintenanceRows = (fleetData?.vehicles || []).map(v =>
        calculateMaintenanceRow(v, v.vehicle_id)
    );

    const totalImmediateCost = maintenanceRows.reduce((acc, row) => acc + row.cost, 0);

    return (
        <section className="tables-section" id="tables">
            {/* 1. All Dynamic Tables */}
            <div className="section-title">
                <h2>Data Analysis</h2>
                <p className="section-subtitle">Complete report from markdown parsing</p>
            </div>

            <div id="all-tables-container">
                {sortedTables.length > 0 ? (
                    sortedTables.map((t, i) => <DynamicTable key={i} table={t} />)
                ) : (
                    <div className="table-section"><p style={{ padding: '20px', textAlign: 'center', color: 'var(--text-tertiary)' }}>No tables data found.</p></div>
                )}
            </div>

            {/* 2. Main Maintenance Table */}
            <div className="table-section">
                <div className="section-header">
                    <h3>Fleet Maintenance & Alerts</h3>
                </div>
                <div className="table-container">
                    <table id="maintenance-table">
                        <thead>
                            <tr>
                                <th>Vehicle ID</th>
                                <th>Segment</th>
                                <th>Priority</th>
                                <th>Failure Risk (%)</th>
                                <th>Status</th>
                                <th>Service Center</th>
                                <th>Est. Hours</th>
                                <th>Cost Est. ($)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {maintenanceRows.map((row, i) => (
                                <tr key={i}>
                                    <td style={{ fontWeight: 500 }}>{row.id}</td>
                                    <td>{row.segment}</td>
                                    <td><span className={`badge badge-${row.priority}`}>{row.priority.toUpperCase()}</span></td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                            <div style={{ flex: 1, height: '6px', background: '#eee', borderRadius: '3px' }}>
                                                <div style={{ width: `${row.risk}%`, height: '100%', background: row.risk > 80 ? '#ff7675' : '#00b894', borderRadius: '3px' }}></div>
                                            </div>
                                            <span style={{ fontSize: '12px' }}>{row.risk}%</span>
                                        </div>
                                    </td>
                                    <td><span className={`badge badge-status-${row.status.toLowerCase()}`}>{row.status}</span></td>
                                    <td>{row.center}</td>
                                    <td>{row.hours.toFixed(1)} hrs</td>
                                    <td><strong style={{ color: 'var(--primary-purple)' }}>${row.cost.toFixed(2)}</strong></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="table-footer">
                    <div className="table-total">
                        TOTAL IMMEDIATE COSTS: <span style={{ color: 'var(--primary-purple)' }}>${totalImmediateCost.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </section>
    );
}

TablesSection.propTypes = {
    tables: PropTypes.array,
    fleetData: PropTypes.object
};

DynamicTable.propTypes = {
    table: PropTypes.object
};
