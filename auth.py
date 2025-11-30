from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import datetime, timedelta
import os
import re
from functools import wraps

from app import db, mail, login_manager
from models import User
from flask_mail import Message

# Create blueprint
auth = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_token(user, expires_in=3600):
    """Generate JWT token for API authentication"""
    return create_access_token(
        identity=user.id,
        expires_delta=timedelta(seconds=expires_in)
    )

@auth.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    if not all(k in data for k in ['email', 'username', 'password']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Validate email format
    if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        username=data['username'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.set_password(data['password'])
    
    # Save to database
    db.session.add(user)
    db.session.commit()
    
    # Generate verification token
    token = user.get_reset_token()
    
    # Send verification email (in production)
    if current_app.config['ENV'] == 'production':
        send_verification_email(user.email, token)
    
    return jsonify({
        "message": "User registered successfully. Please check your email to verify your account.",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }), 201

@auth.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin
        }
    })

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": access_token})

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client should delete the token)"""
    return jsonify({"message": "Successfully logged out"})

@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        token = user.get_reset_token()
        send_reset_email(user.email, token)
    
    # Always return success to prevent email enumeration
    return jsonify({"message": "If an account exists with this email, a password reset link has been sent"})

@auth.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    """Reset password with token"""
    user = User.verify_reset_token(token)
    if not user:
        return jsonify({"error": "Invalid or expired token"}), 400
    
    new_password = request.json.get('password')
    if not new_password or len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400
    
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({"message": "Password has been reset successfully"})

def send_verification_email(email, token):
    """Send account verification email"""
    msg = Message('Verify Your Email',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    
    verification_url = url_for('auth.verify_email', token=token, _external=True)
    
    msg.body = f'''To verify your email, visit the following link:
{verification_url}

If you did not make this request, please ignore this email.
'''
    
    msg.html = f'''
    <h2>Verify Your Email</h2>
    <p>Click the button below to verify your email address:</p>
    <a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Email</a>
    <p>Or copy and paste this link into your browser:</p>
    <p>{verification_url}</p>
    <p>If you did not make this request, please ignore this email.</p>
    '''
    
    mail.send(msg)

def send_reset_email(email, token):
    """Send password reset email"""
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, please ignore this email.
'''
    
    msg.html = f'''
    <h2>Password Reset</h2>
    <p>Click the button below to reset your password:</p>
    <a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block;">Reset Password</a>
    <p>Or copy and paste this link into your browser:</p>
    <p>{reset_url}</p>
    <p>If you did not request a password reset, please ignore this email.</p>
    '''
    
    mail.send(msg)

@auth.route('/verify-email/<token>')
def verify_email(token):
    """Verify user's email with token"""
    user = User.verify_reset_token(token)
    if not user:
        return jsonify({"error": "Invalid or expired token"}), 400
    
    if user.email_verified:
        return jsonify({"message": "Email already verified"}), 200
    
    user.email_verified = True
    db.session.commit()
    
    return jsonify({"message": "Email verified successfully"})
