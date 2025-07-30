# ATM Simulator Website

A polished yet simple web application that simulates an Automated Teller Machine (ATM) experience. Built with Flask, HTML, CSS (Bootstrap 5), and JavaScript.

## Features

- Secure login using account number + hashed PIN
- View current balance
- Cash withdrawal & deposit with validation
- Transaction history (JSON endpoint + dynamic table)
- Modular, easily-extensible architecture

## Project Structure

```text
.
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── data/
│   └── users.json      # Sample data store (JSON)
├── templates/
│   ├── base.html       # Base template with Bootstrap
│   ├── login.html      # Login page
│   └── dashboard.html  # Main dashboard
└── static/
    ├── css/
    │   └── styles.css  # Custom styles
    └── js/
        └── app.js      # Front-end JS logic
```

## Setup & Run

1. Install Python 3.10+
2. Create virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Launch the server:

```bash
python app.py
```

5. Open http://localhost:5000 in your browser.

> Default sample account: **1001**, PIN **1234**

## Next Steps / Ideas

- Persist data in SQLite or PostgreSQL
- Implement multiple user accounts & registration
- Add transfer between accounts
- Integrate RESTful API and SPA front-end framework (React/Vue)
- Add unit tests & CI pipeline