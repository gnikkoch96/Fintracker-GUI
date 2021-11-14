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


def authenticate_user_login(email, password):
    try:
        firebase_auth.sign_in_with_email_and_password(email, password)
        return True
    except:
        print("[ERROR] Login Failed")
        return False


def create_user_account(email, password):
    try:
        firebase_auth.create_user_with_email_and_password(email, password)
        return True
    except:
        return False
