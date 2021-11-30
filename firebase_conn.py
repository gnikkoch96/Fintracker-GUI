import pyrebase
import configs

# firebase init
firebase = pyrebase.initialize_app(configs.FIREBASE_CONFIG)

# authentication
firebase_auth = firebase.auth()

# realtime database
firebase_db = firebase.database()


def authenticate_user_login(email, password):
    try:
        auth = firebase_auth.sign_in_with_email_and_password(email, password)

        # todo remove this
        print("Logged in successfully!")
        return auth[configs.FIREBASE_LOCAL_ID]
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


def add_open_trade_db(user_id, data, is_option=False):
    if user_id is not None:
        if is_option:
            firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
                configs.FIREBASE_OPTION_TEXT).push(data)
        else:
            firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
                configs.FIREBASE_STOCK_CRYPTO_TEXT).push(data)


def add_closed_trade_db(user_id, data):
    if user_id is not None:
        firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES_TEXT).push(data)


def remove_open_trade_by_id(user_id, is_option, trade_id):
    if is_option:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_OPTION_TEXT).child(trade_id).remove()
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_STOCK_CRYPTO_TEXT).child(trade_id).remove()


def get_closed_trades_db(user_id):
    if user_id is not None:
        return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES_TEXT).get().val()


def get_closed_trade_by_id_db(user_id, trade_id):
    return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES_TEXT).child(trade_id).get().val()


# todo combine with options method
def get_open_trades_stock_crypto_db(user_id):
    if user_id is not None:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_STOCK_CRYPTO_TEXT).get().val()


def get_open_trades_options_db(user_id):
    if user_id is not None:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_OPTION_TEXT).get().val()


def get_open_trade_by_id_db(user_id, trade_id, is_option=False):
    if is_option:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_OPTION_TEXT).child(trade_id).get().val()
    else:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_STOCK_CRYPTO_TEXT).child(trade_id).get().val()


def get_open_trades_keys(user_id, is_option):
    if is_option:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_OPTION_TEXT).get().val().keys()
    else:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_STOCK_CRYPTO_TEXT).get().val().keys()


def update_open_trade_by_id(user_id, trade_id, new_data, is_options=False):
    if is_options:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_OPTION_TEXT).child(trade_id).update(new_data)
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES_TEXT).child(
            configs.FIREBASE_STOCK_CRYPTO_TEXT).child(trade_id).update(new_data)
