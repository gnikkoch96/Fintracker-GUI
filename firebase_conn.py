import pyrebase
import configs

# firebase init (connects to our firebase server)
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
        return auth[configs.FIREBASE_LOCAL_ID]  # returns the user's id
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


# adds a new trade to the db
def add_open_trade_db(user_id, data, is_option):
    if user_id is not None:
        if is_option:
            firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).push(data)
        else:
            firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).push(data)


# removes a trade from the db with the corresponding trade_id
def remove_open_trade_by_id(user_id, is_option, trade_id):
    if is_option:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).remove()
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).remove()


# gets the open trades corresponding to the stock/crypto or option table
def get_open_trades_db(user_id, is_option):
    if user_id is not None:
        if is_option:
            return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).get().val()
        else:
            return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).get().val()


# retrieves open trade information corresponding to trade id
def get_open_trade_by_id(user_id, trade_id, is_option):
    if is_option:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).get().val()
    else:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).get().val()


# retrieves the ids for all open trades (used to retrieve recent trade)
def get_open_trades_keys(user_id, is_option):
    if is_option:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_OPTION).get().val().keys()
    else:
        return firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).get().val().keys()


# updates an open trade by trade_id
def update_open_trade_by_id(user_id, trade_id, new_data, is_options):
    if is_options:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).update(new_data)
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).update(new_data)


# used when updating specific properties of a trade (i.e. count, ticker, etc...)
def update_open_trade_by_id_key(user_id, trade_id, keyword, new_data, is_options):
    if is_options:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).update({keyword: new_data})
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_OPEN_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).update({keyword: new_data})


# add a trade to the closed trade category
def add_closed_trade_db(user_id, data, is_option):
    if user_id is not None:
        if is_option:
            firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_OPTION).push(data)
        else:
            firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).push(data)


# removes a trade from the db with the corresponding trade_id
def remove_closed_trade_by_id(user_id, is_option, trade_id):
    if is_option:
        firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).remove()
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).remove()

# retrieves all closed trades corresponding to user id
def get_closed_trades_db(user_id, is_option):
    if user_id is not None:
        if is_option:
            return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_OPTION).get().val()
        else:
            return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).get().val()


# retrieves a closed trade corresponding to trade id
def get_closed_trade_by_id(user_id, trade_id, is_option):
    if is_option:
        return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).get().val()
    else:
        return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).get().val()


# retrieve closed trade ids (used to get the recent closed trade)
def get_closed_trades_keys(user_id, is_option):
    if is_option:
        return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_OPTION).get().val().keys()
    else:
        return firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).get().val().keys()


# updates closed trade corresponding to trade id
def update_closed_trade_by_id(user_id, trade_id, new_data, is_options=False):
    if is_options:
        firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_OPTION).child(trade_id).update(new_data)
    else:
        firebase_db.child(user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
            configs.FIREBASE_STOCK_CRYPTO).child(trade_id).update(new_data)
