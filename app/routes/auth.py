# /app/routes/auth.py

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.models.user import User
from app.services.user_service import create_user, verify_user, verify_token
from app.middlewares.auth_middleware import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = create_user(data['username'], data['password'])
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = verify_user(data['username'], data['password'])
    if user:
        token = user.get_token()
        return jsonify({
            'token': token,  # Token is already in string format
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'id': current_user.id,
        'username': current_user.username
    }), 200
