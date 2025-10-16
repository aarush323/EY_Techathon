# Automotive Predictive Maintenance Dashboard

A modern, responsive web dashboard for visualizing automotive predictive maintenance data and insights.

## Features

### 📊 **Interactive Dashboard**
- **Overview Tab**: Executive summary with key metrics and fleet status
- **Fleet Health**: Real-time vehicle monitoring with detailed sensor data
- **Failure Predictions**: AI-powered component failure predictions
- **Service Scheduling**: Appointment management and optimization
- **Quality Insights**: Manufacturing quality analysis and RCA/CAPA insights
- **Analytics**: Performance metrics and cost analysis

### 🎨 **Modern UI/UX**
- Responsive design that works on desktop, tablet, and mobile
- Beautiful gradient backgrounds and glass-morphism effects
- Smooth animations and transitions
- Interactive charts and visualizations
- Real-time data updates

### 🔧 **Technical Features**
- RESTful API backend with Flask
- Sample data for demonstration
- Integration ready for CrewAI system
- CORS enabled for frontend-backend communication
- Error handling and loading states

## Quick Start

### 1. Install Dependencies
```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)
```bash
# For CrewAI integration
export OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Run the Dashboard
```bash
python app.py
```

### 4. Access the Dashboard
Open your browser and navigate to: **http://localhost:5000**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/api/dashboard` | GET | Complete dashboard data |
| `/api/vehicles` | GET | Vehicle fleet data |
| `/api/vehicles/<id>` | GET | Specific vehicle details |
| `/api/predictions` | GET | Failure predictions |
| `/api/alerts` | GET | Current alerts |
| `/api/service-centers` | GET | Service center information |
| `/api/appointments` | GET | Scheduled appointments |
| `/api/quality-insights` | GET | Manufacturing quality insights |
| `/api/analytics` | GET | Performance analytics |
| `/api/run-analysis` | GET | Run CrewAI analysis |
| `/api/health` | GET | Health check |

## Dashboard Structure

```
dashboard/
├── index.html          # Main dashboard HTML
├── styles.css          # CSS styling and animations
├── script.js           # JavaScript functionality
├── sample-data.json    # Sample data for demonstration
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Sample Data

The dashboard comes with comprehensive sample data including:

- **10 vehicles** with realistic sensor readings
- **Failure predictions** with probability scores
- **Service center network** across major Indian cities
- **Customer engagement** data and metrics
- **Manufacturing quality insights** and RCA/CAPA analysis
- **Cost analysis** and performance metrics

## Integration with CrewAI

The dashboard can integrate with the CrewAI predictive maintenance system:

1. **Set your OpenRouter API key**:
   ```bash
   export OPENROUTER_API_KEY=your_api_key_here
   ```

2. **Run real analysis**:
   - Navigate to the dashboard
   - The system will automatically use CrewAI if available
   - Fallback to sample data if CrewAI is not accessible

## Customization

### Adding New Data Sources
1. Update `sample-data.json` with your data structure
2. Modify the API endpoints in `app.py` if needed
3. Update the frontend JavaScript to handle new data fields

### Styling Changes
- Modify `styles.css` for visual changes
- The design uses CSS Grid and Flexbox for responsive layouts
- Color scheme can be updated by changing CSS custom properties

### Adding New Features
- Add new tabs by updating the navigation in `index.html`
- Create corresponding JavaScript functions in `script.js`
- Add new API endpoints in `app.py` as needed

## Browser Support

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Performance

- **Fast loading**: Optimized CSS and JavaScript
- **Responsive**: Works on all device sizes
- **Real-time updates**: Live data refresh capabilities
- **Efficient rendering**: Virtual scrolling for large datasets

## Security

- CORS enabled for API access
- Input validation on API endpoints
- Error handling to prevent information leakage
- No sensitive data in sample files

## Troubleshooting

### Dashboard not loading
- Check if Flask server is running on port 5000
- Verify all files are in the correct directory
- Check browser console for JavaScript errors

### API endpoints not responding
- Ensure Flask-CORS is installed: `pip install Flask-CORS`
- Check if the server is running without errors
- Verify the sample-data.json file exists and is valid

### CrewAI integration not working
- Verify OpenRouter API key is set correctly
- Check if the CrewAI system is properly installed
- Review server logs for import errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Automotive Predictive Maintenance AI System and follows the same licensing terms.

