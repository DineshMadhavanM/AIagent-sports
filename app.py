from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import logging
from datetime import datetime, timedelta
import secrets
import string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
mail = Mail()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    jwt.init_app(app)
    mail.init_app(app)
    
    # Initialize rate limiter
    limiter.init_app(app)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from routes import api as api_blueprint
    from auth import auth as auth_blueprint
    
    app.register_blueprint(api_blueprint.bp, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({"error": "Not found"}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({"error": "Internal server error"}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    # Routes
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/login')
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('login.html')
    
    @app.route('/signup')
    def signup_page():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('signup.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html', user=current_user)
    
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)
    
    # API Endpoints
    @app.route('/api/me')
    @jwt_required()
    def get_current_user():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin
        })
    
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user(user_id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify({"error": "Invalid token"}), 401
            
        if user_id != current_user_id and not current_user.is_admin:
            return jsonify({"error": "Insufficient permissions"}), 403
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None
        })
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})
    
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

# CLI Commands
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                email='admin@example.com',
                username='admin',
                first_name='Admin',
                last_name='User',
                is_admin=True,
                email_verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created with email: admin@example.com and password: admin123")
        print("Database initialized successfully!")

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'default'))
    
    # Initialize database
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )
