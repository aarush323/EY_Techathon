document.addEventListener("DOMContentLoaded", () => {
  const reportContainer = document.getElementById("report-container");
  const timestampContainer = document.getElementById("report-timestamp");
  const syncTime = document.getElementById("sync-time");

  function updateSyncTime() {
    const now = new Date();
    syncTime.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  }

  async function fetchReport() {
    try {
      const response = await fetch("/api/dashboard");
      if (!response.ok) throw new Error("Report not ready yet");

      const data = await response.json();
      const rawText = data.report_text || 'No report text available';

      // Enhanced markdown table to HTML conversion with improved logic
      const tableRegex = /\|(.+)\|\n\|([-\s|]+)\|\n((?:\|.*\|\n)+)/g;
      let htmlText = rawText.replace(tableRegex, (_, headers, separator, rows) => {
        // Process headers - filter out empty cells
        const headerArray = headers.split('|')
          .map(h => h.trim())
          .filter(h => h.length > 0);
        
        const headerCells = headerArray.map(h => `<th>${h}</th>`).join('');

        // Process rows with improved cell handling
        const rowLines = rows.trim().split('\n');
        const rowHTML = rowLines.map(line => {
          // Split by | and filter out empty leading/trailing cells
          const cells = line.split('|')
            .map(c => c.trim())
            .filter((c, idx, arr) => {
              // Keep middle cells, remove leading/trailing empty ones
              if (idx === 0 || idx === arr.length - 1) return c.length > 0;
              return true;
            });
          
          // Pad cells to match header length
          const paddedCells = [...cells];
          while (paddedCells.length < headerArray.length) {
            paddedCells.push('');
          }
          
          // Truncate if more cells than headers
          const finalCells = paddedCells.slice(0, headerArray.length);
          
          return `<tr>${finalCells.map(c => `<td>${c || '-'}</td>`).join('')}</tr>`;
        }).join('');

        return `<table><thead><tr>${headerCells}</tr></thead><tbody>${rowHTML}</tbody></table>`;
      });

      // Enhanced markdown replacements with proper ordering
      htmlText = htmlText
        .replace(/(?:^|\n)---+/g, '<hr>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '<br><br>');

      reportContainer.innerHTML = htmlText;
      timestampContainer.textContent = `Last updated: ${data.timestamp || 'N/A'}`;
      updateSyncTime();
    } catch (err) {
      reportContainer.innerHTML = `
        <div class="loading-container">
          <div style="font-size: 18px; color: #00ffcc; margin-bottom: 10px; font-weight: 600;">◢ AWAITING DATA STREAM ◣</div>
          <div style="font-size: 14px; color: rgba(0, 255, 204, 0.6);">Execute main.py to generate crew analysis</div>
        </div>
      `;
      timestampContainer.textContent = "Standby Mode";
      console.warn(err);
    }
  }

  // Initial fetch and update sync time
  fetchReport();
  updateSyncTime();
  
  // Periodic updates
  setInterval(fetchReport, 10000);
  setInterval(updateSyncTime, 1000);

  // Particles.js configuration
  particlesJS('particles-js', {
    particles: {
      number: { value: 80, density: { enable: true, value_area: 800 } },
      color: { value: '#00ffcc' },
      shape: { type: 'circle' },
      opacity: { value: 0.3, random: true },
      size: { value: 3, random: true },
      line_linked: {
        enable: true,
        distance: 150,
        color: '#00ffcc',
        opacity: 0.2,
        width: 1
      },
      move: {
        enable: true,
        speed: 2,
        direction: 'none',
        random: false,
        straight: false,
        out_mode: 'out',
        bounce: false
      }
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: { enable: true, mode: 'grab' },
        onclick: { enable: true, mode: 'push' },
        resize: true
      },
      modes: {
        grab: { distance: 140, line_linked: { opacity: 0.5 } },
        push: { particles_nb: 4 }
      }
    },
    retina_detect: true
  });
});