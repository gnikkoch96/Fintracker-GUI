import pyrebase

firebase_config = {
    'apiKey': "AIzaSyCtotU0H3hBXwq-Z3-29HSUHKin2M-JdDA",
    'authDomain': "fintracker-ec2ae.firebaseapp.com",
    'databaseURL': 'https://fintracker-ec2ae-default-rtdb.firebaseio.com/',
    'projectId': "fintracker-ec2ae",
    'storageBucket': "fintracker-ec2ae.appspot.com",
    'messagingSenderId': "281971152933",
    'appId': "1:281971152933:web:2fcd7568723b378846c7cc",
    'measurementId': "G-8Z1P4NZ1TJ"
}

firebase = pyrebase.initialize_app(firebase_config)  # connects to the firebase with the corresponding credentials

# firebase authentication (sign-in)
firebase_auth = firebase.auth()

# firebase database
firebase_db = firebase.database()

# login credentials
email = "nikko@email.com"
password = "123456"

user_info = firebase_auth.sign_in_with_email_and_password(email, password)

# data to save
data = {
    "name": "Mortimer 'Morty' Smith"
}

# Pass the user's idToken to the push method
user_id = user_info['localId']
token_id = user_info['idToken']

results = firebase_db.child(user_id).push(data, token_id)

# try:
#     firebase_auth.sign_in_with_email_and_password(email, password)
#     print("[LOGIN] Logged In Successfully")
# except requests.exceptions.HTTPError as e:
#     error_json = e.args[1]
#     error = json.loads(error_json)['error']['message']
#     if error == "EMAIL_EXISTS":
#         print("Email already exists")


