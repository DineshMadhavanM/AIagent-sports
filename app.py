from flask import Flask, render_template, jsonify
from flask_cors import CORS
from config import config
import os

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__, static_folder='static')
    
    # Apply configuration
    app.config.from_object(config[config_name])
    
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
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': config_name,
            'debug': app.config['DEBUG']
        })
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'default'))
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG'],
        threaded=True
    )
