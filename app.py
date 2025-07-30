from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # In production, use a secure random key

# Simulated user database (account: {pin, balance, history})
USERS = {
    '123456': {
        'pin': '1234',
        'balance': 1000.0,
        'history': []
    },
    '654321': {
        'pin': '4321',
        'balance': 500.0,
        'history': []
    }
}

# Helper functions

def get_user():
    account = session.get('account')
    if account and account in USERS:
        return USERS[account]
    return None

def add_history(user, txn_type, amount):
    user['history'].insert(0, {
        'type': txn_type,
        'amount': amount,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# Routes

@app.route('/', methods=['GET'])
def home():
    if 'account' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        account = request.form['account']
        pin = request.form['pin']
        user = USERS.get(account)
        if user and user['pin'] == pin:
            session['account'] = account
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid account or PIN.'
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    message = request.args.get('message')
    error = request.args.get('error')
    return render_template('dashboard.html', user={'account': session['account'], 'balance': user['balance']}, message=message, error=error)

@app.route('/withdraw', methods=['POST'])
def withdraw():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    try:
        amount = float(request.form['amount'])
        if amount <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for('dashboard', error='Invalid amount.'))
    if user['balance'] < amount:
        return redirect(url_for('dashboard', error='Insufficient funds.'))
    user['balance'] -= amount
    add_history(user, 'Withdrawal', amount)
    return redirect(url_for('dashboard', message='Withdrawal successful.'))

@app.route('/deposit', methods=['POST'])
def deposit():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    try:
        amount = float(request.form['amount'])
        if amount <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for('dashboard', error='Invalid amount.'))
    user['balance'] += amount
    add_history(user, 'Deposit', amount)
    return redirect(url_for('dashboard', message='Deposit successful.'))

@app.route('/history', methods=['GET'])
def history():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    return render_template('history.html', history=user['history'])

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('account', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)