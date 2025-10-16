# 🚗 Automotive Predictive Maintenance Dashboard - Complete

## ✅ What's Been Created

### **Frontend (HTML/CSS/JavaScript)**
- **`index.html`**: Modern, responsive dashboard with 6 main tabs
- **`styles.css`**: Beautiful styling with gradients, animations, and mobile responsiveness
- **`script.js`**: Interactive functionality with filtering, modals, and real-time updates

### **Backend (Flask API)**
- **`app.py`**: RESTful API server with 10+ endpoints
- **`requirements.txt`**: Python dependencies (Flask, Flask-CORS)
- **`start_dashboard.py`**: Easy startup script with dependency checking

### **Data & Integration**
- **`sample-data.json`**: Comprehensive sample data for demonstration
- **`README.md`**: Complete documentation and setup instructions
- **Backend integration**: Ready to connect with your CrewAI system

## 🎯 Dashboard Features

### **6 Main Sections:**

1. **📊 Overview Tab**
   - Executive summary with key metrics
   - Fleet health status visualization
   - Recent alerts and notifications
   - Service center status

2. **🚗 Fleet Health Tab**
   - Vehicle-by-vehicle monitoring
   - Real-time sensor readings
   - Interactive filtering (priority, status)
   - Detailed vehicle modal popups

3. **🧠 Failure Predictions Tab**
   - AI-powered component failure predictions
   - Probability scores and confidence levels
   - Time-to-failure estimates
   - Risk severity classifications

4. **📅 Service Scheduling Tab**
   - Appointment management
   - Service center coordination
   - Schedule optimization tools
   - Calendar view

5. **🔧 Quality Insights Tab**
   - RCA/CAPA analysis results
   - Manufacturing quality trends
   - Supplier assessments
   - Design improvement recommendations

6. **📈 Analytics Tab**
   - Performance metrics
   - Cost analysis
   - Customer engagement data
   - Service quality trends

## 🚀 How to Run

### **Quick Start:**
```bash
cd dashboard
python start_dashboard.py
```

### **Manual Start:**
```bash
cd dashboard
pip install -r requirements.txt
python app.py
```

### **With CrewAI Integration:**
```bash
export OPENROUTER_API_KEY=your_api_key_here
python start_dashboard.py
```

## 🌐 Access Points

- **Main Dashboard**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/health
- **Run Analysis**: Click "Run Analysis" button in dashboard

## 📊 Sample Data Included

- **10 vehicles** with realistic sensor data
- **15 failure predictions** with probability scores
- **5 service centers** across major Indian cities
- **Real-time alerts** and notifications
- **Customer engagement** metrics
- **Manufacturing quality** insights
- **Cost analysis** and performance metrics

## 🔌 API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api/dashboard` | Complete dashboard data |
| `/api/vehicles` | Vehicle fleet information |
| `/api/predictions` | Failure predictions |
| `/api/alerts` | Current alerts |
| `/api/run-analysis` | **Run CrewAI analysis** |
| `/api/health` | System health check |

## 🎨 Design Features

- **Modern UI**: Glass-morphism effects, gradients, smooth animations
- **Responsive**: Works on desktop, tablet, and mobile
- **Interactive**: Click vehicles for details, filter data, real-time updates
- **Professional**: Clean, automotive industry-appropriate design
- **Accessible**: Good contrast, readable fonts, intuitive navigation

## 🔗 Integration Status

### **✅ Ready Now:**
- Standalone dashboard with sample data
- Beautiful, professional interface
- Full API backend
- Mobile-responsive design

### **🔗 Ready for CrewAI:**
- API endpoint `/api/run-analysis` connects to your CrewAI system
- Automatic fallback to sample data if CrewAI unavailable
- Real-time data updates after analysis
- OpenRouter API key integration

## 📱 Mobile Support

The dashboard is fully responsive and works great on:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets (iPad/Android tablets)
- 💻 Desktop computers
- 🖥️ Large screens

## 🎯 Business Value

This dashboard provides:
- **Executive visibility** into fleet health and costs
- **Operational efficiency** through predictive insights
- **Customer satisfaction** via proactive maintenance
- **Cost savings** through optimized scheduling
- **Quality improvements** via manufacturing insights

## 🚀 Next Steps

1. **Run the dashboard**: `python start_dashboard.py`
2. **Set your API key**: `export OPENROUTER_API_KEY=your_key`
3. **Click "Run Analysis"** to test CrewAI integration
4. **Customize** the data sources as needed
5. **Deploy** to your preferred hosting platform

---

## 🎉 **Your dashboard is ready to impress!**

The dashboard combines beautiful design with powerful functionality, ready to showcase your automotive predictive maintenance AI system to stakeholders, customers, and investors.

