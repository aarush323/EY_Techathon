#!/usr/bin/env python3
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

# Current folder (dashboard/) for serving static files
current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=current_dir)
CORS(app)

# Path to the report in src/system/
PROJECT_ROOT = os.path.dirname(current_dir)
REPORT_FILE = os.path.join(PROJECT_ROOT, 'src', 'systemm', 'crew_report.json')

def load_json_file(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route('/')
def index():
    return send_from_directory(current_dir, 'index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory(current_dir, 'styles.css')

@app.route('/script.js')
def script():
    return send_from_directory(current_dir, 'script.js')

@app.route('/api/dashboard')
def get_dashboard_data():
    report = load_json_file(REPORT_FILE)
    if not report:
        return jsonify({
            'report_text': 'Crew report not yet generated. Run main.py first.',
            'timestamp': datetime.now().isoformat()
        }), 503
    return jsonify(report)

@app.route('/api/run-analysis')
def run_analysis():
    return jsonify({
        'status': 'info',
        'message': 'Please run main.py manually to generate the CrewAI report.',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
