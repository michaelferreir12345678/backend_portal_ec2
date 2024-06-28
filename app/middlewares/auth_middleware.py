# /app/middlewares/auth_middleware.py

from functools import wraps
from flask import request, jsonify
from app.services.user_service import verify_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            current_user = verify_token(token)
            if not current_user:
                return jsonify({'message': 'Token is invalid!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)  # Passa os argumentos para a função decorada
    return decorated
