#!/usr/bin/env python3
"""
Simple test server to verify Flask is working
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .success { color: #28a745; font-size: 24px; font-weight: bold; }
            .info { color: #17a2b8; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 Automotive Predictive Maintenance System</h1>
            <p class="success">✅ Server is Running Successfully!</p>
            <p>Your Flask server is working correctly.</p>
            <div class="info">
                <h3>Next Steps:</h3>
                <ol>
                    <li>This confirms your Python/Flask setup is working</li>
                    <li>Now let's start the full dashboard</li>
                    <li>Press Ctrl+C to stop this test server</li>
                </ol>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/api/test')
def api_test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'server': 'Flask Test Server'
    })

if __name__ == '__main__':
    print("🧪 Starting Test Server...")
    print("🌐 Test page: http://localhost:5000")
    print("🔧 API test: http://localhost:5000/api/test")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)

