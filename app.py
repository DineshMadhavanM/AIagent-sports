from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from config import config
import os
import logging
from datetime import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__, static_folder='static')
    
    # Apply configuration
    app.config.from_object(config[config_name])
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    from routes import api as api_blueprint
    app.register_blueprint(api_blueprint.bp, url_prefix='/api')
    
    # Root route
    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Request logging
    @app.before_request
    def log_request():
        app.logger.info(f"Request: {request.method} {request.path}")
    
    # Error handling
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}', exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.'
        }), 500
    
    # Health check endpoint with more details
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': config_name,
            'debug': app.config['DEBUG'],
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
        
    # New endpoint for sports statistics
    @app.route('/api/stats', methods=['GET'])
    @limiter.limit("10 per minute")
    def get_sports_stats():
        """Get sports statistics with filtering options"""
        sport = request.args.get('sport', 'cricket')
        stat_type = request.args.get('type', 'overview')
        
        # In a real app, this would query a database or external API
        stats = {
            'sport': sport,
            'type': stat_type,
            'data': {
                'last_updated': datetime.utcnow().isoformat(),
                'source': 'Sports Agent API'
            }
        }
        
        return jsonify(stats)
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'default'))
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG'],
        threaded=True
    )
