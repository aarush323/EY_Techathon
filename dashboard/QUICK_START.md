# 🚀 Quick Start Guide

## 📦 What Was Implemented

A **complete frontend markdown parsing pipeline** that converts LLM-generated markdown reports into interactive dashboards.

---

## 📁 Files Changed

### Modified
- ✅ `index.html` - Added marked.js, cheerio, lodash CDN scripts
- ✅ `script.js` - Complete pipeline implementation (replaced old code)

### Created
- 📄 `MARKDOWN_PIPELINE.md` - Full documentation
- 📄 `IMPLEMENTATION_SUMMARY.md` - Complete feature summary
- 📄 `sample-markdown-report.md` - Example markdown format
- 📄 `test-pipeline.html` - Interactive debugging tool
- 📄 `test-markdown-response.json` - Sample backend response

### Unchanged
- ⚪ `styles.css` - No changes
- ⚪ `app.py` - No changes (backend untouched)
- ⚪ CrewAI files - No changes

---

## 🎯 How to Use

### Step 1: Generate Report (Backend)
```bash
cd c:\t_thon_latestt\EY_Techathon
python src/systemm/main.py run
```

This creates `src/systemm/crew_report.json` with:
```json
{
  "report_text": "<markdown content>",
  "timestamp": "2024-12-03T..."
}
```

### Step 2: Start Dashboard
```bash
cd c:\t_thon_latestt\EY_Techathon\dashboard
python app.py
```

### Step 3: View Dashboard
Open browser: `http://localhost:5000`

**The pipeline automatically:**
1. Fetches data from `/api/dashboard`
2. Parses markdown → HTML
3. Extracts tables and KPIs
4. Renders charts and tables

---

## 🧪 Testing Without Backend

Open `test-pipeline.html` in any browser:
```
file:///c:/t_thon_latestt/EY_Techathon/dashboard/test-pipeline.html
```

1. Click "Load Sample Markdown"
2. Click "Run Full Pipeline"
3. See parsed data in output

---

## 📊 Expected Backend Response

Your backend must return:
```json
{
  "report_text": "# Report\n\n## KPIs\n- Fleet Health: 85%\n...",
  "timestamp": "2024-12-03T23:14:10+05:30"
}
```

**Current backend (`app.py`)** already does this! ✅

---

## 🔍 Debugging

### Check Console Logs
Open DevTools (F12) → Console tab

Look for:
```
📄 Starting markdown parsing pipeline...
✅ Markdown converted to HTML
✅ HTML loaded into Cheerio
✅ Extracted tables: [...]
✅ Extracted KPIs: {...}
✅ Built structured data: {...}
```

### Common Issues

#### Issue: "No markdown found"
**Solution:** Backend not returning `report_text` field
- Run `python src/systemm/main.py run` first
- Check `src/systemm/crew_report.json` exists

#### Issue: Charts not showing
**Solution:** Check browser console for errors
- Verify Chart.js loaded
- Check data format

#### Issue: Tables empty
**Solution:** Markdown tables not detected
- Check markdown has proper table syntax
- Use test page to debug

---

## 📋 Markdown Format

Your markdown should include:

### KPIs (regex extracted)
```markdown
- Fleet Health Score: 85%
- Overall Engagement Rate: 92%
- Service Center Utilization: 65-85%
```

### Tables (cheerio extracted)
```markdown
## Fleet Table
| Vehicle ID | Status | Priority |
|------------|--------|----------|
| VEH001 | Healthy | Low |

## Failure Predictions
| Vehicle ID | Component | Failure Probability |
|------------|-----------|---------------------|
| VEH004 | Engine | 95% |
```

**See `sample-markdown-report.md` for complete example.**

---

## 🎨 What You Get

### 5 KPI Cards
- Fleet Health Score
- Critical Priority Vehicles
- Avg Monthly Usage
- Service Center Utilization
- Customer Engagement Rate

### 5 Charts
1. **Fleet Health Trend** (Line)
2. **Priority Distribution** (Doughnut)
3. **Component Failures** (Bar)
4. **Service Workload** (Horizontal Bar)
5. **Engagement Channels** (Bar)

### 1 Main Table
- Vehicle ID, Segment, Priority
- Failure Risk % (with progress bar)
- Scheduled Service, Center
- Est. Hours, Cost

---

## ✅ Verification Checklist

After implementation, verify:

- [ ] Open `http://localhost:5000`
- [ ] See 5 KPI cards with values
- [ ] See 5 charts rendering
- [ ] See maintenance table with data
- [ ] No errors in console
- [ ] Timestamp shows current date

---

## 🔧 Customization

### Add New Table Type
Edit `script.js` → `classifyTable()`:
```javascript
if (headerText.includes('your_keyword')) {
  return 'your_type';
}
```

### Add New KPI
Edit `script.js` → `extractKPIsFromMarkdown()`:
```javascript
match = /Your KPI[\s::\-–—]+([\d.]+)%?/i.exec(md);
if (match) kpis.yourKPI = parseFloat(match[1]);
```

### Add New Chart
Edit `script.js` → Add function in `renderCharts()`:
```javascript
function renderYourChart(data) {
  const ctx = document.getElementById('yourChart').getContext('2d');
  new Chart(ctx, { /* config */ });
}
```

---

## 📚 Documentation

- **`MARKDOWN_PIPELINE.md`** - Technical architecture
- **`IMPLEMENTATION_SUMMARY.md`** - Complete features
- **`sample-markdown-report.md`** - Example format
- **This file** - Quick reference

---

## 🎉 You're Done!

The pipeline is **fully implemented** and ready to use.

**No backend changes needed.**  
**No CrewAI changes needed.**  
**Just generate markdown and it works!**

---

## 📞 Need Help?

1. **Check console logs** (F12)
2. **Use test page** (`test-pipeline.html`)
3. **Review sample markdown** (`sample-markdown-report.md`)
4. **Read full docs** (`MARKDOWN_PIPELINE.md`)

---

**Happy Dashboard Building! 🚀**
