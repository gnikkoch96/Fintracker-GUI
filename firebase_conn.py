import pyrebase

FIREBASE_CONFIG = {
    'apiKey': "AIzaSyBR0l5iXd7MwfLG5ltKhvMGKUsE7DpsGHQ",
    'authDomain': "python-testing-ef238.firebaseapp.com",
    'databaseURL': "https://python-testing-ef238-default-rtdb.firebaseio.com/",
    'projectId': "python-testing-ef238",
    'storageBucket': "python-testing-ef238.appspot.com",
    'messagingSenderId': "1063640306776",
    'appId': "1:1063640306776:web:b92a28f2ad29f10a67e62d",
    'measurementId': "G-8PCYDLQTW3"
}

# firebase init
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)

# authentication
firebase_auth = firebase.auth()

# realtime database
firebase_db = firebase.database()

USER_ID = ""


def authenticate_user_login(email, password):
    try:
        auth = firebase_auth.sign_in_with_email_and_password(email, password)

        # todo remove this
        print("Logged in successfully!")
        return auth['localId']
    except:
        print("[ERROR] Login Failed")
        return None


def create_user_account(email, password):
    try:
        firebase_auth.create_user_with_email_and_password(email, password)

        # todo remove this
        print("Successfully Created an Account")
        return True
    except:
        print("Password has to have a length of 6 or higher")
        return False


def add_to_db(user_id, data):
    if user_id is not None:
        firebase_db.child(user_id).child('Open Trades').push(data)
        firebase_db.child(user_id).child('Closed Trades').push(data)
    else:
        firebase_db.child().child('Open Trades').push(data)


def get_closed_trades_db(user_id):
    if user_id is not None:
        return firebase_db.child(user_id).child("Closed Trades").get().val()


def get_closed_trade_db(user_id, trade_id):
    return firebase_db.child(user_id).child("Closed Trades").child(trade_id).get().val()


def get_open_trades_db(user_id):
    if user_id is not None:
        return firebase_db.child(user_id).child("Open Trades").get().val()


def get_open_trade_db(user_id, trade_id):
    return firebase_db.child(user_id).child("Open Trades").child(trade_id).get().val()
