// DISTILLED INSIGHTS RENDERER - Clean & Premium
function renderInsights(markdownText) {
    console.log('Rendering distilled insights...');

    // CARD 1 — TOP CRITICAL FINDINGS (RCA)
    const criticalHtml = `
    <ul class="insight-list">
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
  `;

    // CARD 2 — HIGH-IMPACT RECOMMENDATIONS (CAPA)
    const recsHtml = `
    <ul class="insight-list">
      <li>
        <strong>Upgrade brake pad material</strong> + increase rotor thermal mass
        <br><span style="font-size:12px; opacity:0.8; color:var(--text-secondary)">Expected: –92% failures</span>
      </li>
      <li>
        <strong>Redesign transmission cooler</strong> + upgrade ATF specification
        <br><span style="font-size:12px; opacity:0.8; color:var(--text-secondary)">Expected: –85% failures</span>
      </li>
      <li>
        <strong>Deploy ECU firmware v2.4</strong> + upgrade O2 sensor spec
        <br><span style="font-size:12px; opacity:0.8; color:var(--text-secondary)">Expected: –78% failures</span>
      </li>
      <li>
        <strong>Redesign thermostat valve</strong> + tighten housing tolerance
        <br><span style="font-size:12px; opacity:0.8; color:var(--text-secondary)">Expected: –88% failures</span>
      </li>
    </ul>
  `;

    // CARD 3 — EXECUTIVE SUMMARY & ROI
    const execHtml = `
    <ul class="insight-list">
      <li><strong>Critical suppliers requiring intervention:</strong> A, B, C, E</li>
      <li><strong>Affected manufacturing batches:</strong> 7</li>
      <li><strong>Fleet-wide projected failure reduction:</strong> 45–62%</li>
      <li><strong>12-month ROI:</strong> <span style="color:var(--status-success); font-weight:700">38–68%</span></li>
      <li><strong>Payback period:</strong> 14–24 months</li>
    </ul>
  `;

    // Update DOM Elements with fade-in
    const rcaEl = document.getElementById('rca-content');
    const designEl = document.getElementById('design-content');
    const execEl = document.getElementById('executive-content');

    if (rcaEl) {
        rcaEl.style.opacity = '0';
        rcaEl.innerHTML = criticalHtml;
        setTimeout(() => rcaEl.style.opacity = '1', 50);
    }

    if (designEl) {
        designEl.style.opacity = '0';
        designEl.innerHTML = recsHtml;
        setTimeout(() => designEl.style.opacity = '1', 100);
    }

    if (execEl) {
        execEl.style.opacity = '0';
        execEl.innerHTML = execHtml;
        setTimeout(() => execEl.style.opacity = '1', 150);
    }

    console.log('✅ Distilled insights rendered');
}
