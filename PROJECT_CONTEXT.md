# Automotive Predictive Maintenance AI System - Complete Project Context

## Project Overview

**Name:** Automotive Predictive Maintenance AI System  
**Framework:** CrewAI (Multi-Agent AI Orchestration)  
**Purpose:** Predictive maintenance system for automotive fleets using AI agents to analyze vehicle telemetry, predict component failures, engage customers, schedule maintenance, and generate business intelligence insights.

**Created For:** EY Techathon 2025  
**Hardware:** Asus TUF F15 (no dedicated GPU requirements)

---

## Architecture Overview

### Multi-Agent System (7 AI Agents)

The system uses **CrewAI** to orchestrate 7 specialized AI agents that work sequentially to complete a comprehensive predictive maintenance workflow:

1. **Data Analysis Agent**
   - Tools: VehicleTelematicsAPI, MaintenanceHistoryAPI
   - Role: Monitors vehicle fleet data, analyzes telemetry metrics
   - Task: Fetch and analyze real-time vehicle health data

2. **Diagnosis Agent**
   - Tools: MaintenanceHistoryAPI
   - Role: Predicts component failures based on historical patterns
   - Task: Identify priority maintenance needs and failure probabilities

3. **Customer Engagement Agent**
   - Tools: CustomerNotificationAPI
   - Role: Creates personalized maintenance alerts
   - Task: Generate and send customer notifications about required maintenance

4. **Scheduling Agent**
   - Tools: ServiceCenterAPI, IternioRouteOptimizer
   - Role: Finds nearby service centers and optimizes routes
   - Task: Book maintenance appointments considering location and route optimization

5. **Feedback Agent**
   - Tools: CustomerNotificationAPI, MaintenanceHistoryAPI
   - Role: Collects service completion feedback
   - Task: Update maintenance records with service results

6. **Manufacturing Quality Insights Agent**
   - Tools: MaintenanceHistoryAPI
   - Role: Analyzes patterns across entire fleet
   - Task: Identify recurring issues and component quality trends

7. **Master Orchestrator Agent**
   - Tools: None (aggregates outputs from other agents)
   - Role: Compiles comprehensive business intelligence
   - Task: Generate final dashboard report with all insights

### Workflow Execution

**Process Type:** Sequential  
**Execution Flow:** Agents run one after another in order  
**Output:** JSON report saved to `src/systemm/crew_report.json`  
**Runtime:** 2-5 minutes with Cerebras API, 10-20 minutes with local Ollama

---

## Technology Stack

### Core Framework
- **CrewAI** (>=0.203.0) - Multi-agent AI orchestration
- **LiteLLM** - Unified LLM interface (included with CrewAI)
- **Pydantic** (>=2.0.0) - Data validation and schema management

### LLM Providers (Dual Configuration)

**Primary: Cerebras API (Recommended)**
- Model: `cerebras/llama3.1-8b` (8B parameters)
- Benefits: Fast inference, free tier, cloud-based, no GPU required
- API Key Required: Yes (from https://cloud.cerebras.ai/)

**Backup: Local Ollama**
- Model: `ollama/mistral:latest` (7B parameters)
- Benefits: Fully private, offline capable, no API costs
- API Key Required: No (local execution)

**Configuration Method:** Environment variables in `.env` file
```env
LLM_PROVIDER=cerebras  # or 'ollama'
CEREBRAS_API_KEY=your_key_here  # only for Cerebras
```

### Web Dashboard
- **Flask** (>=3.0.0) - Backend API server
- **Flask-CORS** (>=4.0.0) - Cross-origin resource sharing
- **Frontend:** HTML/CSS/JavaScript (static files served by Flask)

### Environment Management
- **python-dotenv** (>=1.0.0) - Load `.env` configuration files

### External APIs & Tools
- **VehicleTelematicsAPI** - Mock vehicle sensor data
- **MaintenanceHistoryAPI** - Historical maintenance records with ML predictions
- **CustomerNotificationAPI** - Customer communication system
- **ServiceCenterAPI** - Service center availability and booking
- **IternioRouteOptimizer** - EV route optimization (uses external Iternio API)
- **requests** (>=2.31.0) - HTTP client for API calls

---

## Project Structure

```
EY_Techathon/
├── src/
│   └── systemm/
│       ├── __init__.py
│       ├── crew.py              # Main crew orchestration with LLM config
│       ├── main.py              # Entry point for running workflow
│       ├── config/
│       │   ├── agents.yaml      # Agent definitions and prompts
│       │   └── tasks.yaml       # Task definitions and descriptions
│       └── tools/
│           ├── __init__.py
│           ├── custom_tool.py
│           ├── vehicle_telematics_api.py
│           ├── maintenance_history_api.py
│           ├── customer_notification_api.py
│           ├── service_center_api.py
│           ├── iternio_route_optimizer.py
│           └── ueba_security_monitor.py
│
├── dashboard/
│   ├── app.py                   # Flask server
│   ├── start_dashboard.py       # Dashboard launcher
│   ├── test_server.py          # Server testing utility
│   ├── index.html              # Dashboard UI
│   ├── styles.css              # Dashboard styles
│   └── script.js               # Dashboard JavaScript
│
├── knowledge/                   # Knowledge base for agents
│
├── .env                         # Environment config (gitignored)
├── .env.example                 # Template for .env
├── .gitignore
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata
│
├── README.md                    # Project documentation
├── RUN_INSTRUCTIONS.md         # Detailed setup and execution guide
├── CEREBRAS_SETUP.md           # Cerebras API configuration guide
├── QUICKSTART.md               # Quick start commands
└── PROJECT_CONTEXT.md          # This file
```

---

## Detailed Component Descriptions

### 1. Core Orchestration (`crew.py`)

**Key Features:**
- Dynamic LLM provider selection via environment variables
- Loads `.env` file on import using `python-dotenv`
- Configures all 7 agents with appropriate tools
- Implements CrewAI decorators: `@agent`, `@task`, `@crew`

**LLM Configuration Logic:**
```python
llm_provider = os.getenv("LLM_PROVIDER", "cerebras").lower()

if llm_provider == "cerebras":
    # Uses cerebras/llama3.1-8b for all agents
else:
    # Uses ollama/mistral:latest for all agents
```

**Agent Initialization Example:**
```python
@agent
def data_analysis_agent(self) -> Agent:
    return Agent(
        config=self.agents_config["data_analysis_agent"],
        tools=[VehicleTelematicsAPI(), MaintenanceHistoryAPI()],
        llm=LLM(model=self.llm_models["data_analysis_agent"], temperature=0.7),
        reasoning=False,
        max_iter=25,
        allow_delegation=False
    )
```

### 2. Main Entry Point (`main.py`)

**Functions:**
- `run()` - Execute the crew workflow with sample inputs
- `train()` - Train crew on historical data
- `test()` - Test crew performance
- `replay()` - Replay specific task execution

**Sample Inputs:**
```python
inputs = {
    'oem_name': 'Sample OEM',
    'customer_name': 'John Doe',
    'vehicle_id': 'VH12345'
}
```

**Output Handling:**
- Generates JSON report at `src/systemm/crew_report.json`
- Includes report text and timestamp
- Prints results to terminal

### 3. Custom Tools

Each tool inherits from `crewai.tools.BaseTool` and implements:
- Input schema using Pydantic `BaseModel`
- `_run()` method with core logic
- Description and name attributes

**Example Tools:**

**VehicleTelematicsAPI:**
- Simulates real-time vehicle sensor data
- Returns: Battery health, motor diagnostics, brake metrics, tire pressure

**MaintenanceHistoryAPI:**
- Retrieves historical maintenance records
- Implements ML-based failure prediction
- Returns: Service history, predicted failures, confidence scores

**ServiceCenterAPI:**
- Finds nearby service centers
- Checks availability and books appointments
- Uses geolocation and scheduling logic

**IternioRouteOptimizer:**
- Integrates with external Iternio API
- Optimizes routes for EVs considering charging stations
- Requires Iternio API key (configured in tool)

### 4. Dashboard (`dashboard/app.py`)

**Flask Routes:**
- `/` - Serves main dashboard HTML
- `/styles.css` - Dashboard styles
- `/script.js` - Dashboard JavaScript
- `/api/dashboard` - Returns crew report JSON
- `/api/run-analysis` - Info endpoint about running analysis

**Features:**
- CORS enabled for local development
- Serves static files from dashboard directory
- Reads report from `src/systemm/crew_report.json`
- Returns 503 if report not yet generated

---

## Configuration Files

### `.env` (User-created, gitignored)
```env
# LLM Provider: cerebras or ollama
LLM_PROVIDER=cerebras

# Cerebras API Configuration
CEREBRAS_API_KEY=csk-your-actual-key-here

# Ollama runs locally, no key needed
```

### `agents.yaml`
Defines each agent's configuration:
- Role description
- Goal statement
- Backstory/context
- LLM parameters

### `tasks.yaml`
Defines each task's configuration:
- Description
- Expected output format
- Agent assignment
- Context/dependencies

### `requirements.txt`
```txt
# Core AI Framework (includes LiteLLM for Ollama support)
crewai[tools]>=0.203.0,<1.0.0

# Environment Configuration
python-dotenv>=1.0.0

# Web Framework
flask>=3.0.0
flask-cors>=4.0.0

# Data Validation
pydantic>=2.0.0

# HTTP Requests
requests>=2.31.0
```

---

## How to Run the Project

### Prerequisites

**Option 1: Cerebras API (Recommended)**
1. Get free API key from https://cloud.cerebras.ai/
2. Copy `.env.example` to `.env`
3. Add your `CEREBRAS_API_KEY` to `.env`
4. Set `LLM_PROVIDER=cerebras`

**Option 2: Local Ollama (Backup)**
1. Install Ollama from https://ollama.ai/download
2. Pull model: `ollama pull mistral:latest`
3. Set `LLM_PROVIDER=ollama` in `.env`

### Installation

```powershell
cd c:\t_thon_latestt\EY_Techathon
pip install -r requirements.txt
```

### Running the AI Workflow

```powershell
# Execute the crew
python src\systemm\main.py run

# Output: src\systemm\crew_report.json
```

### Starting the Dashboard

```powershell
# In new terminal
python dashboard\app.py

# Open browser: http://localhost:5000
```

### Alternative Commands

```powershell
# Train the crew
python src\systemm\main.py train <iterations> <filename>

# Test the crew
python src\systemm\main.py test <iterations>

# Replay a task
python src\systemm\main.py replay <task_id>
```

---

## Workflow Execution Details

### Sequential Process

1. **Input Validation** - System validates OEM name, customer name, vehicle ID
2. **Agent Initialization** - All 7 agents created with configured LLM and tools
3. **Task Execution** - Tasks run sequentially in defined order
4. **Data Flow** - Each task receives context from previous tasks
5. **Report Generation** - Final orchestrator compiles all outputs
6. **JSON Export** - Report saved for dashboard consumption

### Task Dependencies

```
Monitor Fleet Data (Agent 1)
    ↓
Predict Failures (Agent 2)
    ↓
Engage Customers (Agent 3)
    ↓
Schedule Appointments (Agent 4)
    ↓
Collect Feedback (Agent 5)
    ↓
Manufacturing Insights (Agent 6)
    ↓
BI Dashboard (Agent 7) → Final Report
```

### Error Handling

- Agents retry on transient failures (max_iter=25)
- Tools return error messages in structured format
- Dashboard shows 503 if report not generated
- LLM fallback: If Cerebras fails, manually switch to Ollama

---

## API Integrations

### Internal Mock APIs

Most tools use **simulated data** for demonstration:
- `VehicleTelematicsAPI` - Generates realistic sensor readings
- `MaintenanceHistoryAPI` - Creates synthetic maintenance history with ML predictions
- `CustomerNotificationAPI` - Logs notifications (no actual sending)
- `ServiceCenterAPI` - Mock service center database

### External APIs

**Iternio Route Optimizer:**
- Real API integration for EV route optimization
- Endpoint: `https://api.iternio.com/1/...`
- Requires API key: `ITERNIO_API_KEY` in environment or tool code
- Features: Charging station planning, route optimization

---

## Recent Changes & Configuration

### LLM Provider Evolution

1. **Initial:** Perplexity API (`perplexity/sonar-pro`)
2. **Migration 1:** Local Ollama (`ollama/llama3.2:1b`)
3. **User Change:** Local Ollama (`ollama/mistral:latest`)
4. **Current:** Dual provider system
   - Primary: Cerebras (`cerebras/llama3.1-8b`)
   - Backup: Ollama (`ollama/mistral:latest`)

### Configuration Method

**Dynamic Selection:**
- No code changes required to switch providers
- Just edit `LLM_PROVIDER` in `.env` file
- System automatically loads correct model configuration

**Benefits:**
- Flexibility for different environments
- Cost optimization (use free Cerebras for dev)
- Privacy option (use local Ollama for sensitive data)
- No internet requirement (Ollama backup)

---

## System Requirements

**Minimum:**
- OS: Windows 10/11
- Python: 3.10 - 3.13
- RAM: 8GB (16GB recommended for Ollama)
- Storage: 2GB for dependencies + models
- Internet: Required for Cerebras, optional for Ollama

**Recommended Hardware:**
- Asus TUF F15 or similar laptop
- No dedicated GPU required
- CPU: Modern multi-core processor
- SSD for faster model loading (Ollama)

---

## Key Files for GPT Context

If providing context to another LLM, these files are most critical:

1. `src/systemm/crew.py` - Agent orchestration logic
2. `src/systemm/main.py` - Entry point and execution flow
3. `src/systemm/config/agents.yaml` - Agent definitions
4. `src/systemm/config/tasks.yaml` - Task definitions
5. `src/systemm/tools/*.py` - Custom tool implementations
6. `dashboard/app.py` - Web dashboard backend
7. `.env.example` - Configuration template
8. `requirements.txt` - Dependencies
9. This file (`PROJECT_CONTEXT.md`) - Complete overview

---

## Development Notes

### Adding New Agents

1. Define agent in `config/agents.yaml`
2. Add agent method in `crew.py` with `@agent` decorator
3. Assign tools and LLM configuration
4. Update `llm_models` dictionary with model choice

### Adding New Tools

1. Create new file in `src/systemm/tools/`
2. Inherit from `BaseTool`
3. Define input schema with Pydantic
4. Implement `_run()` method
5. Import and assign to agents in `crew.py`

### Switching LLM Models

Edit the model strings in `crew.py`:
```python
# For Cerebras
"agent_name": "cerebras/llama3.1-70b"  # or llama3.1-8b

# For Ollama  
"agent_name": "ollama/mistral:latest"  # or any Ollama model
```

---

## Summary for GPT

**Project Type:** Multi-agent AI system for automotive predictive maintenance  
**Framework:** CrewAI with 7 specialized agents  
**LLM:** Cerebras API (primary) or local Ollama (backup)  
**Purpose:** Analyze vehicle data, predict failures, engage customers, schedule maintenance  
**Output:** JSON business intelligence report displayed in Flask dashboard  
**Key Feature:** Dynamic LLM provider switching via environment variables  
**Target Hardware:** Laptops without GPU (optimized for Asus TUF F15)  
**Setup Time:** <10 minutes with Cerebras API  
**Execution Time:** 2-5 minutes per workflow run

This system demonstrates enterprise-grade AI agent orchestration for real-world automotive applications, with flexibility for cloud (Cerebras) or local (Ollama) execution based on privacy, cost, and performance requirements.
