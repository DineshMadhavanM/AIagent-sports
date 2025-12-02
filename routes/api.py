from flask import jsonify, request, make_response
from .. import app
from ..services.sports_agent_service import handle_agent_query

@app.route('/api/query', methods=['POST', 'OPTIONS'])
def query():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200

    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    return handle_agent_query()
