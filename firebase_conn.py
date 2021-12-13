import threading

import pyrebase
import configs
import time

# firebase init (connects to our firebase server)
firebase = pyrebase.initialize_app(configs.FIREBASE_CONFIG)

# authentication
firebase_auth = firebase.auth()

# realtime database
firebase_db = firebase.database()


# returns the user's id once authenticated
def authenticate_user_login(email, password):
    try:
        return firebase_auth.sign_in_with_email_and_password(email, password)
    except:
        return None


# attempts to create an account using passed email and password
def create_user_account(email, password):
    try:
        firebase_auth.create_user_with_email_and_password(email, password)
        return True
    except:
        return False


# desc used to connect client to firebase
class FirebaseConn:
    def __init__(self, user_info):
        # user
        self._user = user_info
        self._user_id = user_info[configs.FIREBASE_LOCAL_ID]
        self._token_id = user_info[configs.FIREBASE_TOKENID]

        # thread that will refresh token (so that they are allowed to continue using our service)
        threading.Thread(target=self.refresh_token, daemon=True).start()

    def refresh_token(self):
        while True:
            # wait about an hour before refreshing the service token
            time.sleep(configs.HOUR_IN_SECONDS)
            firebase.auth().refresh(self._user[configs.FIREBASE_REFRESHTOKEN])

    # adds a new trade to the db
    def add_open_trade_db(self, data, is_option):
        if self._user_id is not None:
            if is_option:
                firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                    configs.FIREBASE_OPTION).push(data, self._token_id)
            else:
                firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                    configs.FIREBASE_STOCK_CRYPTO).push(data, self._token_id)

    # removes a trade from the db with the corresponding trade_id
    def remove_open_trade_by_id(self, is_option, trade_id):
        if is_option:
            firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).remove(self._token_id)
        else:
            firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).remove(self._token_id)

    # gets the open trades corresponding to the stock/crypto or option table
    def get_open_trades_db(self, is_option):
        if self._user_id is not None:
            if is_option:
                return firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                    configs.FIREBASE_OPTION).get(self._token_id).val()
            else:
                return firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                    configs.FIREBASE_STOCK_CRYPTO).get(self._token_id).val()

    # retrieves open trade information corresponding to trade id
    def get_open_trade_by_id(self, trade_id, is_option):
        if is_option:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).get(self._token_id).val()
        else:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).get(self._token_id).val()

    # retrieves the ids for all open trades (used to retrieve recent trade)
    def get_open_trades_keys(self, is_option):
        if is_option:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).get(self._token_id).val().keys()
        else:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).get(self._token_id).val().keys()

    # updates an open trade by trade_id
    def update_open_trade_by_id(self, trade_id, new_data, is_options):
        if is_options:
            firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).update(new_data, self._token_id)
        else:
            firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).update(new_data, self._token_id)

    # used when updating specific properties of a trade by keyword (i.e. count, ticker, etc...)
    def update_open_trade_by_id_key(self, trade_id, keyword, new_data, is_options):
        if is_options:
            firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).update({keyword: new_data}, self._token_id)
        else:
            firebase_db.child(self._user_id).child(configs.FIREBASE_OPEN_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).update({keyword: new_data}, self._token_id)

    # add a trade to the closed trade category
    def add_closed_trade_db(self, data, is_option):
        if self._user_id is not None:
            if is_option:
                firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                    configs.FIREBASE_OPTION).push(data, self._token_id)
            else:
                firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                    configs.FIREBASE_STOCK_CRYPTO).push(data, self._token_id)

    # removes a trade from the db with the corresponding trade_id
    def remove_closed_trade_by_id(self, is_option, trade_id):
        if is_option:
            firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).remove(self._token_id)
        else:
            firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).remove(self._token_id)

    # retrieves all closed trades corresponding to user id
    def get_closed_trades_db(self, is_option):
        if self._user_id is not None:
            if is_option:
                return firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                    configs.FIREBASE_OPTION).get(self._token_id).val()
            else:
                return firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                    configs.FIREBASE_STOCK_CRYPTO).get(self._token_id).val()

    # retrieves a closed trade corresponding to trade id
    def get_closed_trade_by_id(self, trade_id, is_option):
        if is_option:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).get(self._token_id).val()
        else:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).get(self._token_id).val()

    # retrieve closed trade ids (used to get the recent closed trade)
    def get_closed_trades_keys(self, is_option):
        if is_option:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_OPTION).get(self._token_id).val().keys()
        else:
            return firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).get(self._token_id).val().keys()

    # updates closed trade corresponding to trade id
    def update_closed_trade_by_id(self, trade_id, new_data, is_options=False):
        if is_options:
            firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_OPTION).child(trade_id).update(new_data, self._token_id)
        else:
            firebase_db.child(self._user_id).child(configs.FIREBASE_CLOSE_TRADES).child(
                configs.FIREBASE_STOCK_CRYPTO).child(trade_id).update(new_data, self._token_id)
