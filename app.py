from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from sports_agent import SportsAgent
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Initialize the agent with Gemini provider and the provided API key
GEMINI_API_KEY = "AIzaSyDIH2SW1sXh-jy9I_CxV7ujpjIJMdsIhII"
agent = SportsAgent(provider='gemini', api_key=GEMINI_API_KEY)

@app.after_request
def after_request(response):
    # Add CORS headers to all responses
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST', 'OPTIONS'])
def handle_query():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200

    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
            
        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
            
        response = agent.respond(query)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
