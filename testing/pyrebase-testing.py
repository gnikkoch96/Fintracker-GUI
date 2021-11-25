import pyrebase


firebase_config = {
    'apiKey': "AIzaSyBR0l5iXd7MwfLG5ltKhvMGKUsE7DpsGHQ",
    'authDomain': "python-testing-ef238.firebaseapp.com",
    'databaseURL': "https://python-testing-ef238-default-rtdb.firebaseio.com/",
    'projectId': "python-testing-ef238",
    'storageBucket': "python-testing-ef238.appspot.com",
    'messagingSenderId': "1063640306776",
    'appId': "1:1063640306776:web:b92a28f2ad29f10a67e62d",
    'measurementId': "G-8PCYDLQTW3"
}

firebase = pyrebase.initialize_app(firebase_config)  # connects to the firebase with the corresponding credentials

# firebase authentication (sign-in)
firebase_auth = firebase.auth()

# login credentials
# email = input("Enter Email: ")
# password = input("Enter Password: ")
#
# try:
#     firebase_auth.sign_in_with_email_and_password(email, password)
#     print("[LOGIN] Logged In Successfully")
# except requests.exceptions.HTTPError as e:
#     error_json = e.args[1]
#     error = json.loads(error_json)['error']['message']
#     if error == "EMAIL_EXISTS":
#         print("Email already exists")


# sign up
email = input("Enter Email: ")
password = input("Enter Password: ")
password_confirm = input("Confirm Password: ")
if password == password_confirm:
    try:
        firebase_auth.create_user_with_email_and_password(email, password)
        print("[CREATE] Account Created")
    except:
        print("[ERROR] Account could not be Created")
