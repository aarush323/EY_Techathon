#!/usr/bin/env python3
from flask import Flask, jsonify, send_from_directory
import json
import os
from datetime import datetime

# Current folder (dashboard/) for serving static files
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
app = Flask(__name__, static_folder=src_dir)

# Path to the report in src/systemm/
REPORT_FILE = os.path.join(src_dir, 'systemm', 'crew_report.json')

def load_json_file(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Serve HTML pages
@app.route('/')
def index():
    return send_from_directory(os.path.join(src_dir, 'pages'), 'index.html')

@app.route('/<page_name>')
def serve_page(page_name):
    # Handle both /page and /page.html
    if not page_name.endswith('.html'):
        page_name += '.html'
    return send_from_directory(os.path.join(src_dir, 'pages'), page_name)

# Serve static assets (JS, CSS)
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(src_dir, 'js'), filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(src_dir, 'css'), filename)

# API routes
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
