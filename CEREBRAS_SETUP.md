# 🚀 Cerebras API Setup Guide (Recommended for Asus TUF F15)

## Why Cerebras?

✅ **FREE Tier Available** - No credit card required  
✅ **Fast Inference** - Powered by Cerebras CS-2 chips  
✅ **No GPU Required** - Perfect for your Asus TUF F15  
✅ **70B Parameter Model** - More capable than local 1B/7B models  
✅ **CrewAI Compatible** - Works seamlessly via LiteLLM  

## Quick Setup

### 1. Get Your Free Cerebras API Key

1. Visit [https://cloud.cerebras.ai/](https://cloud.cerebras.ai/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your key (starts with `csk-...`)

### 2. Configure Environment Variables

Copy the example file:
```powershell
cd c:\t_thon_latestt\EY_Techathon
copy .env.example .env
```

Edit `.env` and add your Cerebras API key:
```env
LLM_PROVIDER=cerebras
CEREBRAS_API_KEY=csk-your-actual-key-here
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

This includes `python-dotenv` for loading `.env` files.

### 4. Run Your AI Workflow 🎉

```powershell
python src\systemm\main.py run
```

## Provider Configuration

The system now supports **two providers** with automatic switching:

### Primary: Cerebras (Default)

```env
LLM_PROVIDER=cerebras
CEREBRAS_API_KEY=your_key_here
```

All agents use: `cerebras/llama3.1-70b`

**Benefits:**
- ⚡ Super fast inference
- 🧠 70B parameter model
- 🆓 Free tier available
- ☁️ Cloud-based (no local resources)

### Backup: Ollama (Local)

```env
LLM_PROVIDER=ollama
```

All agents use: `ollama/mistral:latest`

**Benefits:**
- 🔒 Fully private
- 📡 Works offline
- 💰 Zero API costs
- 🔧 Full control

**Requirements:**
```powershell
# Install Ollama
# Download from: https://ollama.ai/download

# Pull the model
ollama pull mistral:latest
```

## Switching Between Providers

Just change `LLM_PROVIDER` in your `.env` file:

```env
# Use Cerebras (recommended)
LLM_PROVIDER=cerebras

# OR use local Ollama (backup)
LLM_PROVIDER=ollama
```

No code changes needed! 🎯

## Running the Workflow

### With Cerebras (Recommended)

```powershell
# 1. Ensure .env is configured with Cerebras key
# 2. Run the workflow
python src\systemm\main.py run

# 3. Start dashboard (in new terminal)
python dashboard\app.py

# 4. Open browser
# http://localhost:5000
```

**Expected Runtime:** 2-5 minutes (much faster than local models!)

### With Ollama (Backup)

```powershell
# 1. Change LLM_PROVIDER=ollama in .env
# 2. Ensure Ollama is running and model is pulled
ollama pull mistral:latest

# 3. Run the workflow
python src\systemm\main.py run
```

**Expected Runtime:** 10-20 minutes (local processing)

## Model Comparison

| Feature | Cerebras (llama3.1-70b) | Ollama (mistral:latest) |
|---------|-------------------------|-------------------------|
| **Parameters** | 70 billion | 7 billion |
| **Speed** | ⚡⚡⚡⚡⚡ Very Fast | ⚡⚡ Medium |
| **Quality** | 🌟🌟🌟🌟🌟 Excellent | 🌟🌟🌟 Good |
| **Cost** | 🆓 Free tier | 🆓 Free |
| **Internet** | ✅ Required | ❌ Not required |
| **Privacy** | ☁️ Cloud | 🔒 Local |
| **GPU Required** | ❌ No | ❌ No (CPU works) |

## Troubleshooting

### Cerebras API Key Not Working

```powershell
# Check if .env file is loaded
# Add debug print to crew.py:
print(f"Using LLM Provider: {llm_provider}")
print(f"Cerebras API Key: {os.getenv('CEREBRAS_API_KEY')[:10]}...")
```

### Rate Limit Errors

Cerebras free tier has limits. If you hit them:
1. Wait a few minutes
2. Or switch to Ollama temporarily:
   ```env
   LLM_PROVIDER=ollama
   ```

### Import Error: dotenv

```powershell
pip install python-dotenv
```

### .env File Not Found

Create it from the example:
```powershell
copy .env.example .env
# Then edit .env with your actual API key
```

## Files Modified

The following files were updated to support dual providers:

- [crew.py](file:///c:/t_thon_latestt/EY_Techathon/src/systemm/crew.py) - Dynamic provider selection
- [requirements.txt](file:///c:/t_thon_latestt/EY_Techathon/requirements.txt) - Added python-dotenv
- [.env.example](file:///c:/t_thon_latestt/EY_Techathon/.env.example) - Configuration template
- `.env` - Your actual configuration (gitignored)

## Security Notes

> [!WARNING]
> **Never commit `.env` to git!** It contains your API key.

The `.env` file is automatically ignored by git. Only share `.env.example`.

## Performance Tips

### For Fastest Results (Cerebras)
- Use Cerebras during development
- Benefit from cloud-scale hardware
- No local resource usage

### For Privacy/Offline (Ollama)
- Use Ollama for sensitive data
- Works without internet
- Full control over inference

## Next Steps

1. ✅ Get Cerebras API key (free)
2. ✅ Add key to `.env` file
3. ✅ Run `python src\systemm\main.py run`
4. ✅ Enjoy fast, free AI inference!

**Questions?** Check the main [RUN_INSTRUCTIONS.md](file:///c:/t_thon_latestt/EY_Techathon/RUN_INSTRUCTIONS.md) for more details.
