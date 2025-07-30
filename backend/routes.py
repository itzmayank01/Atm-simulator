from flask import Blueprint, request, jsonify
from models import users_db, authenticate_user, get_user_by_token
from utils import generate_token, require_auth
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    card_number = data.get('card_number')
    pin = data.get('pin')
    user = authenticate_user(card_number, pin)
    if user:
        token = generate_token(user['card_number'])
        user['token'] = token
        return jsonify({
            'token': token,
            'name': user['name']
        })
    return jsonify({'error': 'Invalid card number or PIN'}), 401

@api_bp.route('/balance', methods=['GET'])
@require_auth
def balance(user):
    return jsonify({'balance': user['balance']})

@api_bp.route('/withdraw', methods=['POST'])
@require_auth
def withdraw(user):
    data = request.get_json()
    amount = float(data.get('amount', 0))
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    if user['balance'] < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    user['balance'] -= amount
    user['history'].append({
        'type': 'Withdraw',
        'amount': amount,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    return jsonify({'balance': user['balance']})

@api_bp.route('/deposit', methods=['POST'])
@require_auth
def deposit(user):
    data = request.get_json()
    amount = float(data.get('amount', 0))
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    user['balance'] += amount
    user['history'].append({
        'type': 'Deposit',
        'amount': amount,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    return jsonify({'balance': user['balance']})

@api_bp.route('/history', methods=['GET'])
@require_auth
def history(user):
    return jsonify({'history': user['history']})