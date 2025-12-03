# 📊 Schema-Based Markdown Parser Documentation

## 🎯 Overview

This enhanced parser extracts data from CrewAI-generated markdown reports and maps it to a **strict JSON schema** without hallucination. It uses context-aware table classification and flexible regex patterns to handle variations in LLM output.

---

## 🏗️ Architecture

```
Markdown Report (from CrewAI)
    ↓
marked.js → HTML
    ↓
DOMParser → DOM
    ↓
Context-Aware Table Extraction
    ↓
Schema Mapping (NO HALLUCINATION)
    ↓
Structured JSON Output
```

---

## 📋 Complete JSON Schema

```javascript
{
  "fleet_metrics": {
    "fleet_health_score": number | null,
    "critical_count": number | null,
    "high_count": number | null,
    "medium_count": number | null,
    "low_count": number | null,
    "predicted_failures_total": number | null,
    "sensor_highlights": object
  },

  "fleet_health_table": array,  // Fleet status for all vehicles

  "system_monitoring": {
    "brake_system": array,
    "transmission_system": array,
    "engine_control_system": array,
    "cooling_system": array
  },

  "failure_prediction": {
    "vehicle_predictions": array,  // Component-level predictions
    "total_predicted_failures": number | null
  },

  "root_cause_analysis": {
    "brake_system": array,
    "transmission": array,
    "engine_control": array,
    "cooling_system": array
  },

  "customer_engagement": {
    "overall_metrics": {
      "success_rate": number | null,
      "response_rate": number | null,
      "avg_response_time_hours": number | null,
      "engagement_effectiveness_score": number | null
    },
    "channel_performance": array,
    "per_vehicle_engagement": array
  },

  "service_scheduling": {
    "appointments": array,
    "utilization": array,
    "avg_wait_time_days": number | null,
    "emergency_appointments": number | null
  },

  "technician_operations": {
    "technicians": array,
    "utilization_summary": number | null
  },

  "service_execution": {
    "ongoing_services": array,
    "service_quality_metrics": array,
    "projected_feedback": array
  },

  "manufacturing_quality": {
    "defect_patterns": array,
    "batch_correlations": array,
    "supplier_quality": array,
    "rca_summary": array,
    "capa_recommendations": array
  },

  "business_intelligence": {
    "roi": number | null,
    "payback_period_months": number | null,
    "year_1_savings": number | null,
    "immediate_repair_costs": number | null,
    "long_term_investment": number | null,
    "npv_5_year": number | null
  },

  "workflow_status": array,
  "ueba_events": array
}
```

---

## 🔍 How It Works

### 1. Context-Aware Table Classification

The parser doesn't just look at table headers - it also examines the **heading above the table** to understand context:

```javascript
function findTableContext(tableElement, doc) {
  let currentNode = tableElement.previousElementSibling;
  
  while (currentNode) {
    if (['h1', 'h2', 'h3', 'h4'].includes(currentNode.tagName.toLowerCase())) {
      return currentNode.textContent.trim().toLowerCase();
    }
    currentNode = currentNode.previousElementSibling;
  }
  return '';
}
```

**Example:**
```markdown
## Brake System Monitoring

| Vehicle ID | Brake Status | Pad Thickness |
|------------|--------------|---------------|
| VEH001     | Good         | 8.5mm         |
```

The parser sees "Brake System Monitoring" heading → classifies table as `system_monitoring_brake`.

### 2. Flexible Table Classification

Uses both **header keywords** and **context** for robust classification:

| Schema Field | Header Keywords | Context Keywords |
|-------------|----------------|------------------|
| `fleet_health_table` | vehicle, status, priority, health | fleet health, vehicle status |
| `system_monitoring_brake` | brake, pad, thickness | brake system, brake monitoring |
| `failure_prediction` | failure, prediction, probability, component | failure prediction, predictive analysis |
| `engagement_channels` | channel, method, communication | customer engagement |
| `scheduling_appointments` | appointment, scheduled, service center | service scheduling, appointments |

**Example Classification Logic:**
```javascript
function classifyTableAdvanced(headers, context, rows) {
  const headerText = headers.join(' ').toLowerCase();
  const contextText = context.toLowerCase();

  // Fleet Health Table
  if (matchesKeywords(headerText, ['vehicle', 'status', 'priority']) ||
      matchesKeywords(contextText, ['fleet health'])) {
    return 'fleet_health';
  }

  // System Monitoring - Brake
  if (matchesKeywords(contextText, ['brake system', 'brake monitoring'])) {
    return 'system_monitoring_brake';
  }
  
  // ... more classifications
}
```

### 3. NO HALLUCINATION Rule

**Golden Rule:** If data doesn't exist in markdown → set to `null` or `[]`

```javascript
// Initialize with nulls/empty arrays
const schema = {
  fleet_metrics: {
    fleet_health_score: null,  // Will stay null if not found
    critical_count: null,
    // ...
  }
};

// Only set if found
let match = /Fleet Health Score[\s::\-–—]+([\d.]+)%?/i.exec(text);
if (match) schema.fleet_metrics.fleet_health_score = parseFloat(match[1]);
// Otherwise stays null - NO DEFAULT VALUE
```

### 4. Flexible Regex Extraction

Handles multiple formatting variations:

```javascript
// Matches ALL of these:
// - "Fleet Health Score: 85%"
// - "Fleet Health Score - 85%"
// - "Fleet Health Score – 85%" (en-dash)
// - "Fleet Health Score  :  85%"
/Fleet Health Score[\s::\-–—]+([\d.]+)%?/i

// Handles ranges:
// - "Service Utilization: 65-85%"
// - "Service Utilization: 75%"
/Service Center Utilization[\s::\-–—]+([\d]+)[\s–-]*([\d]*)%?/i
```

### 5. Smart Value Extraction

Cleans and parses values safely:

```javascript
// Extract cost with commas: "$45,000" → 45000
match = /Year 1 Savings?[\s::\-–—]+\$?([\d,]+)/i.exec(text);
if (match) {
  schema.business_intelligence.year_1_savings = parseFloat(match[1].replace(/,/g, ''));
}

// Extract percentage: "85%" → 85
const probStr= p['Failure Probability'] || '0';
const prob = parseFloat(String(probStr).replace(/[^0-9.]/g, ''));
```

---

## 📊 Extraction Examples

### Example 1: Fleet Metrics

**Markdown:**
```markdown
## Executive Summary

- Fleet Health Score: 85%
- Critical Vehicles: 3
- Total Predicted Failures: 15
```

**Extracted:**
```json
{
  "fleet_metrics": {
    "fleet_health_score": 85,
    "critical_count": 3,
    "predicted_failures_total": 15,
    // ... rest null
  }
}
```

### Example 2: Fleet Health Table

**Markdown:**
```markdown
## Fleet Health Analysis

| Vehicle ID | Status | Priority | Sensor Status |
|------------|--------|----------|---------------|
| VEH001 | Healthy | Low | Normal |
| VEH004 | Critical | Critical | Multiple Failures |
| VEH007 | Warning | High | Engine Alert |
```

**Extracted:**
```json
{
  "fleet_health_table": [
    { "Vehicle ID": "VEH001", "Status": "Healthy", "Priority": "Low", "Sensor Status": "Normal" },
    { "Vehicle ID": "VEH004", "Status": "Critical", "Priority": "Critical", "Sensor Status": "Multiple Failures" },
    { "Vehicle ID": "VEH007", "Status": "Warning", "Priority": "High", "Sensor Status": "Engine Alert" }
  ],
  "fleet_metrics": {
    "critical_count": 1,  // Auto-counted from table
    "high_count": 1,
    "low_count": 1
  }
}
```

### Example 3: Customer Engagement

**Markdown:**
```markdown
## Customer Engagement Analysis

- Success Rate: 87.5%
- Response Rate: 92%
- Average Response Time: 4.2 hours

### Channel Performance

| Channel | Contacts | Success Rate |
|---------|----------|--------------|
| SMS | 45 | 85% |
| Email | 30 | 70% |
| App | 20 | 95% |
```

**Extracted:**
```json
{
  "customer_engagement": {
    "overall_metrics": {
      "success_rate": 87.5,
      "response_rate": 92,
      "avg_response_time_hours": 4.2,
      "engagement_effectiveness_score": null
    },
    "channel_performance": [
      { "Channel": "SMS", "Contacts": "45", "Success Rate": "85%" },
      { "Channel": "Email", "Contacts": "30", "Success Rate": "70%" },
      { "Channel": "App", "Contacts": "20", "Success Rate": "95%" }
    ]
  }
}
```

### Example 4: Business Intelligence

**Markdown:**
```markdown
## Financial Analysis

- ROI: 256%
- Payback Period: 8.5 months
- Year 1 Savings: $240,000
- Immediate Repair Costs: $93,500
- NPV (5-year): $1,250,000
```

**Extracted:**
```json
{
  "business_intelligence": {
    "roi": 256,
    "payback_period_months": 8.5,
    "year_1_savings": 240000,
    "immediate_repair_costs": 93500,
    "long_term_investment": null,
    "npv_5_year": 1250000
  }
}
```

---

## 🎯 Classification Matrix

| Table Type | Schema Path | Detection Method |
|-----------|-------------|------------------|
| Fleet Status | `fleet_health_table` | Headers: vehicle, status, priority |
| Brake Monitoring | `system_monitoring.brake_system` | Context: "brake system" |
| Transmission | `system_monitoring.transmission_system` | Context: "transmission" |
| Engine Control | `system_monitoring.engine_control_system` | Context: "engine control" |
| Cooling System | `system_monitoring.cooling_system` | Context: "cooling system" |
| Failure Predictions | `failure_prediction.vehicle_predictions` | Headers: failure, probability, component |
| RCA - Brake | `root_cause_analysis.brake_system` | Context: "root cause" + "brake" |
| RCA - Transmission | `root_cause_analysis.transmission` | Context: "root cause" + "transmission" |
| Engagement Channels | `customer_engagement.channel_performance` | Headers: channel, method |
| Engagement by Vehicle | `customer_engagement.per_vehicle_engagement` | Context: "customer engagement" |
| Appointments | `service_scheduling.appointments` | Headers: appointment, scheduled |
| Center Utilization | `service_scheduling.utilization` | Headers: utilization, capacity |
| Technicians | `technician_operations.technicians` | Headers: technician, mechanic |
| Ongoing Services | `service_execution.ongoing_services` | Context: "ongoing service" |
| Service Quality | `service_execution.service_quality_metrics` | Context: "service quality" |
| Feedback | `service_execution.projected_feedback` | Context: "feedback" |
| Defect Patterns | `manufacturing_quality.defect_patterns` | Context: "defect pattern" |
| Batch Data | `manufacturing_quality.batch_correlations` | Context: "batch" |
| Supplier Quality | `manufacturing_quality.supplier_quality` | Context: "supplier quality" |
| CAPA | `manufacturing_quality.capa_recommendations` | Context: "capa", "corrective action" |
| Workflow | `workflow_status` | Context: "workflow" |
| UEBA | `ueba_events` | Context: "ueba", "security" |

---

## ⚙️ Configuration

### Adding New Table Types

1. **Add to schema initialization:**
```javascript
const schema = {
  // ... existing fields
  your_new_field: []  // or null for single values
};
```

2. **Add classification logic:**
```javascript
function classifyTableAdvanced(headers, context, rows) {
  // ... existing logic
  
  if (matchesKeywords(contextText, ['your keyword'])) {
    return 'your_classification';
  }
}
```

3. **Add mapping logic:**
```javascript
function mapTableToSchema(table, schema) {
  switch (classification) {
    // ... existing cases
    
    case 'your_classification':
      schema.your_new_field = rows;
      break;
  }
}
```

### Adding New Metrics

Add regex extraction in appropriate function:

```javascript
function extractYourMetrics(text, schema) {
  let match = /Your Metric[\s::\-–—]+([\d.]+)/i.exec(text);
  if (match) schema.your_section.your_metric = parseFloat(match[1]);
}
```

---

## 🐛 Debugging

### Enable Detailed Logging

The parser logs each step:

```javascript
console.log('🔄 Starting schema-based parsing...');
console.log('📊 Found ${tables.length} tables');
console.log('✅ Schema parsing complete');
```

**Check Console (F12) for:**
- Tables found and classified
- KPIs extracted
- Final schema structure

### Verify Schema Output

Add this after parsing:

```javascript
const structuredData = parseMarkdownToSchema(markdownText);
console.log('📋 Final Schema:', JSON.stringify(structuredData, null, 2));
```

### Common Issues

**Issue: Table not classified correctly**
- Check context heading above table
- Verify header keywords match classification logic
- Add console.log in `classifyTableAdvanced()`

**Issue: Metric extracted as null**
- Check regex pattern matches your markdown format
- Test regex at https://regex101.com/
- Verify metric exists in markdown

**Issue: Values parsed incorrectly**
- Check for commas, currency symbols, percentages
- Use `.replace(/[^0-9.]/g, '')` to clean

---

## ✅ Validation Rules

1. **Never hallucinate** - If not in markdown → null/[]
2. **Preserve original values** - No rounding unless necessary
3. **Match schema exactly** - Field names must match
4. **Type safety** - Numbers are numbers, arrays are arrays
5. **Context awareness** - Use both headers and context

---

## 🚀 Usage

### In Dashboard

```javascript
// Fetch from backend
const response = await fetch('/api/dashboard');
const data = await response.json();

if (data.report_text) {
  // Parse markdown → schema
  const structured = parseMarkdownToSchema(data.report_text);
  
  // Render dashboard
  renderDashboard(structured, data.timestamp);
}
```

### Standalone Testing

```javascript
const markdown = `
# Fleet Report

- Fleet Health Score: 85%

| Vehicle ID | Status |
|------------|--------|
| VEH001 | Healthy |
`;

const schema = parseMarkdownToSchema(markdown);
console.log(schema.fleet_metrics.fleet_health_score);  // 85
console.log(schema.fleet_health_table);  // [{ "Vehicle ID": "VEH001", "Status": "Healthy" }]
```

---

## 📦 Dependencies

- **marked.js** - Markdown → HTML conversion
- **DOMParser** - Native browser API (no CDN needed)
- **Chart.js** - Visualization (separate concern)

**No additional libraries needed!**

---

## 🎉 Summary

This parser provides:

✅ **Schema compliance** - Exact JSON structure  
✅ **Zero hallucination** - null/[] for missing data  
✅ **Context awareness** - Smart table classification  
✅ **Flexibility** - Handles LLM output variations  
✅ **Type safety** - Proper number/string/array types  
✅ **Maintainability** - Clear, documented code  

**Backend unchanged. CrewAI unchanged. Pure frontend solution.**
