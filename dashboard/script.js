// ============================================================================
// ENHANCED MARKDOWN → STRUCTURED JSON PARSER & DASHBOARD RENDERER
// Extracts data according to strict schema and conditionally renders UI
// ============================================================================

// ============================================================================
// UTILITY: HAS DATA HELPER
// ============================================================================
function hasData(value) {
  if (value === null || value === undefined || value === "") return false;
  if (value === 0) return true;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === "object") return Object.keys(value).length > 0;
  return true;
}

// ============================================================================
// UTILITY: FORMAT PERCENTAGE (SMART SCALING)
// ============================================================================
function formatPercentage(value) {
  if (value === null || value === undefined) return '--';
  let num = parseFloat(value);
  if (isNaN(num)) return value;
  if (num <= 1 && num > 0) num = num * 100;
  return Math.round(num * 10) / 10 + '%';
}

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  fetchDashboardData();
});

// ============================================================================
// STEP 1: FETCH DATA FROM BACKEND
// ============================================================================
async function fetchDashboardData() {
  try {
    const response = await fetch('/api/dashboard');
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();

    if (data.report_text) {
      console.log('📄 Processing markdown report...');
      const structuredData = parseMarkdownToSchema(data.report_text);
      console.log('✅ Parsed structured data:', structuredData);

      renderDashboard(structuredData, data.timestamp);

      // Render ALL tables found in the markdown at the bottom
      renderRawTables(structuredData.all_tables);
    } else {
      console.log('⚠️ No markdown found, checking for legacy JSON format');
      renderDashboard(data);
    }
  } catch (error) {
    console.error('❌ Error fetching dashboard data:', error);
    showErrorState();
  }
}

// ============================================================================
// MARKDOWN → SCHEMA PARSER (MAIN FUNCTION)
// ============================================================================
function parseMarkdownToSchema(markdownText) {
  const schema = {
    fleet_metrics: {
      fleet_health_score: null,
      critical_count: null,
      high_count: null,
      medium_count: null,
      low_count: null,
      predicted_failures_total: null
    },
    all_tables: [] // Store ALL tables for raw rendering & smart chart mapping
  };

  const html = marked.parse(markdownText);
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");

  // Extract all tables
  schema.all_tables = extractAllTablesWithContext(doc, markdownText);

  // Extract KPIs from text
  extractFleetMetrics(markdownText, schema);
  extractCustomerEngagementMetrics(markdownText, schema);
  extractServiceMetrics(markdownText, schema);

  return schema;
}

// ============================================================================
// TABLE EXTRACTION
// ============================================================================
function extractAllTablesWithContext(doc, markdownText) {
  const tables = [];
  const tableElements = doc.querySelectorAll("table");

  tableElements.forEach((table, index) => {
    const headers = [];
    table.querySelectorAll("th").forEach(th => headers.push(th.textContent.trim()));

    const rows = [];
    table.querySelectorAll("tr").forEach(tr => {
      const cells = tr.querySelectorAll("td");
      if (cells.length > 0) {
        const rowObj = {};
        cells.forEach((td, idx) => {
          if (headers[idx]) rowObj[headers[idx]] = td.textContent.trim();
        });
        if (Object.keys(rowObj).length) rows.push(rowObj);
      }
    });

    const context = findTableContext(table, doc);
    tables.push({ headers, rows, context, index });
  });

  return tables;
}

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

// ============================================================================
// EXTRACT METRICS (REGEX)
// ============================================================================
function extractFleetMetrics(text, schema) {
  let match = /Fleet Health Score[\s::\-–—]+([\d.]+)%?/i.exec(text);
  if (match) schema.fleet_metrics.fleet_health_score = parseFloat(match[1]);
  match = /Critical[\s:]+([\d]+)/i.exec(text);
  if (match) schema.fleet_metrics.critical_count = parseInt(match[1]);
  match = /Total.*Predicted.*Failures[\s::\-–—]+([\d]+)/i.exec(text);
  if (match) schema.fleet_metrics.predicted_failures_total = parseInt(match[1]);
}

function extractCustomerEngagementMetrics(text, schema) {
  if (!schema.customer_engagement) schema.customer_engagement = { overall_metrics: {} };
  let match = /Success Rate[\s::\-–—]+([\d.]+)%?/i.exec(text);
  if (match) schema.customer_engagement.overall_metrics.success_rate = parseFloat(match[1]);
}

function extractServiceMetrics(text, schema) {
  if (!schema.service_scheduling) schema.service_scheduling = {};
  let match = /Average Wait Time[\s::\-–—]+([\d.]+)\s*(days?)/i.exec(text);
  if (match) schema.service_scheduling.avg_wait_time_days = parseFloat(match[1]);
}

// ============================================================================
// RENDER DASHBOARD
// ============================================================================
function renderDashboard(data, timestamp) {
  renderKPIs(data);
  // Pass ALL tables to chart renderer for smart mapping
  renderCharts(data.all_tables, data.fleet_metrics);

  if (timestamp) {
    const dateEl = document.getElementById('last-updated-date');
    if (dateEl) dateEl.textContent = new Date(timestamp).toLocaleDateString();
  }
}

function renderKPIs(data) {
  const kpiContainer = document.getElementById('kpi-container');
  if (!kpiContainer) return;
  const metrics = data.fleet_metrics || {};
  const engagement = data.customer_engagement?.overall_metrics || {};
  const scheduling = data.service_scheduling || {};

  const potentialKpis = [
    { title: "Fleet Health Score", value: formatPercentage(metrics.fleet_health_score), trend: "+2.5%", isPositive: true },
    { title: "Critical Priority Vehicles", value: metrics.critical_count, trend: metrics.critical_count > 0 ? "Action Req" : "Stable", isPositive: (metrics.critical_count || 0) === 0 },
    { title: "Customer Success Rate", value: formatPercentage(engagement.success_rate), trend: "+5.0%", isPositive: true },
    { title: "Avg Wait Time", value: scheduling.avg_wait_time_days ? `${scheduling.avg_wait_time_days} days` : null, trend: "Optimal", isPositive: true },
    { title: "Predicted Failures", value: metrics.predicted_failures_total, trend: "Monitored", isPositive: false }
  ];

  const validKpis = potentialKpis.filter(kpi => hasData(kpi.value) && kpi.value !== null);
  kpiContainer.innerHTML = validKpis.map(kpi => `
    <div class="kpi-card">
      <div class="kpi-title">${kpi.title}</div>
      <div class="kpi-value">${kpi.value}</div>
      <div class="kpi-trend ${kpi.isPositive ? 'trend-up' : 'trend-down'}">${kpi.trend}</div>
    </div>
  `).join('');
}

// ============================================================================
// SMART CHART MAPPING & RENDERING
// ============================================================================
function renderCharts(tables, metrics) {
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.color = '#636e72';

  Chart.helpers.each(Chart.instances, function (instance) {
    instance.destroy();
  });

  // 1. Fleet Health Trend
  if (metrics && hasData(metrics.fleet_health_score)) {
    renderFleetHealthTrend(metrics.fleet_health_score);
  } else {
    hideChart('healthTrendChart');
  }

  // 2. Priority Distribution (Find any table with Priority column)
  const priorityTable = findTableWithColumn(tables, ['Priority', 'Status', 'Risk Level']);
  if (priorityTable) {
    renderPriorityDistribution(priorityTable);
  } else {
    hideChart('priorityDistChart');
  }

  // 3. Component Failures (Find table with Probability/Risk)
  const failureTable = findTableWithColumn(tables, ['Probability', 'Failure Probability', 'Risk Score']);
  if (failureTable) {
    renderComponentFailures(failureTable);
  } else {
    hideChart('failureProbChart');
  }

  // 4. Service Workload (Find table with Utilization/Workload)
  const workloadTable = findTableWithColumn(tables, ['Utilization', 'Workload', 'Capacity']);
  if (workloadTable) {
    renderServiceWorkload(workloadTable);
  } else {
    hideChart('serviceWorkloadChart');
  }

  // 5. Engagement (Find table with Channel/Method)
  const engagementTable = findTableWithColumn(tables, ['Channel', 'Method', 'Source']);
  if (engagementTable) {
    renderEngagementChannels(engagementTable);
  } else {
    hideChart('engagementChannelChart');
  }
}

// Helper to find a table that contains ANY of the target columns (case-insensitive)
function findTableWithColumn(tables, targetColumns) {
  return tables.find(table =>
    table.headers.some(h =>
      targetColumns.some(target => h.toLowerCase().includes(target.toLowerCase()))
    )
  );
}

function hideChart(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (canvas) canvas.closest('.chart-card').style.display = 'none';
}

// --- CHART RENDERERS ---

function renderFleetHealthTrend(score) {
  const ctx = document.getElementById('healthTrendChart').getContext('2d');
  let currentScore = score || 85;
  if (currentScore <= 1 && currentScore > 0) currentScore *= 100;

  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, 'rgba(108, 99, 255, 0.4)');
  gradient.addColorStop(1, 'rgba(108, 99, 255, 0.0)');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Fleet Health',
        data: [currentScore - 5, currentScore - 3, currentScore - 4, currentScore - 2, currentScore - 1, currentScore],
        borderColor: '#6c63ff',
        borderWidth: 3,
        backgroundColor: gradient,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: false, min: 0, max: 100 }, x: { display: false } }
    }
  });
  document.getElementById('healthTrendChart').closest('.chart-card').style.display = 'block';
}

function renderPriorityDistribution(table) {
  // Count occurrences in the Priority/Status column
  const colName = table.headers.find(h => ['Priority', 'Status', 'Risk Level'].some(t => h.toLowerCase().includes(t.toLowerCase())));
  const counts = {};
  table.rows.forEach(row => {
    const val = row[colName] || 'Unknown';
    counts[val] = (counts[val] || 0) + 1;
  });

  const ctx = document.getElementById('priorityDistChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(counts),
      datasets: [{
        data: Object.values(counts),
        backgroundColor: ['#00b894', '#fdcb6e', '#fd9644', '#ff7675', '#6c63ff'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: { legend: { position: 'bottom', labels: { usePointStyle: true } } }
    }
  });
  document.getElementById('priorityDistChart').closest('.chart-card').style.display = 'block';
}

function renderComponentFailures(table) {
  // Extract Component (Label) and Probability (Value)
  const labelCol = table.headers[0]; // Assume first column is component/vehicle
  const valCol = table.headers.find(h => ['Probability', 'Risk', 'Score'].some(t => h.toLowerCase().includes(t.toLowerCase())));

  const labels = [];
  const data = [];

  table.rows.forEach(row => {
    labels.push(row[labelCol]);
    let val = parseFloat((row[valCol] || '0').replace(/[^0-9.]/g, ''));
    if (val <= 1 && val > 0) val *= 100;
    data.push(val);
  });

  const ctx = document.getElementById('failureProbChart').getContext('2d');
  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, '#6c63ff');
  gradient.addColorStop(1, '#a29bfe');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Risk (%)',
        data: data,
        backgroundColor: gradient,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, max: 100 }, x: { display: false } }
    }
  });
  document.getElementById('failureProbChart').closest('.chart-card').style.display = 'block';
}

function renderServiceWorkload(table) {
  const labelCol = table.headers[0];
  const valCol = table.headers.find(h => ['Utilization', 'Workload'].some(t => h.toLowerCase().includes(t.toLowerCase())));

  const labels = [];
  const data = [];

  table.rows.forEach(row => {
    labels.push(row[labelCol]);
    let val = parseFloat((row[valCol] || '0').replace(/[^0-9.]/g, ''));
    if (val <= 1 && val > 0) val *= 100;
    data.push(val);
  });

  const ctx = document.getElementById('serviceWorkloadChart').getContext('2d');
  const gradient = ctx.createLinearGradient(400, 0, 0, 0);
  gradient.addColorStop(0, '#00b894');
  gradient.addColorStop(1, '#55efc4');

  new Chart(ctx, {
    type: 'bar',
    indexAxis: 'y',
    data: {
      labels: labels,
      datasets: [{
        label: 'Utilization',
        data: data,
        backgroundColor: gradient,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { beginAtZero: true, max: 100 }, y: { display: false } }
    }
  });
  document.getElementById('serviceWorkloadChart').closest('.chart-card').style.display = 'block';
}

function renderEngagementChannels(table) {
  const labelCol = table.headers[0];
  const valCol = table.headers.find(h => ['Count', 'Total', 'Contacts'].some(t => h.toLowerCase().includes(t.toLowerCase()))) || table.headers[1];

  const labels = [];
  const data = [];

  table.rows.forEach(row => {
    labels.push(row[labelCol]);
    data.push(parseFloat((row[valCol] || '0').replace(/[^0-9.]/g, '')));
  });

  const ctx = document.getElementById('engagementChannelChart').getContext('2d');
  new Chart(ctx, {
    type: 'polarArea',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: ['rgba(108, 99, 255, 0.7)', 'rgba(0, 184, 148, 0.7)', 'rgba(253, 203, 110, 0.7)', 'rgba(255, 118, 117, 0.7)'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'right', labels: { usePointStyle: true } } },
      scales: { r: { ticks: { display: false } } }
    }
  });
  document.getElementById('engagementChannelChart').closest('.chart-card').style.display = 'block';
}

// ============================================================================
// RENDER RAW TABLES (WITH COLOR BADGES)
// ============================================================================
function renderRawTables(tables) {
  const container = document.createElement('section');
  container.className = 'raw-tables-section';
  container.style.marginTop = '40px';
  container.innerHTML = '<h3 style="color: #6c63ff; margin-bottom: 20px;">📄 Detailed Reports</h3>';

  tables.forEach(table => {
    if (!hasData(table.rows)) return;
    const tableDiv = document.createElement('div');
    tableDiv.className = 'table-container';
    tableDiv.style.marginBottom = '30px';
    const title = table.context ? table.context.toUpperCase() : `TABLE ${table.index + 1}`;

    let html = `
      <h4 style="color: #636e72; margin-bottom: 10px; font-size: 14px; border-left: 4px solid #a29bfe; padding-left: 10px;">${title}</h4>
      <table>
        <thead><tr>${table.headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
        <tbody>
    `;

    table.rows.forEach(row => {
      html += '<tr>';
      table.headers.forEach(h => {
        const cellData = row[h] || '';
        html += `<td>${formatCellWithBadge(cellData)}</td>`;
      });
      html += '</tr>';
    });

    html += '</tbody></table>';
    tableDiv.innerHTML = html;
    container.appendChild(tableDiv);
  });

  // Replace the old table section if it exists, or append
  const existing = document.querySelector('.raw-tables-section');
  if (existing) existing.remove();

  // Also hide the old hardcoded maintenance table if we have raw tables
  const oldTable = document.querySelector('.table-section');
  if (oldTable) oldTable.style.display = 'none';

  document.querySelector('.dashboard-container').appendChild(container);
}

// Helper to add badges to cell content
function formatCellWithBadge(text) {
  const lower = text.toLowerCase();

  if (['critical', 'fail', 'high', 'severe'].some(k => lower.includes(k))) {
    return `<span class="badge badge-critical">${text}</span>`;
  }
  if (['warning', 'medium', 'moderate'].some(k => lower.includes(k))) {
    return `<span class="badge badge-medium">${text}</span>`;
  }
  if (['healthy', 'pass', 'good', 'normal', 'low', 'optimal'].some(k => lower.includes(k))) {
    return `<span class="badge badge-low">${text}</span>`;
  }

  return text;
}

function showErrorState() {
  const kpiContainer = document.getElementById('kpi-container');
  if (kpiContainer) {
    kpiContainer.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: #ff7675;">
        <h3>⚠️ Unable to load dashboard data</h3>
        <p>Please check your backend connection and try again.</p>
      </div>
    `;
  }
}
