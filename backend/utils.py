import secrets
from flask import request, jsonify
from functools import wraps
from models import get_user_by_token

def generate_token(card_number):
    # For demo: token is card_number + random hex
    return f"{card_number}-{secrets.token_hex(8)}"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401
        token = auth.split(' ', 1)[1]
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(user, *args, **kwargs)
    return decorated