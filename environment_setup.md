# Environment Setup for Automotive Predictive Maintenance AI System

## Required API Keys

### 1. OpenRouter API Key (REQUIRED - Already provided)
```bash
OPENROUTER_API_KEY=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
```
- **Purpose**: Powers all 7 AI agents with DeepSeek model
- **Status**: ✅ Provided and configured
- **Cost**: Free tier available

### 2. Iternio API Key (OPTIONAL - For real EV route optimization)
```bash
ITERNIO_API_KEY=your_iternio_api_key_here
```
- **Purpose**: Real electric vehicle route planning and charging station optimization
- **Get it from**: https://iternio.com/api/
- **Status**: Currently using simulation mode
- **Cost**: Free tier available for basic usage

### 3. Telematics API Key (OPTIONAL - For real vehicle data)
```bash
TELEMATICS_API_KEY=your_telematics_api_key_here
TELEMATICS_API_URL=https://your-telematics-api.com
```
- **Purpose**: Real-time vehicle sensor data instead of simulation
- **Status**: Currently using realistic simulation data
- **Cost**: Depends on your telematics provider

## Current System Status

### ✅ Working with Simulation Data:
- **Vehicle Telematics**: Realistic simulated data for 10 vehicles (VEH001-VEH010)
- **Service Centers**: Simulated Indian service center network
- **Customer Notifications**: Simulated SMS/email/app notifications
- **Maintenance History**: Simulated historical data

### 🔄 Can be Enhanced with Real APIs:
- **Iternio Route Optimization**: Real EV charging stations and route planning
- **Real Telematics**: Live vehicle sensor data
- **Real Notifications**: Actual SMS/email delivery

## Setup Instructions

1. **Create `.env` file** in project root:
```bash
cp environment_setup.md .env
# Then edit .env with your actual API keys
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the system**:
```bash
python src/automotive_predictive_maintenance_ai_system/main.py run
```

## API Key Requirements Summary

| API | Required | Status | Purpose |
|-----|----------|--------|---------|
| OpenRouter | ✅ YES | ✅ Configured | AI Agent Models |
| Iternio | ❌ Optional | ⚠️ Simulation | EV Route Planning |
| Telematics | ❌ Optional | ⚠️ Simulation | Vehicle Data |
| Notification | ❌ Optional | ⚠️ Simulation | SMS/Email |

**Total Required**: 1 API key (OpenRouter) - Already provided!
