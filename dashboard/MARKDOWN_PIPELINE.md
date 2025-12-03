# 📊 Markdown Pipeline Implementation

## 🎯 Overview

This implementation provides a **complete frontend-only markdown → data pipeline** that converts LLM-generated markdown reports into a fully interactive dashboard with charts, KPIs, and tables.

**Key Features:**
- ✅ **Zero backend modifications** required
- ✅ **Dynamic table classification** (no hardcoded column names)
- ✅ **Flexible regex KPI extraction** (handles formatting variations)
- ✅ **Comprehensive fallback logic** (UI never breaks)
- ✅ **Future-proof** (adapts to LLM output changes)

---

## 🔧 Technologies Used

### Required Libraries (CDN)
All libraries are loaded via CDN in `index.html`:

```html
<!-- Markdown parsing -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<!-- HTML parsing/manipulation (browser build) -->
<script src="https://cdn.jsdelivr.net/npm/cheerio@1.0.0-rc.12/dist/browser/cheerio.min.js"></script>

<!-- Utility functions -->
<script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"></script>

<!-- Charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

---

## 📋 Pipeline Flow

### **Step 1: Fetch Data from Backend**
```javascript
const response = await fetch('/api/dashboard');
const data = await response.json();
// Expected: { report_text: "<markdown>", timestamp: "..." }
```

### **Step 2: Convert Markdown → HTML**
```javascript
const html = marked.parse(report_text);
```
Uses `marked.js` to transform markdown into HTML.

### **Step 3: Load HTML into Cheerio**
```javascript
const $ = cheerio.load(html);
```
Parses HTML using jQuery-like syntax in the browser.

### **Step 4: Extract Tables Dynamically**
```javascript
$('table').each((i, table) => {
  // Extract headers
  const headers = [];
  $(table).find('th').each((j, th) => {
    headers.push($(th).text().trim());
  });
  
  // Extract rows
  const rows = [];
  $(table).find('tr').each((j, tr) => {
    const rowObj = {};
    $(tr).find('td').each((k, td) => {
      rowObj[headers[k]] = $(td).text().trim();
    });
    if (Object.keys(rowObj).length) rows.push(rowObj);
  });
  
  // Classify table
  const tableType = classifyTable(headers);
});
```

### **Step 5: Classify Tables by Header Keywords**
**NO hardcoded column names!** Classification uses **partial keyword matching**:

| Table Type | Keywords in Headers |
|------------|-------------------|
| **Fleet** | `vehicle`, `sensor`, `maintenance`, `priority` |
| **Failures** | `component`, `failure`, `confidence`, `probability` |
| **Engagement** | `engagement`, `method`, `communication`, `channel` |
| **Scheduling** | `appointment`, `service center`, `workload`, `scheduled` |
| **Quality** | `completion`, `satisfaction`, `quality`, `feedback` |
| **KPIs** | `kpi`, `metric`, `current`, `score` |

Example:
```javascript
function classifyTable(headers) {
  const headerText = headers.join(' ').toLowerCase();
  
  if (headerText.includes('vehicle') || headerText.includes('priority')) {
    return 'fleet';
  }
  // ... other classifications
}
```

### **Step 6: Extract KPIs Using Flexible Regex**
Handles variations in formatting (colons, hyphens, en-dashes, spacing):

```javascript
// Fleet Health Score
let match = /Fleet Health Score[\s::\-–—]+([\d.]+)%?/i.exec(md);
if (match) kpis.fleetHealthScore = parseFloat(match[1]);

// Service Center Utilization (handles ranges like "65-85%")
match = /Service Center Utilization[\s::\-–—]+([\d]+)[\s–-]*([\d]*)%?/i.exec(md);
if (match) {
  kpis.serviceCenterUtilization = match[2] ? parseFloat(match[2]) : parseFloat(match[1]);
}
```

**Supported KPIs:**
- Fleet Health Score
- Overall Engagement Rate
- Service Center Utilization
- Customer Satisfaction
- Critical Vehicles
- Average Monthly Usage
- Cost Savings
- Predictive Accuracy

### **Step 7: Build Structured Data Models**
Converts parsed tables + regex KPIs into unified structure:

```javascript
{
  fleet: {
    vehicles: [...],
    total_vehicles: 10,
    critical: 1,
    warning: 2,
    healthy: 7
  },
  failures: {
    predictions: [...]
  },
  engagement: {
    communication_methods: { sms: 45, email: 30, ... }
  },
  scheduling: {
    appointments: [...],
    service_centers: [...]
  },
  quality: { ... },
  kpis: { ... }
}
```

### **Step 8: Render Visualizations**
**5 Dynamic Charts:**

1. **Fleet Health Score Trend** (Line chart - simulated 6-month trend)
2. **Priority Distribution** (Doughnut chart - Critical/Warning/Healthy)
3. **Component Failure Probabilities** (Bar chart - max probability per component)
4. **Service Center Workload** (Horizontal bar - utilization %)
5. **Engagement by Channel** (Bar chart - SMS/Email/App/Call)

All charts use parsed data with fallback to sample data if empty.

### **Step 9: Populate Main Maintenance Table**
**Merges 3 data sources:**

```javascript
const vehicles = fleet.vehicles || [];
const predictions = failures.predictions || [];
const appointments = scheduling.appointments || [];

const rows = vehicles.map(v => {
  const vehicleId = v.vehicle_id || '';
  
  // Match by vehicle ID (case-insensitive)
  const pred = predictions.find(p => 
    (p.vehicle_id || '').toLowerCase() === vehicleId.toLowerCase()
  );
  
  const appt = appointments.find(a => 
    (a.vehicle_id || '').toLowerCase() === vehicleId.toLowerCase()
  );
  
  // Fallback logic for missing data
  const priority = v.priority || (pred ? 'high' : 'low');
  const risk = pred ? pred.failure_probability : (priority === 'critical' ? 85 : 15);
  const date = appt ? appt.scheduled_date : 'Pending';
  
  return { id: vehicleId, priority, risk, date, ... };
});
```

**Columns:**
- Vehicle ID
- Segment (Light/Heavy Duty)
- Priority (Critical/High/Medium/Low badge)
- Failure Risk (% with color-coded progress bar)
- Scheduled Service
- Service Center
- Est. Hours
- Cost Estimate

### **Step 10: Fallback Guarantee**
If **any** parsing step fails:

```javascript
try {
  // Normal pipeline
} catch (error) {
  console.error('Error in markdown pipeline:', error);
  fallbackRender(markdownText); // Still display tables
}
```

**Fallback behavior:**
- Markdown tables rendered as HTML directly
- Charts hidden (no crash)
- KPIs show skeleton state
- **User always sees content**

---

## 🎨 Dynamic Features

### **Flexible Column Matching**
Instead of exact column names, uses fuzzy matching:

```javascript
function findValue(obj, possibleKeys) {
  for (let key of Object.keys(obj)) {
    const lowerKey = key.toLowerCase();
    for (let searchKey of possibleKeys) {
      if (lowerKey.includes(searchKey.toLowerCase())) {
        return obj[key];
      }
    }
  }
  return null;
}

// Usage:
const vehicleId = findValue(row, ['vehicle', 'id', 'vehicle id']);
```

This handles:
- `Vehicle ID` → matches
- `Vehicle` → matches
- `ID` → matches
- `VehicleID` → matches
- Case variations

### **Safe Parsing**
All numeric conversions use safe parsers:

```javascript
function parseFloatSafe(value) {
  if (!value) return 0;
  const num = parseFloat(String(value).replace(/[^0-9.-]/g, ''));
  return isNaN(num) ? 0 : num;
}
```

Handles:
- `"95%"` → `95`
- `"$1,250"` → `1250`
- `""` → `0`
- `null` → `0`

---

## 🔄 Backend API Format

**Expected Response:**
```json
{
  "report_text": "# Fleet Health Report\n\n## KPIs\n...",
  "timestamp": "2024-01-20T15:30:00Z"
}
```

**Legacy Support:**
If `report_text` is missing, falls back to structured JSON format (existing behavior preserved).

---

## 📝 Example Markdown Format

```markdown
# Automotive Predictive Maintenance Report

## Key Performance Indicators

- Fleet Health Score: 95%
- Overall Engagement Rate: 92%
- Service Center Utilization: 65-85%
- Critical Vehicles: 3

## Fleet Health Table

| Vehicle ID | Status | Priority | Sensor Status |
|------------|--------|----------|---------------|
| VEH001 | Healthy | Low | Normal |
| VEH002 | Warning | Medium | Alert |
| VEH004 | Critical | Critical | Failure |

## Failure Predictions

| Vehicle ID | Component | Failure Probability | Confidence | Cost |
|------------|-----------|-------------------|------------|------|
| VEH004 | Engine | 95% | 92% | $45,000 |
| VEH002 | Brake System | 78% | 85% | $12,000 |

## Customer Engagement

| Method | Count | Status |
|--------|-------|--------|
| SMS | 45 | Active |
| Email | 30 | Active |
| App | 20 | Active |
| Voice | 5 | Active |

## Service Scheduling

| Vehicle ID | Service Center | Scheduled Date | Workload % |
|------------|----------------|----------------|------------|
| VEH004 | Mumbai SC | 2024-01-21 | 60% |
| VEH002 | Delhi SC | 2024-01-22 | 80% |
```

---

## 🚀 Running the Dashboard

### **1. Start Backend**
```bash
cd c:\t_thon_latestt\EY_Techathon\dashboard
python app.py
```

### **2. Open Browser**
Navigate to: `http://localhost:5000`

### **3. Backend Must Return**
Endpoint: `GET /api/dashboard`

Response format:
```json
{
  "report_text": "<your markdown here>",
  "timestamp": "2024-01-20T15:30:00Z"
}
```

---

## 🛠️ Debugging

Enable console logging to inspect each pipeline step:

```javascript
console.log('📄 Starting markdown parsing pipeline...');
console.log('✅ Markdown converted to HTML');
console.log('✅ HTML loaded into Cheerio');
console.log('✅ Extracted tables:', tables);
console.log('✅ Extracted KPIs:', kpis);
console.log('✅ Built structured data:', structuredData);
```

Open browser DevTools (F12) and check the Console tab.

---

## ✅ Testing Checklist

- [ ] Markdown successfully parsed to HTML
- [ ] Tables detected and classified correctly
- [ ] KPIs extracted via regex
- [ ] Charts render without errors
- [ ] Main table shows merged data
- [ ] Fallback works when parsing fails
- [ ] No console errors
- [ ] UI remains responsive

---

## 🎯 Benefits

✅ **No Backend Changes** - Pure frontend solution  
✅ **LLM-Friendly** - Adapts to output variations  
✅ **Maintainable** - Clear separation of concerns  
✅ **Robust** - Comprehensive error handling  
✅ **Flexible** - Easy to extend with new table types  
✅ **Fast** - Client-side processing  

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `index.html` | Dashboard structure + CDN imports |
| `script.js` | Complete markdown pipeline implementation |
| `styles.css` | Dashboard styling (unchanged) |

---

## 🔮 Future Enhancements

1. **Custom Table Classifiers** - Add more table types dynamically
2. **Export to PDF** - Generate reports from markdown
3. **Real-time Updates** - WebSocket support for live data
4. **Historical Trends** - Store previous reports for comparison
5. **Advanced Regex** - ML-based entity extraction

---

## 📞 Support

For questions or issues, check:
- Browser console for error messages
- Network tab for API response format
- Markdown structure matches expected format

---

**🎉 Pipeline Complete! Your dashboard now intelligently transforms ANY markdown report into a rich, interactive visualization.**
