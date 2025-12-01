#!/usr/bin/env python3
"""
Startup script for the Automotive Predictive Maintenance Dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Flask and Flask-CORS are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def check_api_key():
    """Check if OpenRouter API key is set"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        print("✅ OpenRouter API key is set")
        return True
    else:
        print("⚠️  OpenRouter API key not set")
        print("   Set it with: export OPENROUTER_API_KEY=your_api_key_here")
        print("   Dashboard will use sample data instead")
        return False

def main():
    """Main startup function"""
    print("🚀 Automotive Predictive Maintenance Dashboard")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check API key
    check_api_key()
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the dashboard directory.")
        sys.exit(1)
    
    print("\n📊 Starting dashboard server...")
    print("🌐 Dashboard will be available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print("\n💡 Features:")
    print("   - Interactive fleet health monitoring")
    print("   - AI-powered failure predictions")
    print("   - Service scheduling optimization")
    print("   - Manufacturing quality insights")
    print("   - Real-time analytics and reporting")
    print("\n" + "=" * 50)
    
    # Start the Flask server
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

