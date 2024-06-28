from flask import Blueprint, request, jsonify, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.services.user_service import create_user, verify_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = create_user(data['username'], data['password'])
        return jsonify({'message': 'User created successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = verify_user(data['username'], data['password'])
        if user:
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    try:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
