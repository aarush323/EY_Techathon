# LLM Provider Configuration Guide

The system supports **three LLM providers** with automatic priority-based selection.

## Provider Priority

1. **Perplexity API** (1st Choice - Recommended)
2. **Cerebras API** (2nd Choice - Free Tier)
3. **Local Ollama** (3rd Choice - Backup)

---

## 1. Perplexity API (Recommended)

### Why Perplexity?
✅ **Real-time Web Search** - Access to current information  
✅ **Powerful Models** - Sonar Pro for high-quality outputs  
✅ **Fast Inference** - Quick response times  
✅ **CrewAI Compatible** - Works seamlessly via LiteLLM  

### Setup

**Step 1: Get API Key**
1. Visit [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Sign up or log in
3. Create a new API key
4. Copy your key (starts with `pplx-...`)

**Step 2: Configure**

Edit `.env`:
```env
LLM_PROVIDER=perplexity
PERPLEXITY_API_KEY=pplx-your-actual-key-here
```

**Model Used:** `perplexity/sonar-pro`

### Pricing
- Pay-per-use model
- See [https://www.perplexity.ai/pricing](https://www.perplexity.ai/pricing) for current rates

---

## 2. Cerebras API (Free Tier)

### Why Cerebras?
✅ **FREE Tier Available** - No credit card required  
✅ **Fast Inference** - CS-2 chip acceleration  
✅ **No GPU Required** - Perfect for laptops  
✅ **Good Performance** - 8B parameter model  

### Setup

**Step 1: Get API Key**
1. Visit [https://cloud.cerebras.ai/](https://cloud.cerebras.ai/)
2. Sign up for free account
3. Navigate to API Keys
4. Create and copy your key (starts with `csk-...`)

**Step 2: Configure**

Edit `.env`:
```env
LLM_PROVIDER=cerebras
CEREBRAS_API_KEY=csk-your-actual-key-here
```

**Model Used:** `cerebras/llama3.1-8b`

### Pricing
- Free tier available
- Check current limits at [https://cloud.cerebras.ai/](https://cloud.cerebras.ai/)

---

## 3. Local Ollama (Backup)

### Why Ollama?
✅ **Fully Private** - All data stays local  
✅ **Offline Capable** - No internet required  
✅ **Zero API Costs** - Completely free forever  
✅ **Full Control** - Your own infrastructure  

### Setup

**Step 1: Install Ollama**
1. Download from [https://ollama.ai/download](https://ollama.ai/download)
2. Run installer (Windows/Mac/Linux)
3. Ollama starts automatically as background service

**Step 2: Pull Model**
```powershell
ollama pull mistral:latest
```

**Step 3: Configure**

Edit `.env`:
```env
LLM_PROVIDER=ollama
# No API key needed for Ollama
```

**Model Used:** `ollama/mistral:latest` (7B parameters)

### System Requirements
- RAM: 8GB minimum (16GB recommended)
- Storage: ~4GB for mistral model
- No GPU required (CPU works fine)

---

## Quick Comparison

| Feature | Perplexity | Cerebras | Ollama |
|---------|-----------|----------|---------|
| **Priority** | 1st Choice | 2nd Choice | 3rd Choice |
| **Model** | sonar-pro | llama3.1-8b | mistral:latest |
| **Speed** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ | ⚡⚡ |
| **Quality** | 🌟🌟🌟🌟🌟 | 🌟🌟🌟🌟 | 🌟🌟🌟 |
| **Web Search** | ✅ Yes | ❌ No | ❌ No |
| **Cost** | 💰 Pay-per-use | 🆓 Free tier | 🆓 Free |
| **Internet** | ✅ Required | ✅ Required | ❌ Not required |
| **Privacy** | ☁️ Cloud | ☁️ Cloud | 🔒 Local |
| **Setup Time** | ~2 min | ~2 min | ~5 min |

---

## Switching Providers

Simply edit your `.env` file:

```env
# Use Perplexity (1st choice - recommended)
LLM_PROVIDER=perplexity

# OR use Cerebras (2nd choice - free)
LLM_PROVIDER=cerebras

# OR use Ollama (3rd choice - local)
LLM_PROVIDER=ollama
```

**No code changes needed!** The system automatically detects and switches.

---

## Configuration File

Your `.env` file should look like this:

```env
# ==============================================
# LLM PROVIDER CONFIGURATION
# ==============================================
LLM_PROVIDER=perplexity  # or cerebras or ollama

# ==============================================
# PERPLEXITY API (1st Choice)
# ==============================================
PERPLEXITY_API_KEY=pplx-your-key-here

# ==============================================
# CEREBRAS API (2nd Choice)
# ==============================================
CEREBRAS_API_KEY=csk-your-key-here

# ==============================================
# OLLAMA (3rd Choice - Local)
# ==============================================
# No API key needed
```

---

## Troubleshooting

### Perplexity API Not Working
```powershell
# Check API key is set correctly
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('PERPLEXITY_API_KEY')[:10])"

# Verify provider is set
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('LLM_PROVIDER'))"
```

### Cerebras Rate Limits
If you hit Cerebras free tier limits:
1. Wait a few minutes, or
2. Switch to Perplexity (if you have API key), or
3. Switch to Ollama (free, local)

### Ollama Connection Issues
```powershell
# Check Ollama is running
ollama list

# Pull model again if needed
ollama pull mistral:latest

# Test model
ollama run mistral:latest "Hello"
```

---

## Running the Workflow

After configuring your preferred provider:

```powershell
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the AI workflow
python src\systemm\main.py run

# Start dashboard
python dashboard\app.py

# Open http://localhost:5000
```

---

## Recommendations

**For Production/Best Quality:**
- Use **Perplexity** (sonar-pro has web search + high quality)

**For Development/Testing:**
- Use **Cerebras** (free tier, fast, good quality)

**For Privacy/Offline:**
- Use **Ollama** (local, private, no internet needed)

**Cost Optimization:**
- Development: Cerebras (free tier)
- Production: Perplexity (pay-per-use, best quality)
- Sensitive Data: Ollama (local, private)

---

## Next Steps

1. Choose your provider based on needs
2. Get API key (for Perplexity or Cerebras)
3. Configure `.env` file
4. Run `python src\systemm\main.py run`
5. Enjoy AI-powered predictive maintenance! 🚀

For detailed setup instructions, see:
- [QUICKSTART.md](file:///c:/t_thon_latestt/EY_Techathon/QUICKSTART.md)
- [CEREBRAS_SETUP.md](file:///c:/t_thon_latestt/EY_Techathon/CEREBRAS_SETUP.md)
- [RUN_INSTRUCTIONS.md](file:///c:/t_thon_latestt/EY_Techathon/RUN_INSTRUCTIONS.md)
