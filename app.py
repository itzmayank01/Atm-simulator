from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///atm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(10), unique=True, nullable=False)
    pin_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def set_pin(self, pin):
        self.pin_hash = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_pin(self, pin):
        return bcrypt.checkpw(pin.encode('utf-8'), self.pin_hash.encode('utf-8'))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'deposit', 'withdrawal', 'balance_inquiry'
    amount = db.Column(db.Float, nullable=True)
    balance_after = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        account_number = data.get('account_number')
        pin = data.get('pin')
        
        if not account_number or not pin:
            return jsonify({'success': False, 'message': 'Account number and PIN are required'}), 400
        
        user = User.query.filter_by(account_number=account_number).first()
        
        if user and user.check_pin(pin):
            session['user_id'] = user.id
            session['account_number'] = user.account_number
            
            # Log balance inquiry
            transaction = Transaction(
                user_id=user.id,
                transaction_type='login',
                balance_after=user.balance,
                description='User login'
            )
            db.session.add(transaction)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'full_name': user.full_name,
                    'account_number': user.account_number,
                    'balance': user.balance
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid account number or PIN'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred during login'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/balance', methods=['GET'])
def get_balance():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in first'}), 401
    
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Log balance inquiry
        transaction = Transaction(
            user_id=user.id,
            transaction_type='balance_inquiry',
            balance_after=user.balance,
            description='Balance inquiry'
        )
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'balance': user.balance,
            'account_number': user.account_number
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in first'}), 401
    
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Invalid withdrawal amount'}), 400
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if user.balance < amount:
            return jsonify({'success': False, 'message': 'Insufficient funds'}), 400
        
        # Process withdrawal
        user.balance -= amount
        
        # Log transaction
        transaction = Transaction(
            user_id=user.id,
            transaction_type='withdrawal',
            amount=amount,
            balance_after=user.balance,
            description=f'Cash withdrawal: ${amount:.2f}'
        )
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully withdrew ${amount:.2f}',
            'new_balance': user.balance,
            'transaction_id': transaction.id
        })
        
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred during withdrawal'}), 500

@app.route('/api/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in first'}), 401
    
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Invalid deposit amount'}), 400
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Process deposit
        user.balance += amount
        
        # Log transaction
        transaction = Transaction(
            user_id=user.id,
            transaction_type='deposit',
            amount=amount,
            balance_after=user.balance,
            description=f'Cash deposit: ${amount:.2f}'
        )
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully deposited ${amount:.2f}',
            'new_balance': user.balance,
            'transaction_id': transaction.id
        })
        
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred during deposit'}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in first'}), 401
    
    try:
        limit = request.args.get('limit', 10, type=int)
        transactions = Transaction.query.filter_by(user_id=session['user_id'])\
            .order_by(Transaction.timestamp.desc())\
            .limit(limit).all()
        
        transaction_list = []
        for trans in transactions:
            transaction_list.append({
                'id': trans.id,
                'type': trans.transaction_type,
                'amount': trans.amount,
                'balance_after': trans.balance_after,
                'timestamp': trans.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'description': trans.description
            })
        
        return jsonify({
            'success': True,
            'transactions': transaction_list
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if sample users already exist
        if User.query.count() == 0:
            # Create sample users
            users_data = [
                {'account_number': '1234567890', 'pin': '1234', 'full_name': 'John Doe', 'balance': 1500.00},
                {'account_number': '9876543210', 'pin': '5678', 'full_name': 'Jane Smith', 'balance': 2750.50},
                {'account_number': '5555666677', 'pin': '9999', 'full_name': 'Bob Johnson', 'balance': 890.25},
            ]
            
            for user_data in users_data:
                user = User(
                    account_number=user_data['account_number'],
                    full_name=user_data['full_name'],
                    balance=user_data['balance']
                )
                user.set_pin(user_data['pin'])
                db.session.add(user)
            
            db.session.commit()
            print("Sample users created successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)