from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
import json
import os
from datetime import datetime

# Configuration
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'users.json')
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ----------------------
# Helper Functions
# ----------------------

def load_users():
    """Load user data from the JSON file."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return data.get('users', [])

def save_users(users):
    """Persist user data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump({'users': users}, f, indent=4)

def get_user_by_id(user_id):
    for user in load_users():
        if user['id'] == user_id:
            return user
    return None

def authenticate(user_id, pin):
    """Return user dict if credentials are valid, else None."""
    users = load_users()
    for user in users:
        if user['id'] == user_id and check_password_hash(user['pin_hash'], pin):
            return user
    return None

def add_transaction(user, transaction_type, amount):
    entry = {
        'type': transaction_type,
        'amount': amount,
        'timestamp': datetime.utcnow().isoformat()
    }
    user.setdefault('transactions', []).insert(0, entry)  # newest first

# ----------------------
# Routes
# ----------------------

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user_id = int(request.form['account'])
            pin = request.form['pin']
        except (KeyError, ValueError):
            flash('Invalid login details.', 'danger')
            return redirect(url_for('login'))

        user = authenticate(user_id, pin)
        if user:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect account or PIN.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        amount = float(request.form['amount'])
    except (KeyError, ValueError):
        flash('Invalid amount.', 'danger')
        return redirect(url_for('dashboard'))

    users = load_users()
    for user in users:
        if user['id'] == session['user_id']:
            if amount <= 0:
                flash('Amount must be positive.', 'danger')
            elif amount > user['balance']:
                flash('Insufficient balance.', 'danger')
            else:
                user['balance'] -= amount
                add_transaction(user, 'withdrawal', -amount)
                flash(f'Withdrawn ${amount:.2f}.', 'success')
            break
    save_users(users)
    return redirect(url_for('dashboard'))


@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        amount = float(request.form['amount'])
    except (KeyError, ValueError):
        flash('Invalid amount.', 'danger')
        return redirect(url_for('dashboard'))

    if amount <= 0:
        flash('Amount must be positive.', 'danger')
    else:
        users = load_users()
        for user in users:
            if user['id'] == session['user_id']:
                user['balance'] += amount
                add_transaction(user, 'deposit', amount)
                flash(f'Deposited ${amount:.2f}.', 'success')
                break
        save_users(users)
    return redirect(url_for('dashboard'))


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return jsonify(user.get('transactions', []))


if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({'users': []}, f)
    app.run(debug=True, host='0.0.0.0', port=5000)