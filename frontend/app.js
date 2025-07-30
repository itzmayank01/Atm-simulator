// ATM Frontend Logic
const loginScreen = document.getElementById('login-screen');
const dashboardScreen = document.getElementById('dashboard-screen');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const userNameSpan = document.getElementById('user-name');
const atmOperation = document.getElementById('atm-operation');

let authToken = null;

function showScreen(screen) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    screen.classList.add('active');
    atmOperation.innerHTML = '';
}

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const cardNumber = document.getElementById('card-number').value;
    const pin = document.getElementById('pin').value;
    loginError.textContent = '';
    try {
        const res = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_number: cardNumber, pin })
        });
        const data = await res.json();
        if (res.ok) {
            authToken = data.token;
            userNameSpan.textContent = data.name;
            showScreen(dashboardScreen);
        } else {
            loginError.textContent = data.error || 'Login failed';
        }
    } catch (err) {
        loginError.textContent = 'Server error';
    }
});

document.getElementById('logout-btn').onclick = () => {
    authToken = null;
    loginForm.reset();
    showScreen(loginScreen);
};

document.getElementById('balance-btn').onclick = async () => {
    atmOperation.innerHTML = 'Loading...';
    const res = await fetch('http://localhost:5000/api/balance', {
        headers: { 'Authorization': `Bearer ${authToken}` }
    });
    const data = await res.json();
    atmOperation.innerHTML = res.ok ? `<h3>Balance: $${data.balance.toFixed(2)}</h3>` : `<div class="error">${data.error}</div>`;
};

document.getElementById('withdraw-btn').onclick = () => {
    atmOperation.innerHTML = `
        <form id="withdraw-form">
            <label>Amount to Withdraw</label>
            <input type="number" id="withdraw-amount" min="1" required>
            <button type="submit">Withdraw</button>
        </form>
        <div id="withdraw-error" class="error"></div>
    `;
    document.getElementById('withdraw-form').onsubmit = async (e) => {
        e.preventDefault();
        const amount = document.getElementById('withdraw-amount').value;
        const res = await fetch('http://localhost:5000/api/withdraw', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ amount })
        });
        const data = await res.json();
        if (res.ok) {
            atmOperation.innerHTML = `<h3>Withdrawal successful! New Balance: $${data.balance.toFixed(2)}</h3>`;
        } else {
            document.getElementById('withdraw-error').textContent = data.error;
        }
    };
};

document.getElementById('deposit-btn').onclick = () => {
    atmOperation.innerHTML = `
        <form id="deposit-form">
            <label>Amount to Deposit</label>
            <input type="number" id="deposit-amount" min="1" required>
            <button type="submit">Deposit</button>
        </form>
        <div id="deposit-error" class="error"></div>
    `;
    document.getElementById('deposit-form').onsubmit = async (e) => {
        e.preventDefault();
        const amount = document.getElementById('deposit-amount').value;
        const res = await fetch('http://localhost:5000/api/deposit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ amount })
        });
        const data = await res.json();
        if (res.ok) {
            atmOperation.innerHTML = `<h3>Deposit successful! New Balance: $${data.balance.toFixed(2)}</h3>`;
        } else {
            document.getElementById('deposit-error').textContent = data.error;
        }
    };
};

document.getElementById('history-btn').onclick = async () => {
    atmOperation.innerHTML = 'Loading...';
    const res = await fetch('http://localhost:5000/api/history', {
        headers: { 'Authorization': `Bearer ${authToken}` }
    });
    const data = await res.json();
    if (res.ok) {
        if (data.history.length === 0) {
            atmOperation.innerHTML = '<p>No transactions yet.</p>';
        } else {
            atmOperation.innerHTML = '<h3>Transaction History</h3><ul>' +
                data.history.map(t => `<li>${t.type} $${t.amount.toFixed(2)} on ${t.date}</li>`).join('') + '</ul>';
        }
    } else {
        atmOperation.innerHTML = `<div class="error">${data.error}</div>`;
    }
};

// On load, show login
showScreen(loginScreen);