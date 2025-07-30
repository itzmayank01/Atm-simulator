# Mock user database
users_db = [
    {
        'card_number': '1234567890123456',
        'pin': '1234',
        'name': 'Alice',
        'balance': 1000.0,
        'history': [],
        'token': None
    },
    {
        'card_number': '9876543210987654',
        'pin': '4321',
        'name': 'Bob',
        'balance': 500.0,
        'history': [],
        'token': None
    }
]

def authenticate_user(card_number, pin):
    for user in users_db:
        if user['card_number'] == card_number and user['pin'] == pin:
            return user
    return None

def get_user_by_token(token):
    for user in users_db:
        if user.get('token') == token:
            return user
    return None