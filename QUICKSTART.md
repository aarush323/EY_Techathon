# Quick Start Guide - AI Workflow

## 🌟 1st Choice: Perplexity API (Recommended)

**Best quality with real-time web search!**

```powershell
# 1. Get API key from https://www.perplexity.ai/settings/api

# 2. Copy and configure .env
copy .env.example .env
# Edit .env and add your PERPLEXITY_API_KEY
# Set LLM_PROVIDER=perplexity

# 3. Install dependencies
cd c:\t_thon_latestt\EY_Techathon
pip install -r requirements.txt
```

## 💡 2nd Choice: Cerebras API (FREE)

**Free tier, fast inference, no GPU required!**

```powershell
# 1. Get free API key from https://cloud.cerebras.ai/

# 2. Edit .env
# Add your CEREBRAS_API_KEY
# Set LLM_PROVIDER=cerebras

# 3. Install dependencies
pip install -r requirements.txt
```

## ⚡ 3rd Choice: Local Ollama (Backup)

```powershell
# 1. Install Ollama (first time only)
# Download from: https://ollama.ai/download

# 2. Pull the model
ollama pull mistral:latest

# 3. Set provider in .env
# LLM_PROVIDER=ollama

# 4. Install dependencies
cd c:\t_thon_latestt\EY_Techathon
pip install -r requirements.txt
```

## 🚀 Run the AI Workflow

```powershell
# Terminal 1: Run the AI agents
cd c:\t_thon_latestt\EY_Techathon
python src\systemm\main.py run
```

**This will:**
- Process vehicle data with 7 AI agents
- Generate predictive maintenance insights
- Save report to `src\systemm\crew_report.json`
- Take 5-15 minutes to complete

## 📊 View Results in Dashboard

```powershell
# Terminal 2: Start dashboard server
cd c:\t_thon_latestt\EY_Techathon
python dashboard\app.py
```

Then open: **http://localhost:5000**

## 📚 Full Documentation

See [RUN_INSTRUCTIONS.md](file:///c:/t_thon_latestt/EY_Techathon/RUN_INSTRUCTIONS.md) for:
- Detailed troubleshooting
- Advanced commands
- Model alternatives
- System requirements
