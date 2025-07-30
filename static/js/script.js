// ATM Simulator JavaScript
class ATMSimulator {
    constructor() {
        this.currentUser = null;
        this.currentScreen = 'login-screen';
        this.activeInput = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.showScreen('login-screen');
    }

    bindEvents() {
        // Login button
        document.getElementById('login-btn').addEventListener('click', () => this.handleLogin());

        // Logout button
        document.getElementById('logout-btn').addEventListener('click', () => this.handleLogout());

        // Menu buttons
        document.querySelectorAll('.menu-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.getAttribute('data-action');
                this.handleMenuAction(action);
            });
        });

        // Back buttons
        document.querySelectorAll('.back-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const screen = e.currentTarget.getAttribute('data-screen');
                this.showScreen(screen);
            });
        });

        // Amount buttons for withdrawal
        document.querySelectorAll('.amount-btn:not(.deposit-amount)').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const amount = parseFloat(e.currentTarget.getAttribute('data-amount'));
                this.handleWithdrawal(amount);
            });
        });

        // Amount buttons for deposit
        document.querySelectorAll('.deposit-amount').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const amount = parseFloat(e.currentTarget.getAttribute('data-amount'));
                this.handleDeposit(amount);
            });
        });

        // Custom withdrawal
        document.getElementById('withdraw-custom-btn').addEventListener('click', () => {
            const amount = parseFloat(document.getElementById('custom-withdraw').value);
            if (amount && amount > 0) {
                this.handleWithdrawal(amount);
            } else {
                this.showAlert('Error', 'Please enter a valid amount', 'error');
            }
        });

        // Custom deposit
        document.getElementById('deposit-custom-btn').addEventListener('click', () => {
            const amount = parseFloat(document.getElementById('custom-deposit').value);
            if (amount && amount > 0) {
                this.handleDeposit(amount);
            } else {
                this.showAlert('Error', 'Please enter a valid amount', 'error');
            }
        });

        // Keypad functionality
        document.querySelectorAll('.key-btn.number').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const number = e.currentTarget.getAttribute('data-number');
                this.handleKeypadInput(number);
            });
        });

        document.getElementById('clear-btn').addEventListener('click', () => this.handleClear());
        document.getElementById('enter-btn').addEventListener('click', () => this.handleEnter());

        // Input focus management
        document.getElementById('account-number').addEventListener('focus', () => {
            this.activeInput = 'account-number';
        });

        document.getElementById('pin').addEventListener('focus', () => {
            this.activeInput = 'pin';
        });

        document.getElementById('custom-withdraw').addEventListener('focus', () => {
            this.activeInput = 'custom-withdraw';
        });

        document.getElementById('custom-deposit').addEventListener('focus', () => {
            this.activeInput = 'custom-deposit';
        });

        // Enter key support
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                if (this.currentScreen === 'login-screen') {
                    this.handleLogin();
                }
            }
        });

        // Modal close
        document.getElementById('modal-ok').addEventListener('click', () => {
            this.hideAlert();
        });

        // Click outside modal to close
        document.getElementById('alert-modal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('alert-modal')) {
                this.hideAlert();
            }
        });
    }

    handleKeypadInput(number) {
        if (this.activeInput) {
            const input = document.getElementById(this.activeInput);
            if (input) {
                input.value += number;
            }
        }
    }

    handleClear() {
        if (this.activeInput) {
            const input = document.getElementById(this.activeInput);
            if (input) {
                input.value = '';
            }
        }
    }

    handleEnter() {
        if (this.currentScreen === 'login-screen') {
            this.handleLogin();
        } else if (this.currentScreen === 'withdraw-screen' && this.activeInput === 'custom-withdraw') {
            document.getElementById('withdraw-custom-btn').click();
        } else if (this.currentScreen === 'deposit-screen' && this.activeInput === 'custom-deposit') {
            document.getElementById('deposit-custom-btn').click();
        }
    }

    showScreen(screenId) {
        // Hide all screens
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });

        // Show target screen
        const targetScreen = document.getElementById(screenId);
        if (targetScreen) {
            targetScreen.classList.add('active');
            this.currentScreen = screenId;
        }

        // Update balance displays when showing withdrawal/deposit screens
        if (this.currentUser && (screenId === 'withdraw-screen' || screenId === 'deposit-screen')) {
            this.updateBalanceDisplays();
        }
    }

    showLoading() {
        this.showScreen('loading-screen');
    }

    async handleLogin() {
        const accountNumber = document.getElementById('account-number').value.trim();
        const pin = document.getElementById('pin').value.trim();

        if (!accountNumber || !pin) {
            this.showAlert('Error', 'Please enter both account number and PIN', 'error');
            return;
        }

        if (accountNumber.length !== 10) {
            this.showAlert('Error', 'Account number must be 10 digits', 'error');
            return;
        }

        if (pin.length !== 4) {
            this.showAlert('Error', 'PIN must be 4 digits', 'error');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    account_number: accountNumber,
                    pin: pin
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = data.user;
                this.updateUserInfo();
                this.showScreen('main-menu-screen');
                this.showAlert('Success', `Welcome, ${data.user.full_name}!`, 'success');
                
                // Clear login form
                document.getElementById('account-number').value = '';
                document.getElementById('pin').value = '';
            } else {
                this.showScreen('login-screen');
                this.showAlert('Error', data.message, 'error');
            }
        } catch (error) {
            this.showScreen('login-screen');
            this.showAlert('Error', 'Connection error. Please try again.', 'error');
        }
    }

    async handleLogout() {
        try {
            await fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
        } catch (error) {
            console.error('Logout error:', error);
        }

        this.currentUser = null;
        this.showScreen('login-screen');
        this.showAlert('Success', 'You have been logged out successfully', 'success');
    }

    handleMenuAction(action) {
        switch (action) {
            case 'balance':
                this.handleBalanceInquiry();
                break;
            case 'withdraw':
                this.showScreen('withdraw-screen');
                break;
            case 'deposit':
                this.showScreen('deposit-screen');
                break;
            case 'history':
                this.handleTransactionHistory();
                break;
        }
    }

    async handleBalanceInquiry() {
        this.showLoading();

        try {
            const response = await fetch('/api/balance');
            const data = await response.json();

            if (data.success) {
                document.getElementById('balance-amount').textContent = data.balance.toFixed(2);
                document.getElementById('balance-account').textContent = data.account_number;
                document.getElementById('balance-time').textContent = new Date().toLocaleString();
                this.showScreen('balance-screen');
            } else {
                this.showScreen('main-menu-screen');
                this.showAlert('Error', data.message, 'error');
            }
        } catch (error) {
            this.showScreen('main-menu-screen');
            this.showAlert('Error', 'Connection error. Please try again.', 'error');
        }
    }

    async handleWithdrawal(amount) {
        if (!amount || amount <= 0) {
            this.showAlert('Error', 'Please enter a valid amount', 'error');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/api/withdraw', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount: amount })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser.balance = data.new_balance;
                this.showScreen('main-menu-screen');
                this.showAlert('Success', `${data.message}\nNew Balance: $${data.new_balance.toFixed(2)}`, 'success');
                
                // Clear custom amount
                document.getElementById('custom-withdraw').value = '';
            } else {
                this.showScreen('withdraw-screen');
                this.showAlert('Error', data.message, 'error');
            }
        } catch (error) {
            this.showScreen('withdraw-screen');
            this.showAlert('Error', 'Connection error. Please try again.', 'error');
        }
    }

    async handleDeposit(amount) {
        if (!amount || amount <= 0) {
            this.showAlert('Error', 'Please enter a valid amount', 'error');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/api/deposit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount: amount })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser.balance = data.new_balance;
                this.showScreen('main-menu-screen');
                this.showAlert('Success', `${data.message}\nNew Balance: $${data.new_balance.toFixed(2)}`, 'success');
                
                // Clear custom amount
                document.getElementById('custom-deposit').value = '';
            } else {
                this.showScreen('deposit-screen');
                this.showAlert('Error', data.message, 'error');
            }
        } catch (error) {
            this.showScreen('deposit-screen');
            this.showAlert('Error', 'Connection error. Please try again.', 'error');
        }
    }

    async handleTransactionHistory() {
        this.showLoading();

        try {
            const response = await fetch('/api/transactions?limit=10');
            const data = await response.json();

            if (data.success) {
                this.displayTransactions(data.transactions);
                this.showScreen('history-screen');
            } else {
                this.showScreen('main-menu-screen');
                this.showAlert('Error', data.message, 'error');
            }
        } catch (error) {
            this.showScreen('main-menu-screen');
            this.showAlert('Error', 'Connection error. Please try again.', 'error');
        }
    }

    displayTransactions(transactions) {
        const transactionList = document.getElementById('transaction-list');
        transactionList.innerHTML = '';

        if (transactions.length === 0) {
            transactionList.innerHTML = '<div class="transaction-item"><p>No transactions found.</p></div>';
            return;
        }

        transactions.forEach(transaction => {
            const transactionItem = document.createElement('div');
            transactionItem.className = 'transaction-item';

            const typeClass = transaction.type;
            let amountDisplay = '';
            let amountClass = '';

            if (transaction.amount) {
                if (transaction.type === 'withdrawal') {
                    amountDisplay = `-$${transaction.amount.toFixed(2)}`;
                    amountClass = 'negative';
                } else if (transaction.type === 'deposit') {
                    amountDisplay = `+$${transaction.amount.toFixed(2)}`;
                    amountClass = 'positive';
                }
            }

            transactionItem.innerHTML = `
                <div class="transaction-header">
                    <span class="transaction-type ${typeClass}">${transaction.type.replace('_', ' ')}</span>
                    ${amountDisplay ? `<span class="transaction-amount ${amountClass}">${amountDisplay}</span>` : ''}
                </div>
                <div class="transaction-details">
                    <div>${transaction.description}</div>
                    <div>Balance: $${transaction.balance_after.toFixed(2)}</div>
                    <div>${transaction.timestamp}</div>
                </div>
            `;

            transactionList.appendChild(transactionItem);
        });
    }

    updateUserInfo() {
        if (this.currentUser) {
            document.getElementById('user-name').textContent = this.currentUser.full_name;
            document.getElementById('user-account').textContent = this.currentUser.account_number;
        }
    }

    updateBalanceDisplays() {
        if (this.currentUser) {
            document.getElementById('withdraw-balance').textContent = this.currentUser.balance.toFixed(2);
            document.getElementById('deposit-balance').textContent = this.currentUser.balance.toFixed(2);
        }
    }

    showAlert(title, message, type = 'info') {
        const modal = document.getElementById('alert-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalMessage = document.getElementById('modal-message');
        const modalIcon = document.querySelector('.modal-icon');

        modalTitle.textContent = title;
        modalMessage.textContent = message;

        // Set icon based on type
        let iconClass = 'fas fa-info-circle';
        if (type === 'success') {
            iconClass = 'fas fa-check-circle';
            modalIcon.style.color = '#27ae60';
        } else if (type === 'error') {
            iconClass = 'fas fa-exclamation-circle';
            modalIcon.style.color = '#e74c3c';
        } else if (type === 'warning') {
            iconClass = 'fas fa-exclamation-triangle';
            modalIcon.style.color = '#f39c12';
        } else {
            modalIcon.style.color = '#3498db';
        }

        modalIcon.className = `modal-icon ${iconClass}`;
        modal.classList.add('show');

        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => {
                this.hideAlert();
            }, 3000);
        }
    }

    hideAlert() {
        const modal = document.getElementById('alert-modal');
        modal.classList.remove('show');
    }

    // Utility function to format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    // Utility function to validate numeric input
    isValidAmount(amount) {
        return !isNaN(amount) && isFinite(amount) && amount > 0;
    }
}

// Initialize ATM when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.atm = new ATMSimulator();
});

// Add some keyboard shortcuts for better UX
document.addEventListener('keydown', (e) => {
    // ESC key to go back or logout
    if (e.key === 'Escape') {
        if (window.atm.currentScreen !== 'login-screen') {
            if (window.atm.currentScreen === 'main-menu-screen') {
                window.atm.handleLogout();
            } else {
                window.atm.showScreen('main-menu-screen');
            }
        }
    }
});

// Prevent right-click context menu for better ATM simulation
document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
});

// Add touch support for mobile devices
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}