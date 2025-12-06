// ============================================================================
// MAIN ENTRY POINT
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  fetchDashboardData();
});

// ============================================================================
// DATA FETCHING
// ============================================================================
async function fetchDashboardData() {
  try {
    const response = await fetch('/api/dashboard');
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();

    if (data.report_text) {
      processMarkdownPipeline(data.report_text, data.timestamp);
    } else {
      console.log('No markdown found, using legacy JSON format');
      routePageRendering(data);
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
}

// ============================================================================
// MARKDOWN PIPELINE
// ============================================================================
function processMarkdownPipeline(markdownText, timestamp) {
  try {
    const html = marked.parse(markdownText);
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    // Extract structured data
    const tables = extractAllTables(doc);
    const kpis = extractKPIsFromMarkdown(markdownText);
    const sections = extractAllMarkdownSections(doc);

    const structuredData = buildDataModels(tables, kpis);
    structuredData.markdown = sections;

    routePageRendering(structuredData, timestamp);

  } catch (error) {
    console.error('❌ Error in markdown pipeline:', error);
  }
}

// ============================================================================
// DYNAMIC MARKDOWN PARSER
// ============================================================================
function extractAllMarkdownSections(doc) {
  const sections = {};
  let currentSection = "Introduction";

  doc.body.childNodes.forEach(node => {
    if (node.nodeType !== Node.ELEMENT_NODE) return;

    if (/^H[1-6]$/.test(node.tagName)) {
      currentSection = node.textContent.trim();
      if (!sections[currentSection]) sections[currentSection] = [];
    } else {
      if (!sections[currentSection]) sections[currentSection] = [];

      if (node.tagName === 'UL' || node.tagName === 'OL') {
        const items = Array.from(node.children).map(li => li.innerHTML);
        sections[currentSection].push({ type: 'list', items: items, tag: node.tagName });
      } else if (node.tagName === 'TABLE') {
        sections[currentSection].push({ type: 'table', html: node.outerHTML });
      } else if (node.tagName === 'P') {
        const text = node.textContent.trim();
        if (text) sections[currentSection].push({ type: 'text', content: node.innerHTML });
      } else {
        sections[currentSection].push({ type: 'html', content: node.outerHTML });
      }
    }
  });

  return sections;
}

// ============================================================================
// ROUTING & RENDERING
// ============================================================================
function routePageRendering(data, timestamp) {
  const path = window.location.pathname;
  let page = path.split("/").pop();

  // Normalize: handle both /page and /page.html
  if (!page || page === '/') page = 'index.html';
  if (!page.endsWith('.html')) page += '.html';

  const dateEl = document.getElementById('last-updated-date');
  if (dateEl && timestamp) {
    dateEl.textContent = new Date(timestamp).toLocaleDateString();
  }

  // Navbar Active State
  document.querySelectorAll('nav a').forEach(link => {
    const href = link.getAttribute('href');
    const linkPage = href.split('/').pop();

    // Match both /page and /page.html or index
    if (linkPage === page ||
      (page === 'index.html' && (href === '/' || linkPage === 'index.html')) ||
      linkPage.replace('.html', '') === page.replace('.html', '')) {
      link.classList.add('border-black', 'text-gray-900');
      link.classList.remove('border-transparent', 'text-gray-500');
    } else {
      link.classList.remove('border-black', 'text-gray-900');
      link.classList.add('border-transparent', 'text-gray-500');
    }
  });

  // Route to appropriate renderer
  if (page === 'index.html') {
    renderOverviewPage(data);
  } else if (page === 'fleet_health.html') {
    renderFleetHealthPage(data);
  } else if (page === 'failure_predictions.html') {
    renderFailurePredictionsPage(data);
  } else if (page === 'customer_engagement.html') {
    renderCustomerEngagementPage(data);
  } else if (page === 'service_scheduling.html') {
    renderServiceSchedulingPage(data);
  } else if (page === 'service_quality.html') {
    renderServiceQualityPage(data);
  } else if (page === 'manufacturing_quality.html') {
    renderManufacturingQualityPage(data);
  }
}

// ============================================================================
// PAGE RENDERERS
// ============================================================================

// 1. OVERVIEW PAGE
function renderOverviewPage(data) {
  renderKPIs(data);
  // Charts removed from Overview

  renderMaintenanceTableSummary(data);

  if (data.markdown) {
    renderMarkdownSections(data.markdown);
  } else {
    renderLegacyRecommendations(data);
  }

  setText('total-savings', `$${formatCurrency(data.kpis.costSavings || 240000)}`);
  setText('roi-multiplier', '3.5x');
  setText('prevented-costs', `$${formatCurrency((data.kpis.costSavings || 240000) * 0.6)}`);
  setText('mtbf-val', '450 hrs');
  setText('mttr-val', '4.2 hrs');
  setText('availability-val', '96.5%');
}

function renderMarkdownSections(sections) {
  const recContainer = document.getElementById('recommendations-container');
  if (recContainer) {
    const recKeys = Object.keys(sections).filter(k =>
      k.toLowerCase().includes('recommendation') ||
      k.toLowerCase().includes('action') ||
      k.toLowerCase().includes('priority')
    );

    if (recKeys.length > 0) {
      recContainer.innerHTML = '';
      recKeys.forEach(key => {
        const content = sections[key];
        content.forEach(block => {
          if (block.type === 'list') {
            block.items.forEach(item => {
              recContainer.innerHTML += `
                <div class="flex items-start space-x-3 mb-2">
                  <div class="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></div>
                  <div class="text-sm text-gray-600">${item}</div>
                </div>
              `;
            });
          } else if (block.type === 'text') {
            recContainer.innerHTML += `<p class="text-sm text-gray-600 mb-2">${block.content}</p>`;
          }
        });
      });
    }
  }

  let dynamicContainer = document.getElementById('dynamic-sections-container');
  if (!dynamicContainer) {
    const recSection = document.querySelector('section.grid.grid-cols-1.lg\\:grid-cols-2');
    if (recSection && recSection.parentNode) {
      dynamicContainer = document.createElement('section');
      dynamicContainer.id = 'dynamic-sections-container';
      dynamicContainer.className = 'grid grid-cols-1 gap-6 mb-8';
      recSection.parentNode.insertBefore(dynamicContainer, recSection.nextSibling);
    }
  }

  if (dynamicContainer) {
    dynamicContainer.innerHTML = '';

    const excludeKeys = ['fleet health', 'quality', 'scheduling', 'engagement', 'predictions', 'recommendation', 'action', 'priority'];

    Object.keys(sections).forEach(title => {
      if (excludeKeys.some(ex => title.toLowerCase().includes(ex))) return;
      if (title === 'Introduction') return;

      const contentBlocks = sections[title];
      if (!contentBlocks || contentBlocks.length === 0) return;

      const card = document.createElement('div');
      card.className = 'bg-white p-6 rounded-xl shadow-sm border border-gray-100';

      let html = `<h3 class="text-lg font-semibold text-gray-900 mb-4">${title}</h3>`;

      contentBlocks.forEach(block => {
        if (block.type === 'text') {
          html += `<p class="text-sm text-gray-600 mb-3">${block.content}</p>`;
        } else if (block.type === 'list') {
          html += `<ul class="space-y-2 mb-3">`;
          block.items.forEach(item => {
            html += `
              <li class="flex items-start">
                <span class="flex-shrink-0 h-1.5 w-1.5 rounded-full bg-gray-400 mt-2 mr-2"></span>
                <span class="text-sm text-gray-600">${item}</span>
              </li>`;
          });
          html += `</ul>`;
        } else if (block.type === 'table') {
          html += `<div class="overflow-x-auto mb-3"><div class="text-sm text-gray-600">${block.html}</div></div>`;
        }
      });

      card.innerHTML = html;
      dynamicContainer.appendChild(card);
    });
  }
}

function renderLegacyRecommendations(data) {
  const recContainer = document.getElementById('recommendations-container');
  if (recContainer && data.kpis && data.kpis.key_insights) {
    const insights = data.kpis.key_insights;
    recContainer.innerHTML = insights.map(i => `
      <div class="flex items-start space-x-3">
        <div class="flex-shrink-0 w-1.5 h-1.5 rounded-full bg-blue-500 mt-2"></div>
        <p class="text-sm text-gray-600">${i}</p>
      </div>
     `).join('');
  }
}

function renderMaintenanceTableSummary(data) {
  const tbody = document.querySelector('#maintenance-table tbody');
  if (tbody && data.fleet && data.fleet.vehicles) {
    const criticalVehicles = data.fleet.vehicles.filter(v => (v.priority || '').toLowerCase().includes('critical'));
    const vehiclesToShow = criticalVehicles.length > 0 ? criticalVehicles.slice(0, 5) : data.fleet.vehicles.slice(0, 5);

    tbody.innerHTML = vehiclesToShow.map(v => {
      const est = estimateHoursAndCost(v.segment, v.priority, v.vehicle_id);
      return `
        <tr>
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${v.vehicle_id || 'N/A'}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${inferSegment(v.segment, v.vehicle_id)}</td>
          <td class="px-6 py-4 whitespace-nowrap"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(v.priority)}">${v.priority || 'Unknown'}</span></td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">High</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${getScheduledStatus(v.priority)}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Mumbai SC</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${est.hours} hrs</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">$${formatCurrency(est.cost)}</td>
        </tr>
      `;
    }).join('');
  }
}

// 2. FLEET HEALTH PAGE
function renderFleetHealthPage(data) {
  const fleet = data.fleet || {};
  const vehicles = fleet.vehicles || [];

  setText('count-critical', fleet.critical || 0);
  setText('count-warning', fleet.warning || 0);
  setText('count-healthy', fleet.healthy || 0);

  const tbody = document.querySelector('#fleet-table tbody');
  if (tbody) {
    tbody.innerHTML = vehicles.map(v => `
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${v.vehicle_id}</td>
        <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate" title="${v.sensor_status || ''}">${v.sensor_status || 'Normal'}</td>
        <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">${v.anomalies || 'None'}</td>
        <td class="px-6 py-4 whitespace-nowrap"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(v.priority)}">${v.priority}</span></td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${inferSegment(v.segment, v.vehicle_id)}</td>
      </tr>
    `).join('');
  }

  renderFleetHealthTrend(data);
  renderPriorityDistribution(data);
}

// 3. FAILURE PREDICTIONS PAGE
function renderFailurePredictionsPage(data) {
  const failures = data.failures || {};
  const predictions = failures.predictions || [];

  setText('total-predictions', failures.total_predictions || predictions.length);

  const tbody = document.querySelector('#predictions-table tbody');
  if (tbody) {
    tbody.innerHTML = predictions.map(p => `
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${p.component}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${p.failure_probability}%</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${p.confidence_level}%</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${p.estimated_time_to_failure || 'Unknown'}</td>
        <td class="px-6 py-4 whitespace-nowrap"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getRiskBadgeClass(p.safety_impact)}">${p.safety_impact || 'Medium'}</span></td>
      </tr>
    `).join('');
  }

  renderComponentFailures(data);
}

// 4. CUSTOMER ENGAGEMENT PAGE
function renderCustomerEngagementPage(data) {
  const engagement = data.engagement || {};
  const methods = engagement.communication_methods || {};
  const engagements = engagement.engagements || [];

  setText('engagement-rate', `${data.kpis.engagementRate || 92}%`);

  let bestMethod = 'N/A', maxCount = -1;
  let worstMethod = 'N/A', minCount = Infinity;

  for (const [method, count] of Object.entries(methods)) {
    if (count > maxCount) { maxCount = count; bestMethod = method; }
    if (count < minCount) { minCount = count; worstMethod = method; }
  }
  setText('best-method', capitalize(bestMethod));
  setText('worst-method', capitalize(worstMethod));

  const tbody = document.querySelector('#engagement-table tbody');
  if (tbody) {
    if (engagements.length > 0) {
      tbody.innerHTML = engagements.map(e => `
            <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${capitalize(e.method)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${e.status === 'contacted' ? '100%' : 'Pending'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${e.response === 'positive' ? 'High' : 'Low'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Active</td>
            </tr>
        `).join('');
    } else {
      tbody.innerHTML = Object.entries(methods).map(([method, count]) => `
            <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${capitalize(method)}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${count} engagements</td>
            </tr>
        `).join('');
    }
  }

  renderEngagementChannels(data);
}

// 5. SERVICE SCHEDULING PAGE
function renderServiceSchedulingPage(data) {
  const scheduling = data.scheduling || {};
  const appointments = scheduling.appointments || [];

  setText('utilization-min', '65%');
  setText('utilization-max', '85%');

  const tbody = document.querySelector('#scheduling-table tbody');
  if (tbody) {
    tbody.innerHTML = appointments.map(a => `
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${a.vehicle_id}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${a.scheduled_date}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${a.service_center}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${a.workload || 75}%</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">Yes</td>
      </tr>
    `).join('');
  }

  renderServiceWorkload(data);
}

// 6. SERVICE QUALITY PAGE
function renderServiceQualityPage(data) {
  const quality = data.quality || {};

  setText('avg-satisfaction', `${quality.customer_satisfaction_score || 8.7}/10`);
  setText('avg-completion', `${quality.completion_rate || 95}%`);

  const tbody = document.querySelector('#quality-table tbody');
  if (tbody) {
    const mockRows = [
      { vehicle: 'VEH001', completion: '100%', score: '9/10', trend: 'Rising', tech: 'Rajesh Kumar' },
      { vehicle: 'VEH002', completion: '90%', score: '8/10', trend: 'Stable', tech: 'Amit Singh' },
      { vehicle: 'VEH004', completion: '100%', score: '9.5/10', trend: 'Rising', tech: 'Rajesh Kumar' },
    ];

    tbody.innerHTML = mockRows.map(r => `
      <tr>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${r.vehicle}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${r.completion}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">${r.score}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600">${r.trend}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${r.tech}</td>
      </tr>
    `).join('');
  }
}

// 7. MANUFACTURING QUALITY PAGE
function renderManufacturingQualityPage(data) {
  const container = document.getElementById('manufacturing-insights-container');

  if (data.markdown) {
    const qualityKeys = Object.keys(data.markdown).filter(k =>
      k.toLowerCase().includes('defect') ||
      k.toLowerCase().includes('manufacturing') ||
      k.toLowerCase().includes('root cause') ||
      k.toLowerCase().includes('supplier')
    );

    if (qualityKeys.length > 0) {
      container.innerHTML = qualityKeys.map(key => {
        const blocks = data.markdown[key];
        let contentHtml = '';
        blocks.forEach(b => {
          if (b.type === 'list') {
            contentHtml += `<ul class="space-y-2">${b.items.map(i => `
              <li class="flex items-start">
                <span class="flex-shrink-0 h-1.5 w-1.5 rounded-full bg-red-500 mt-2 mr-2"></span>
                <span class="text-sm text-gray-600">${i}</span>
              </li>`).join('')}</ul>`;
          } else if (b.type === 'text') {
            contentHtml += `<p class="text-sm text-gray-600 mb-2">${b.content}</p>`;
          }
        });
        return `
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 border-b pb-2">${key}</h3>
            ${contentHtml}
          </div>
        `;
      }).join('');
      return;
    }
  }

  const insights = [
    { title: "Critical Defects", items: ["Brake pad delamination in Batch #402", "Oil seal leaks in heavy-duty engines"] },
    { title: "High-Incidence Issues", items: ["Transmission overheating in urban traffic", "Battery voltage drops > 15%"] },
    { title: "Supplier Defect Issues", items: ["BrakeTech Industries: 12% defect rate", "FilterCorp: Seal integrity failure"] },
    { title: "Design Improvements", items: ["Upgrade brake pad material to ceramic composite", "Increase oil cooler capacity by 20%"] }
  ];

  if (container) {
    container.innerHTML = insights.map(section => `
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 class="text-lg font-semibold text-gray-900 mb-4 border-b pb-2">${section.title}</h3>
        <ul class="space-y-2">
          ${section.items.map(item => `
            <li class="flex items-start">
              <span class="flex-shrink-0 h-1.5 w-1.5 rounded-full bg-red-500 mt-2 mr-2"></span>
              <span class="text-sm text-gray-600">${item}</span>
            </li>
          `).join('')}
        </ul>
      </div>
    `).join('');
  }
}

// ============================================================================
// SHARED CHART RENDERERS
// ============================================================================

function renderKPIs(data) {
  const kpiContainer = document.getElementById('kpi-container');
  if (!kpiContainer) return;

  const kpis = data.kpis || {};
  const fleet = data.fleet || {};

  const kpiCards = [
    { title: "Fleet Health Score", value: `${kpis.fleetHealthScore || 85}%`, trend: "+2.5%", isPositive: true },
    { title: "Critical Vehicles", value: fleet.critical || 0, trend: "Action Req", isPositive: false },
    { title: "Predicted Failures", value: (data.failures && data.failures.total_predictions) || 15, trend: "New", isPositive: false },
    { title: "Cost Savings", value: `$${formatCurrency(kpis.costSavings || 240000)}`, trend: "YTD", isPositive: true },
    { title: "Availability", value: "96.5%", trend: "Stable", isPositive: true }
  ];

  kpiContainer.innerHTML = kpiCards.map(kpi => `
    <div class="bg-white p-5 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">${kpi.title}</div>
      <div class="text-2xl font-bold text-gray-900 mb-1">${kpi.value}</div>
      <div class="text-sm font-medium ${kpi.isPositive ? 'text-green-600' : 'text-red-600'}">${kpi.trend}</div>
    </div>
  `).join('');
}

function renderFleetHealthTrend(data) {
  const ctx = document.getElementById('healthTrendChart');
  if (!ctx) return;

  new Chart(ctx.getContext('2d'), {
    type: 'line',
    data: {
      labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [{
        label: 'Fleet Health Score',
        data: [65, 68, 72, 78, 84, 90],
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99,102,241,0.1)',
        fill: true,
        tension: 0.4
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
  });
}

function renderPriorityDistribution(data) {
  const ctx = document.getElementById('priorityDistChart');
  if (!ctx) return;

  const fleet = data.fleet || {};
  new Chart(ctx.getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: ['Healthy', 'Warning', 'Critical'],
      datasets: [{
        data: [fleet.healthy || 7, fleet.warning || 2, fleet.critical || 1],
        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
        borderWidth: 0
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom' } } }
  });
}

function renderComponentFailures(data) {
  const ctx = document.getElementById('failureProbChart');
  if (!ctx) return;

  const labels = ['Engine', 'Brakes', 'Transmission', 'Battery', 'Tires'];
  const values = [45, 30, 25, 15, 10];

  new Chart(ctx.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Failure Probability (%)',
        data: values,
        backgroundColor: '#6366f1',
        borderRadius: 4
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } }
  });
}

function renderServiceWorkload(data) {
  const ctx = document.getElementById('serviceWorkloadChart');
  if (!ctx) return;

  new Chart(ctx.getContext('2d'), {
    type: 'bar',
    data: {
      labels: ['Mumbai SC', 'Delhi SC', 'Bangalore SC'],
      datasets: [{
        label: 'Current Workload (%)',
        data: [85, 65, 45],
        backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
        borderRadius: 4
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } }
  });
}

function renderEngagementChannels(data) {
  const ctx = document.getElementById('engagementChannelChart');
  if (!ctx) return;

  const engagement = data.engagement || {};
  const methods = engagement.communication_methods || { sms: 45, email: 30, app: 20, call: 5 };

  new Chart(ctx.getContext('2d'), {
    type: 'pie',
    data: {
      labels: Object.keys(methods).map(capitalize),
      datasets: [{
        data: Object.values(methods),
        backgroundColor: ['#3b82f6', '#8b5cf6', '#ec4899', '#f97316'],
        borderWidth: 0
      }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
  });
}

// ============================================================================
// UTILITIES & PARSERS
// ============================================================================

function extractAllTables(doc) {
  const tables = [];
  doc.querySelectorAll("table").forEach((table, tableIndex) => {
    // Try to get headers from thead > tr > th OR first row th/td
    let headers = [];
    const theadRow = table.querySelector("thead tr");
    if (theadRow) {
      headers = Array.from(theadRow.querySelectorAll("th, td")).map(cell => cell.textContent.trim());
    }

    // Fallback: check if first row has th elements
    if (headers.length === 0) {
      const firstRow = table.querySelector("tr");
      if (firstRow) {
        const thCells = firstRow.querySelectorAll("th");
        if (thCells.length > 0) {
          headers = Array.from(thCells).map(th => th.textContent.trim());
        }
      }
    }

    // Fallback: use first row td as headers if no th found
    if (headers.length === 0) {
      const firstRow = table.querySelector("tr");
      if (firstRow) {
        const tdCells = firstRow.querySelectorAll("td");
        headers = Array.from(tdCells).map(td => td.textContent.trim());
      }
    }

    // Get all rows
    const allRows = Array.from(table.querySelectorAll("tr"));

    // Determine which rows contain data (skip header row)
    const dataRows = allRows.filter(tr => {
      const thCount = tr.querySelectorAll("th").length;
      const tdCount = tr.querySelectorAll("td").length;
      // Skip rows that are header rows (all th) or empty
      return tdCount > 0;
    });

    const rows = dataRows.map(tr => {
      const cells = Array.from(tr.querySelectorAll("td"));
      const rowObj = {};
      cells.forEach((td, idx) => {
        const header = headers[idx] || `col_${idx}`;
        rowObj[header] = td.textContent.trim();
      });
      return rowObj;
    }).filter(r => Object.keys(r).length > 0);

    console.log(`📊 Table ${tableIndex}: headers=${JSON.stringify(headers)}, rows=${rows.length}`);

    if (headers.length > 0 && rows.length > 0) {
      tables.push({ type: classifyTable(headers), headers, rows });
    }
  });

  console.log(`📋 Total tables extracted: ${tables.length}`);
  return tables;
}

function classifyTable(headers) {
  const text = headers.join(' ').toLowerCase();
  console.log(`🔍 Classifying table with headers: ${text}`);

  // More comprehensive keyword matching
  if (text.includes('vehicle') || text.includes('sensor') || text.includes('anomal') || text.includes('health') || text.includes('maintenance priority')) return 'fleet';
  if (text.includes('component') || text.includes('failure') || text.includes('probability') || text.includes('prediction')) return 'failures';
  if (text.includes('engagement') || text.includes('method') || text.includes('channel') || text.includes('communication')) return 'engagement';
  if (text.includes('appointment') || text.includes('schedule') || text.includes('service center') || text.includes('workload')) return 'scheduling';
  if (text.includes('satisfaction') || text.includes('completion') || text.includes('quality')) return 'quality';
  if (text.includes('kpi') || text.includes('metric')) return 'kpis';
  return 'unknown';
}

function extractKPIsFromMarkdown(md) {
  const kpis = {};

  // More flexible regex patterns
  const patterns = {
    fleetHealthScore: /(?:Fleet\s*Health\s*Score|Health\s*Score|Overall\s*Health)[\s::\-–—]*(\d+(?:\.\d+)?)\s*%?/i,
    engagementRate: /(?:Overall\s*)?Engagement\s*Rate[\s::\-–—]*(\d+(?:\.\d+)?)\s*%?/i,
    costSavings: /Cost\s*Savings[\s::\-–—]*\$?\s*([\d,]+(?:\.\d+)?)/i,
    criticalVehicles: /Critical\s*(?:Vehicles?|Count)[\s::\-–—]*(\d+)/i,
    totalPredictions: /(?:Total\s*)?Predictions?[\s::\-–—]*(\d+)/i
  };

  for (const [key, regex] of Object.entries(patterns)) {
    const match = regex.exec(md);
    if (match) {
      kpis[key] = parseFloat(match[1].replace(/,/g, ''));
      console.log(`✓ KPI extracted: ${key} = ${kpis[key]}`);
    }
  }

  return kpis;
}

function buildDataModels(tables, kpis) {
  const data = { fleet: { vehicles: [] }, failures: { predictions: [] }, engagement: { communication_methods: {}, engagements: [] }, scheduling: { appointments: [] }, quality: {}, kpis: kpis };

  console.log(`🔧 Building data models from ${tables.length} tables`);

  tables.forEach(table => {
    console.log(`  Processing table type: ${table.type} with ${table.rows.length} rows`);

    if (table.type === 'fleet') {
      data.fleet.vehicles = processFleetRows(table.rows, table.headers);
    } else if (table.type === 'failures') {
      data.failures.predictions = processFailureRows(table.rows, table.headers);
    } else if (table.type === 'engagement') {
      const engData = processEngagementRows(table.rows, table.headers);
      data.engagement = engData;
    } else if (table.type === 'scheduling') {
      data.scheduling.appointments = processSchedulingRows(table.rows, table.headers);
    } else if (table.type === 'quality') {
      data.quality = processQualityRows(table.rows, table.headers);
    }
  });

  // Calculate fleet counts
  if (data.fleet.vehicles && data.fleet.vehicles.length > 0) {
    data.fleet.critical = data.fleet.vehicles.filter(v => (v.priority || '').toLowerCase().includes('critical') || (v.priority || '').toLowerCase().includes('high')).length;
    data.fleet.warning = data.fleet.vehicles.filter(v => (v.priority || '').toLowerCase().includes('warning') || (v.priority || '').toLowerCase().includes('medium')).length;
    data.fleet.healthy = data.fleet.vehicles.filter(v => (v.priority || '').toLowerCase().includes('healthy') || (v.priority || '').toLowerCase().includes('low') || (v.priority || '').toLowerCase().includes('normal')).length;
    console.log(`  Fleet counts: critical=${data.fleet.critical}, warning=${data.fleet.warning}, healthy=${data.fleet.healthy}`);
  }

  // Set prediction count
  if (data.failures.predictions.length > 0) {
    data.failures.total_predictions = data.failures.predictions.length;
  }

  return data;
}

function processFleetRows(rows, headers) {
  console.log(`  Processing ${rows.length} fleet rows with headers: ${headers?.join(', ')}`);
  return rows.map(r => {
    const vehicle = {
      vehicle_id: findVal(r, ['vehicle', 'id', 'veh']) || Object.values(r)[0],
      priority: findVal(r, ['priority', 'severity', 'maintenance', 'status']) || 'Unknown',
      segment: findVal(r, ['segment', 'type', 'category']),
      sensor_status: findVal(r, ['sensor', 'reading', 'value']),
      anomalies: findVal(r, ['anomal', 'issue', 'problem', 'alert'])
    };
    return vehicle;
  });
}

function processFailureRows(rows, headers) {
  console.log(`  Processing ${rows.length} failure rows with headers: ${headers?.join(', ')}`);
  return rows.map(r => ({
    component: findVal(r, ['component', 'part', 'system']) || Object.values(r)[0],
    failure_probability: parseFloat(findVal(r, ['probability', 'risk', 'failure', 'prob']) || 0),
    confidence_level: parseFloat(findVal(r, ['confidence', 'certainty']) || 80),
    estimated_time_to_failure: findVal(r, ['time', 'days', 'estimate', 'ttf', 'remaining']),
    safety_impact: findVal(r, ['safety', 'impact', 'severity', 'risk'])
  }));
}

function processEngagementRows(rows, headers) {
  console.log(`  Processing ${rows.length} engagement rows with headers: ${headers?.join(', ')}`);
  const methods = {};
  const engagements = rows.map(r => {
    const method = findVal(r, ['method', 'channel', 'type', 'communication']) || Object.values(r)[0];
    if (method) methods[method] = (methods[method] || 0) + 1;
    return {
      method,
      status: findVal(r, ['status', 'result']),
      response: findVal(r, ['response', 'outcome', 'success']),
      rate: findVal(r, ['rate', 'percentage', '%'])
    };
  });
  return { communication_methods: methods, engagements };
}

function processSchedulingRows(rows, headers) {
  console.log(`  Processing ${rows.length} scheduling rows with headers: ${headers?.join(', ')}`);
  return rows.map(r => ({
    vehicle_id: findVal(r, ['vehicle', 'id']) || Object.values(r)[0],
    scheduled_date: findVal(r, ['date', 'schedule', 'appointment', 'time']),
    service_center: findVal(r, ['center', 'location', 'facility', 'service']),
    workload: parseInt(findVal(r, ['workload', 'capacity', 'utilization']) || 75)
  }));
}

function processQualityRows(rows, headers) {
  console.log(`  Processing ${rows.length} quality rows with headers: ${headers?.join(', ')}`);
  if (rows.length === 0) {
    return { completion_rate: 95, customer_satisfaction_score: 8.7 };
  }
  return {
    completion_rate: parseFloat(findVal(rows[0], ['completion', 'complete', 'rate']) || 95),
    customer_satisfaction_score: parseFloat(findVal(rows[0], ['satisfaction', 'score', 'rating']) || 8.7)
  };
}

function findVal(obj, keys) {
  // First try exact key matches
  for (const key of keys) {
    if (obj[key] !== undefined) return obj[key];
  }

  // Then try partial/case-insensitive matches
  for (const k of Object.keys(obj)) {
    const lowerK = k.toLowerCase();
    if (keys.some(key => lowerK.includes(key.toLowerCase()))) {
      return obj[k];
    }
  }
  return null;
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function getStatusBadgeClass(status) {
  const s = (status || '').toLowerCase();
  if (s.includes('critical')) return 'bg-red-100 text-red-800';
  if (s.includes('warning') || s.includes('medium')) return 'bg-yellow-100 text-yellow-800';
  if (s.includes('healthy') || s.includes('low')) return 'bg-green-100 text-green-800';
  return 'bg-gray-100 text-gray-800';
}

function getRiskBadgeClass(risk) {
  const r = (risk || '').toLowerCase();
  if (r.includes('high') || r.includes('critical')) return 'bg-red-100 text-red-800';
  if (r.includes('medium')) return 'bg-yellow-100 text-yellow-800';
  return 'bg-green-100 text-green-800';
}

function getScheduledStatus(priority) {
  const p = (priority || '').toLowerCase();
  if (p.includes('critical')) return 'Scheduled (Urgent)';
  if (p.includes('warning')) return 'Pending';
  return 'Routine';
}

function inferSegment(segment, id) {
  if (segment) return segment;
  if ((id || '').includes('Heavy')) return 'Heavy Duty';
  return 'Light Duty';
}

function estimateHoursAndCost(segment, priority, id) {
  const isHeavy = (segment || '').toLowerCase().includes('heavy') || (id || '').toLowerCase().includes('heavy');
  const rate = isHeavy ? 200 : 125;
  const baseHours = (priority || '').toLowerCase().includes('critical') ? 6 : 2;
  return { hours: baseHours, cost: baseHours * rate };
}

function formatCurrency(val) {
  return Number(val).toLocaleString();
}
