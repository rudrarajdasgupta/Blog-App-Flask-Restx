from functools import wraps
from flask import request, jsonify
from models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        user = User.verify_jwt(token)
        if not user:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(user, *args, **kwargs)
    return decorated