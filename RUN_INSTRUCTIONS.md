# Running the Automotive Predictive Maintenance AI System

This guide provides step-by-step instructions to run the AI agentic workflow using local Ollama LLM.

## Prerequisites

### 1. Install Ollama

**Windows:**
- Download from [https://ollama.ai/download](https://ollama.ai/download)
- Run the installer
- Ollama will start automatically as a background service

**Verification:**
```powershell
ollama --version
```

### 2. Pull the Required Model

Pull the `llama3.2:1b` model:
```powershell
ollama pull llama3.2:1b
```

**Verify the model is available:**
```powershell
ollama list
```

You should see `llama3.2:1b` in the list.

### 3. Install Python Dependencies

Navigate to the project directory:
```powershell
cd c:\t_thon_latestt\EY_Techathon
```

Install all required packages:
```powershell
pip install -r requirements.txt
```

## Running the AI Workflow

### Option 1: Run Main Script Directly

```powershell
cd c:\t_thon_latestt\EY_Techathon
python src\systemm\main.py run
```

This will:
1. Initialize all 7 AI agents (data analysis, diagnosis, customer engagement, scheduling, feedback, manufacturing insights, orchestrator)
2. Execute the predictive maintenance workflow
3. Generate a report saved to `src\systemm\crew_report.json`
4. Print the results to the terminal

### Option 2: Run with Custom Inputs

Edit `src\systemm\main.py` and modify the `inputs` dictionary in the `run()` function:
```python
inputs = {
    'oem_name': 'Your OEM Name',
    'customer_name': 'Customer Name',
    'vehicle_id': 'VEHICLE_ID_HERE'
}
```

Then run:
```powershell
python src\systemm\main.py run
```

## Viewing Results in Dashboard

### 1. Start the Flask Dashboard

In a **new terminal window**:
```powershell
cd c:\t_thon_latestt\EY_Techathon
python dashboard\app.py
```

The dashboard will start on `http://localhost:5000`

### 2. Open in Browser

Navigate to:
```
http://localhost:5000
```

The dashboard will display:
- The AI-generated maintenance report
- Timestamp of report generation
- Analysis results from all agents

## Workflow Overview

The AI system executes these tasks sequentially:

1. **Monitor Vehicle Fleet Data** (Data Analysis Agent)
   - Fetches telemetry and maintenance history
   - Analyzes vehicle health metrics

2. **Predict Component Failures** (Diagnosis Agent)
   - Uses historical data to predict failures
   - Identifies priority maintenance needs

3. **Engage Customers** (Customer Engagement Agent)
   - Creates personalized maintenance alerts
   - Sends notifications via API

4. **Schedule Appointments** (Scheduling Agent)
   - Finds nearby service centers
   - Optimizes routes using Iternio API
   - Books appointments

5. **Collect Feedback** (Feedback Agent)
   - Records service completion
   - Updates maintenance history

6. **Generate Manufacturing Insights** (Manufacturing Quality Insights Agent)
   - Analyzes patterns across fleet
   - Identifies recurring issues

7. **Create Business Intelligence Dashboard** (Master Orchestrator Agent)
   - Compiles all insights
   - Generates comprehensive report

## Troubleshooting

### Ollama Not Running
```powershell
# Check if Ollama is running
ollama list

# If not, start Ollama service (usually automatic on Windows)
# Or restart your computer
```

### Model Not Found
```powershell
# Pull the model again
ollama pull llama3.2:1b
```

### Port Already in Use (Dashboard)
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port by editing dashboard\app.py
# Change the last line to: app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Slow Performance
The `llama3.2:1b` model is lightweight, but with 7 agents running sequentially, the workflow may take several minutes. This is normal for local LLM execution.

**To speed up:**
- Reduce the number of agents (modify `crew.py`)
- Use a more powerful GPU-enabled machine
- Switch to a smaller model like `tinyllama`

## Advanced Options

### Training the Crew
```powershell
python src\systemm\main.py train <iterations> <filename>
```

### Testing the Crew
```powershell
python src\systemm\main.py test <iterations>
```

### Replay a Specific Task
```powershell
python src\systemm\main.py replay <task_id>
```

## System Requirements

- **OS:** Windows 10/11
- **Python:** 3.10 - 3.13
- **RAM:** 8GB minimum (16GB recommended)
- **Storage:** 2GB for Ollama + models
- **Ollama:** Latest version

## Questions or Issues?

Check the project documentation or review the configuration files:
- `src\systemm\config\agents.yaml` - Agent configurations
- `src\systemm\config\tasks.yaml` - Task definitions
- `src\systemm\crew.py` - Crew orchestration logic
