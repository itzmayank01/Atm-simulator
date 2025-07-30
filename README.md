# 🏦 ATM Simulator - SecureBank

A professional, full-featured ATM simulation website built with Flask, HTML, CSS, and JavaScript. This project simulates real ATM operations with secure authentication, transaction processing, and a polished user interface.

![ATM Simulator](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🔐 Security & Authentication
- **Secure PIN Authentication**: Hashed PIN storage using bcrypt
- **Session Management**: Secure user sessions with Flask
- **Input Validation**: Comprehensive frontend and backend validation
- **Protection**: SQL injection and XSS protection

### 💰 ATM Operations
- **Balance Inquiry**: Real-time balance checking with transaction logging
- **Cash Withdrawal**: Support for predefined and custom amounts
- **Cash Deposit**: Multiple deposit options with instant balance updates
- **Transaction History**: Detailed transaction logs with timestamps

### 🎨 User Interface
- **Professional Design**: Modern ATM-like interface with animations
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Interactive Keypad**: Functional numeric keypad for authentic ATM experience
- **Loading States**: Smooth transitions and loading indicators
- **Modal Alerts**: Professional success/error notifications

### 🛠 Technical Features
- **RESTful API**: Clean API endpoints for all operations
- **Database**: SQLite database with SQLAlchemy ORM
- **Error Handling**: Comprehensive error handling and user feedback
- **Security**: Environment variables for sensitive configuration
- **Modular Code**: Clean, maintainable, and extensible codebase

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   # If you have the files, navigate to the project directory
   cd atm-simulator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   - Navigate to: `http://localhost:5000`
   - The ATM interface will load automatically

## 🏃‍♂️ How to Use

### Demo Accounts
The application comes with pre-configured demo accounts:

| Account Number | PIN  | Name        | Initial Balance |
|---------------|------|-------------|-----------------|
| 1234567890    | 1234 | John Doe    | $1,500.00      |
| 9876543210    | 5678 | Jane Smith  | $2,750.50      |
| 5555666677    | 9999 | Bob Johnson | $890.25        |

### Basic Operations

1. **Login**
   - Enter a 10-digit account number
   - Enter a 4-digit PIN
   - Click LOGIN or press Enter

2. **Check Balance**
   - Click "Balance Inquiry" from the main menu
   - View current balance and account details

3. **Withdraw Money**
   - Click "Cash Withdrawal"
   - Select a predefined amount or enter a custom amount
   - Confirm the transaction

4. **Deposit Money**
   - Click "Cash Deposit"
   - Select a predefined amount or enter a custom amount
   - Confirm the transaction

5. **View History**
   - Click "Transaction History"
   - View your last 10 transactions

6. **Logout**
   - Click "LOGOUT" from the main menu
   - Or press ESC key twice

### Keyboard Shortcuts
- **Enter**: Login or confirm operations
- **ESC**: Go back or logout
- **Number keys**: Work with the virtual keypad
- **Tab**: Navigate between input fields

## 📁 Project Structure

```
atm-simulator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # ATM styling
│   └── js/
│       └── script.js     # ATM functionality
└── atm.db                # SQLite database (created automatically)
```

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///atm.db
FLASK_ENV=development
```

### Database
The application uses SQLite for simplicity. The database is created automatically when you first run the application.

**Tables:**
- `user`: Stores user account information and balances
- `transaction`: Logs all ATM transactions

## 🛡 Security Features

- **Password Hashing**: PINs are hashed using bcrypt
- **Session Security**: Secure session management
- **Input Validation**: Both frontend and backend validation
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **XSS Protection**: Input sanitization and validation

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main ATM interface |
| `/api/login` | POST | User authentication |
| `/api/logout` | POST | User logout |
| `/api/balance` | GET | Get account balance |
| `/api/withdraw` | POST | Process withdrawal |
| `/api/deposit` | POST | Process deposit |
| `/api/transactions` | GET | Get transaction history |

## 🎯 Customization

### Adding New Users
You can add new users by modifying the `init_db()` function in `app.py` or by using the Flask shell:

```python
from app import app, db, User
with app.app_context():
    user = User(
        account_number='1111222233',
        full_name='Your Name',
        balance=1000.00
    )
    user.set_pin('1111')
    db.session.add(user)
    db.session.commit()
```

### Styling
Modify `static/css/style.css` to customize the appearance:
- Colors and themes
- Animations and transitions
- Layout and spacing
- Mobile responsiveness

### Features
Extend functionality by:
- Adding new transaction types
- Implementing transfer between accounts
- Adding account statements
- Creating admin panel

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using a production database (PostgreSQL, MySQL)
- Implementing HTTPS
- Setting strong environment variables

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

## 🧪 Testing

Test the application with the demo accounts:

1. **Login Test**: Try all three demo accounts
2. **Balance Test**: Check balance inquiry functionality
3. **Withdrawal Test**: Test various withdrawal amounts
4. **Deposit Test**: Test various deposit amounts
5. **History Test**: Perform transactions and check history
6. **Error Handling**: Try invalid inputs and operations

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process using port 5000
   sudo kill -9 $(sudo lsof -t -i:5000)
   ```

2. **Module not found**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   ```

3. **Database errors**
   ```bash
   # Delete and recreate database
   rm atm.db
   python app.py
   ```

4. **Permission errors**
   ```bash
   # Check file permissions
   chmod 755 app.py
   ```

## 📈 Performance

- **Database**: Uses SQLite with connection pooling
- **Frontend**: Optimized CSS and JavaScript
- **API**: Efficient JSON responses
- **Caching**: Static file caching enabled

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework for the backend
- Font Awesome for icons
- Modern CSS techniques for styling
- Professional ATM design inspiration

---

**Note**: This is a simulation for educational and demonstration purposes. Do not use in production environments without proper security audits and enhancements.