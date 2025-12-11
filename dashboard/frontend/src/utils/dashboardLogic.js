import { marked } from 'marked';
import _ from 'lodash';

// ============================================================================
// MARKDOWN PIPEPLINE LOGIC
// ============================================================================

export function processMarkdownPipeline(markdownText) {
    try {
        console.log('📄 Starting markdown parsing pipeline...');

        // Convert markdown → HTML
        const html = marked.parse(markdownText);

        // Load HTML into DOMParser
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        // Extract tables
        const tables = extractAllTables(doc);

        // Extract KPIs
        const kpis = extractKPIsFromMarkdown(markdownText);

        // Build structured data
        const structuredData = buildDataModels(tables, kpis);

        return {
            structuredData,
            tables, // Return raw tables too for the "All Tables" section
            markdownText // Return raw markdown if needed
        };

    } catch (error) {
        console.error('❌ Error in markdown pipeline:', error);
        return null;
    }
}

// ============================================================================
// TABLE EXTRACTION
// ============================================================================
function extractAllTables(doc) {
    const tables = [];
    const tableElements = doc.querySelectorAll("table");

    tableElements.forEach((table) => {
        // Extract headers
        const headers = [];
        table.querySelectorAll("th").forEach(th => {
            headers.push(th.textContent.trim());
        });

        // Extract rows
        const rows = [];
        table.querySelectorAll("tr").forEach(tr => {
            const cells = tr.querySelectorAll("td");
            if (cells.length > 0) {
                const rowObj = {};
                cells.forEach((td, idx) => {
                    if (headers[idx]) {
                        rowObj[headers[idx]] = td.textContent.trim();
                    }
                });
                if (Object.keys(rowObj).length) {
                    rows.push(rowObj);
                }
            }
        });

        // Classify
        const tableType = classifyTable(headers);

        tables.push({
            type: tableType,
            headers: headers,
            rows: rows,
        });
    });

    return tables;
}

function classifyTable(headers) {
    const headerText = headers.join(' ').toLowerCase();

    if (headerText.includes('vehicle') || headerText.includes('sensor') || headerText.includes('maintenance')) return 'fleet';
    if (headerText.includes('component') || headerText.includes('failure') || headerText.includes('confidence')) return 'failures';
    if (headerText.includes('engagement') || headerText.includes('method') || headerText.includes('channel')) return 'engagement';
    if (headerText.includes('appointment') || headerText.includes('service center') || headerText.includes('workload')) return 'scheduling';
    if (headerText.includes('completion') || headerText.includes('satisfaction') || headerText.includes('quality')) return 'quality';
    if (headerText.includes('kpi') || headerText.includes('metric') || headerText.includes('current')) return 'kpis';

    return 'unknown';
}

// ============================================================================
// KPI EXTRACTION
// ============================================================================
function extractKPIsFromMarkdown(md) {
    const kpis = {};
    let match;

    // Fleet Health Score - Try multiple patterns
    match = /Fleet\s*Availability[^\d]*([\d.]+)%/i.exec(md);
    if (match) {
        kpis.fleetHealthScore = parseFloat(match[1]);
        console.log('✅ Found Fleet Health:', match[1]);
    }

    // Overall Engagement Rate
    match = /(?:Customer\s*)?Engagement\s*Rate[\s::\-–—]*([\d.]+)%/i.exec(md);
    if (match) {
        kpis.engagementRate = parseFloat(match[1]);
    }

    // Service Center Utilization - from workflow table
    match = /Service\s*Center\s*Utilization[\s|]*([\d.]+)%/i.exec(md);
    if (match) {
        kpis.serviceCenterUtilization = parseFloat(match[1]);
    }

    // Customer Satisfaction - Match: - **Customer Satisfaction (CSAT):** 4.6/5.0
    match = /-?\s*\*\*.*(?:Customer\s*Satisfaction|CSAT).*\*\*:?\s*([\d.]+)\/5/i.exec(md);
    if (match) {
        // Convert X/5 to percentage (X * 20)
        let val = parseFloat(match[1]);
        kpis.customerSatisfaction = (val * 20).toFixed(1); // 4.6/5 = 92%
        console.log('✅ Found Satisfaction:', match[1], '→', kpis.customerSatisfaction + '%');
    }

    // Critical Vehicles - from Priority table
    match = /\*\*Critical\*\*[\s|]+([\d,]+)/i.exec(md);
    if (match) {
        kpis.criticalVehicles = parseInt(match[1].replace(/,/g, ''));
    }

    // Avg Monthly Usage
    match = /Average.*Usage[\s::\-–—]+([\d,]+)/i.exec(md);
    if (match) kpis.avgMonthlyUsage = parseInt(match[1].replace(/,/g, ''));

    // Cost Savings - Try multiple patterns
    match = /Annual\s*Savings[^₹]*₹([\d.]+)\s*Cr/i.exec(md);
    if (match) {
        let crores = parseFloat(match[1]);
        kpis.costSavings = (crores * 10000); // Convert Cr to thousands
        console.log('✅ Found Cost Savings:', match[1], 'Cr →', kpis.costSavings, 'thousands');
    }

    // Predictive Accuracy
    match = /Predictive\s*Accuracy[^\d]*([\d.]+)%/i.exec(md);
    if (match) {
        kpis.predictiveAccuracy = parseFloat(match[1]);
    }

    // Fallback: Use table data if regex patterns failed
    if (!kpis.fleetHealthScore) {
        // Try completion_rate (93.1%) as fleet health
        if (kpis.completion_rate) {
            kpis.fleetHealthScore = kpis.completion_rate;
            console.log('📊 Using completion_rate as Fleet Health:', kpis.completion_rate);
        } else if (kpis.data_uptime) {
            kpis.fleetHealthScore = kpis.data_uptime;
            console.log('📊 Using data_uptime as Fleet Health:', kpis.data_uptime);
        }
    }

    if (!kpis.costSavings) {
        // Estimate from vehicle count: 12,450 vehicles * ₹1,500/vehicle/month * 12 months = ~₹22.4 Cr
        if (kpis.vehicles_covered) {
            kpis.costSavings = (kpis.vehicles_covered * 1.5); // Rough estimate: ₹1.5k savings per vehicle
            console.log('📊 Estimated Cost Savings from vehicle count:', kpis.costSavings, 'thousands');
        }
    }

    console.log('📊 Extracted KPIs:', kpis);
    return kpis;
}

// ============================================================================
// DATA MODELS
// ============================================================================
function buildDataModels(tables, kpis) {
    const data = {
        fleet: {},
        failures: {},
        engagement: {},
        scheduling: {},
        quality: {},
        kpis: kpis
    };

    tables.forEach(table => {
        switch (table.type) {
            case 'fleet': data.fleet = processFleetTable(table.rows); break;
            case 'failures': data.failures = processFailuresTable(table.rows); break;
            case 'engagement': data.engagement = processEngagementTable(table.rows); break;
            case 'scheduling': data.scheduling = processSchedulingTable(table.rows); break;
            case 'quality': data.quality = processQualityTable(table.rows); break;
            case 'kpis': Object.assign(data.kpis, processKPITable(table.rows)); break;
        }
    });

    return data;
}

// ... Processors (Fleet, Failures, etc.) ...
// Copied logic from script.js, adapted for export

function processFleetTable(rows) {
    const vehicles = rows.map(row => ({
        vehicle_id: findValue(row, ['vehicle', 'id', 'vehicle id']),
        status: findValue(row, ['status', 'health', 'condition']),
        priority: findValue(row, ['priority', 'severity', 'level']),
        segment: findValue(row, ['segment', 'vehicle type', 'class']),
        sensor_status: findValue(row, ['sensor', 'sensors']),
        maintenance: findValue(row, ['maintenance', 'next service'])
    }));

    const critical = vehicles.filter(v => v.priority && v.priority.toLowerCase().includes('critical')).length;
    const warning = vehicles.filter(v => v.priority && (v.priority.toLowerCase().includes('warning') || v.priority.toLowerCase().includes('medium'))).length;
    const healthy = vehicles.filter(v => v.priority && (v.priority.toLowerCase().includes('low') || v.priority.toLowerCase().includes('healthy'))).length;

    return { vehicles, total_vehicles: vehicles.length, critical, warning, healthy };
}

function processFailuresTable(rows) {
    const predictions = rows.map(row => ({
        vehicle_id: findValue(row, ['vehicle', 'id', 'vehicle id']),
        component: findValue(row, ['component', 'part', 'system']),
        failure_probability: parseFloatSafe(findValue(row, ['failure', 'probability', 'risk'])),
        confidence_level: parseFloatSafe(findValue(row, ['confidence'])),
        cost_implications: parseIntSafe(findValue(row, ['cost']))
    }));
    return { predictions, total_predictions: predictions.length };
}

function processEngagementTable(rows) {
    const methods = {};
    const engagements = rows.map(row => {
        const method = findValue(row, ['method', 'channel']);
        const count = parseIntSafe(findValue(row, ['count', 'total']));
        if (method) {
            const key = method.toLowerCase().replace(/\s+/g, '_');
            methods[key] = (methods[key] || 0) + (count || 1);
        }
        return { method, status: findValue(row, ['status']), count };
    });
    return { communication_methods: methods, engagements, total_customers: rows.length };
}

function processSchedulingTable(rows) {
    const appointments = rows.map(row => ({
        appointment_id: findValue(row, ['appointment', 'id']),
        vehicle_id: findValue(row, ['vehicle']),
        service_center: findValue(row, ['service center', 'center']),
        scheduled_date: findValue(row, ['date', 'scheduled']),
        workload: parseIntSafe(findValue(row, ['workload', 'capacity']))
    }));
    return { appointments, total_appointments: appointments.length }; // Simplified for brevity
}

function processQualityTable(rows) {
    return {
        completion_rate: parseFloatSafe(findValue(rows[0] || {}, ['completion'])) || 95,
        customer_satisfaction_score: parseFloatSafe(findValue(rows[0] || {}, ['satisfaction'])) || 87
    };
}

function processKPITable(rows) {
    const kpis = {};
    rows.forEach(row => {
        const name = findValue(row, ['kpi', 'metric', 'name']);
        const value = findValue(row, ['value', 'current', 'score']);
        if (name && value) {
            const key = name.toLowerCase().replace(/\s+/g, '_');
            kpis[key] = parseFloatSafe(value);
        }
    });
    return kpis;
}

// Utility Helpers
function findValue(obj, possibleKeys) {
    for (let key of Object.keys(obj)) {
        const lowerKey = key.toLowerCase();
        for (let searchKey of possibleKeys) {
            if (lowerKey.includes(searchKey.toLowerCase())) return obj[key];
        }
    }
    return null;
}

export function parseFloatSafe(value) {
    if (!value) return 0;
    const num = parseFloat(String(value).replace(/[^0-9.-]/g, ''));
    return isNaN(num) ? 0 : num;
}

export function parseIntSafe(value) {
    if (!value) return 0;
    const num = parseInt(String(value).replace(/[^0-9-]/g, ''));
    return isNaN(num) ? 0 : num;
}

// Logic for Main Maintenance Table Calculation (imported from script.js lines 1058+)
export function calculateMaintenanceRow(vehicle, id) {
    const segment = inferSegment(vehicle.segment, id);
    const priority = (vehicle.priority || 'Low').toLowerCase().replace(' level', '');
    const risk = (priority === 'critical' ? 85 : (priority === 'high' ? 65 : 15)); // Simplified fallback

    // Status Logic 
    let status = 'Pending';
    if (priority === 'critical') status = 'Ongoing';
    if (priority === 'low') status = 'Completed';

    // Estimations
    const { hours, cost } = estimateHoursAndCost(segment, priority);

    return {
        id,
        segment,
        priority,
        risk,
        status,
        center: 'Main St Center', // Mock default
        hours,
        cost
    };
}

function inferSegment(segment, vehicleId = '') {
    if (segment) return segment;
    if ((vehicleId || '').toLowerCase().includes('heavy')) return 'Heavy Duty';
    return 'Light Duty';
}

function estimateHoursAndCost(segment, priority) {
    const PRIORITY_BASE_HOURS = { critical: 6, high: 4.5, medium: 3, low: 1.5 };
    const SEGMENT_MULTIPLIERS = { light: 1, 'light duty': 1, heavy: 1.5, 'heavy duty': 1.5 };
    const HOURLY_RATES = { light: 120, 'light duty': 120, heavy: 160, 'heavy duty': 160 };

    const segKey = (segment || 'light').toLowerCase();
    const priKey = (priority || 'medium').toLowerCase();

    const baseHours = PRIORITY_BASE_HOURS[priKey] || 3;
    const multiplier = SEGMENT_MULTIPLIERS[segKey] || 1;
    const hours = baseHours * multiplier;

    const rate = HOURLY_RATES[segKey] || 120;
    const cost = hours * rate + (hours * 50); // Labor + Parts

    return { hours, cost };
}

// New Helper for Table Prioritization
export function calculateTableRelevance(table) {
    const text = [...(table.headers || []), table.type || ''].join(' ').toLowerCase();
    let score = 0;
    if (text.match(/failure|predict|risk|probability/)) score += 100;
    if (text.match(/vehicle|fleet|health/)) score += 80;
    if (text.match(/schedul|appointment|service/)) score += 60;
    // ... rest of logic
    score += Math.min((table.rows || []).length * 2, 20);
    return score;
}

export function detectTableIcon(table) {
    // ... basic logic or keep strict port
    const type = table.type || '';
    if (type === 'failures') return '⚠️';
    if (type === 'fleet') return '🚗';
    return '📄';
}

export function generateTableTitle(table) {
    const typeMap = {
        'failures': 'Component Risk Analysis',
        'fleet': 'Fleet Health Overview',
        'scheduling': 'Service Scheduling',
        'engagement': 'Customer Engagement',
        'quality': 'Service Quality',
        'kpis': 'Key Metrics'
    };
    return typeMap[table.type] || 'Data Table';
}
