# Automotive Predictive Maintenance AI System

AI-powered predictive maintenance for automotive fleets using multi-agent orchestration. Built for EY Techathon 2025.

## What It Does

Analyzes vehicle telemetry data to predict component failures before they happen, automatically notifies customers, schedules maintenance appointments, and generates business intelligence insights.

**7 AI Agents Working Together:**
- Fleet data monitoring & analysis
- Component failure prediction
- Customer engagement & notifications
- Service appointment scheduling
- Feedback collection & quality tracking
- Manufacturing defect pattern detection
- Business intelligence dashboard generation

## Tech Stack

**Framework**: CrewAI (multi-agent orchestration)
**LLM**: Cerebras API (llama3.1-8b) + Perplexity API, or local Ollama (mistral)
**Dashboard / Frontend**: Flask + React/Vue with JavaScript
**Tools**: Custom APIs for vehicle telematics, maintenance history, service centers, route optimization

## Quick Start

**1. Install Dependencies**
```powershell
pip install -r requirements.txt
```

**2. Configure LLM Provider**

Copy `.env.example` to `.env` and choose your provider:

```env
# Option A: Cerebras (fast, cloud-based, free tier)
LLM_PROVIDER=cerebras
CEREBRAS_API_KEY=your_key_from_cloud.cerebras.ai

# Option B: Ollama (local, private, no API key)
LLM_PROVIDER=ollama
# Run: ollama pull mistral:latest
```

**3. Run the AI Workflow**
```powershell
python src\systemm\main.py run
```

This generates `src\systemm\crew_report.json` with analysis results (takes 2-5 min with Cerebras, 10-20 min with Ollama).

**4. Launch Dashboard**
```powershell
python dashboard\app.py
```

Open http://localhost:5000 to view the analysis dashboard.

## Project Structure

```
├── src/systemm/           # AI agent system
│   ├── crew.py           # Agent orchestration
│   ├── main.py           # Entry point
│   ├── config/           # Agent & task definitions
│   └── tools/            # Custom API tools
├── dashboard/            # Web dashboard
│   ├── app.py           # Flask server
│   └── frontend/        # React UI
├── .env.example         # Config template
└── requirements.txt     # Python dependencies
```

## How It Works

1. **Data Analysis Agent** fetches vehicle telemetry (battery health, motor status, brake wear)
2. **Diagnosis Agent** predicts failures using historical patterns and ML
3. **Customer Engagement Agent** generates personalized maintenance alerts
4. **Scheduling Agent** finds nearby service centers and optimizes routes
5. **Feedback Agent** tracks service completion and updates records
6. **Manufacturing Insights Agent** identifies recurring defects across fleet
7. **Master Orchestrator** compiles everything into a BI dashboard report

All agents run sequentially, passing context to the next. Final output is a JSON report displayed on the web dashboard.

## Requirements

- Python 3.10-3.13
- 8GB RAM (16GB recommended for local Ollama)
- Internet connection (for Cerebras) or Ollama installed locally
- No GPU required

---

**Built with CrewAI** | Optimized for laptops without dedicated GPUs
