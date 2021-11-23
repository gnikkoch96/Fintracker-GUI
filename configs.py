# firebase config
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

# ids
OPTIONS_WINDOW_ID = "Options Window"
OPTION_WINDOW_TICKER_INPUT_ID = "Options Ticker Input"
OPTION_WINDOW_SEARCH_BTN_ID = "Options Search Button"
OPTION_WINDOW_OPTION_TYPE_COMBO_ID = "Options Type Combo"
OPTION_WINDOW_DATE_COMBO_ID = "Options Date Combo"
OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID ="Options Contract Search Button"
OPTION_TABLE_ID = "Options Table"

TICKER_WINDOW_ID = "Ticker Window"
TICKER_INFO_WINDOW_SEARCH_BTN_ID = "Ticker Search Button"
TICKER_INFO_WINDOW_ID = "Ticker Info"
TICKER_ADD_BTN_ID = "Ticker Add"
TICKER_RADIO_BTNS_ID = "Ticker Radio Buttons"
TICKER_INFO_WINDOW_TICKER_ID = "Ticker Info Ticker"
TICKER_INFO_WINDOW_COUNT_ID = "Ticker Info Count"
TICKER_INFO_WINDOW_BOUGHT_PRICE_ID = "Ticker Info Bought Price"
TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID = "Ticker Add Crypto Stock"
TICKER_INFO_WINDOW_REASON_ID = "Ticker Info Reason"
TICKER_INFO_WINDOW_CONTRACT_BTN_ID = "Ticker Info Contract Button"
TICKER_INFO_WINDOW_SHOW_CONTRACT_ID = "Ticker Info Show Contract"
TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_ID = "Ticker Info Current Price Button"

FINTRACKER_WINDOW_ID = "Fintracker Window"
FINTRACKER_CLOSED_TRADES_ID = "Fintracker Closed Trades"
FINTRACKER_OPEN_TRADES_CONTAINER_ID = "Fintracker Open Trades Container"
FINTRACKER_OPEN_TRADES_ID = "Fintracker Open Trades"
FINTRACKER_OPEN_TRADES_BUTTONS_ID = "Fintracker Open Trades Buttons"
FINTRACKER_ADD_BTN_ID = "Fintracker Add Button"
FINTRACKER_NEWS_BTN_ID = "Fintracker News Button"
FINTRACKER_PROFIT_PERCENT_ID = "Fintracker Win_Rate"
FINTRACKER_PROFIT_ID = "Fintracker Profit"
FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID = "Crypto Stock Open Trades Table"
FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID = "Options Open Trades Table"

LOGIN_WINDOW_ID = "Login Window"
LOGIN_INPUT_EMAIL_ID = "Login E-Mail"
LOGIN_INPUT_PASS_ID = "Login Password"
LOGIN_INPUT_BTN_ID = "Login Button"
LOGIN_INPUT_ERROR_ID = "Login Error"
LOGIN_REGISTER_BTN_ID = "Login->Register"
LOGIN_OFFLINE_BTN_ID = "Offline Mode"

REGISTER_WINDOW_ID = "Register Window"
REGISTER_INPUT_EMAIL_ID = "Register Email"
REGISTER_INPUT_PASS_ID = "Register Pass"
REGISTER_INPUT_ERROR_ID = "Register Error"
REGISTER_BTN_ID = "Register Button"
REGISTER_LOGIN_BTN_ID = "Register to Login"
REGISTER_INPUT_CONFIRM_PASS_ID = "Password Confirmation"


# values
ADD_BTN_TEXT = "Add"
SEARCH_BTN_TEXT = "Search"
VIEWPORT_TITLE = "Fintracker - Record Your Trades!"
VIEWPORT_ICON_PATH = "resources/images/fintrack-logo.ico"

# height and width values
FINTRACKER_WINDOW_VIEWPORT_SIZE = (1700, 800) # width x height
FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.40,
                                          FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65)
FINTRACKER_OPEN_TRADES_CONTAINER_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.45,
                                          FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65)
FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.45,
                                          FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.45)
FINTRACKER_OPEN_TRADES_BUTTONS_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.45,
                                                FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.20)

TICKER_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2,
                               FINTRACKER_WINDOW_VIEWPORT_SIZE[1])
TICKER_INFO_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2.5,
                                    FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5)

OPTIONS_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2,
                               FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5)
OPTIONS_WINDOW_COMBO_WIDTH = FINTRACKER_WINDOW_VIEWPORT_SIZE[0]/10

# firebase keywords
FIREBASE_DATE = "date"
FIREBASE_TICKER = "ticker"
FIREBASE_TYPE = "stock_type"
FIREBASE_COUNT = "count"
FIREBASE_BOUGHT_PRICE = "bought_price"
FIREBASE_REASON = "reason"
FIREBASE_CONTRACT = "contract"
FIREBASE_OPEN_TRADES_TEXT = "Open Trades"
FIREBASE_CLOSE_TRADES_TEXT = "Closed Trades"
FIREBASE_OPTION_TEXT = "Options"
FIREBASE_STOCK_CRYPTO_TEXT = "Stock_Crypto"
FIREBASE_LOCAL_ID = "localId"

# yfinance keywords
YFINANCE_REGULARMARKETPRICE = "regularMarketPrice"
YFINANCE_STRIKE_PRICE_TEXT = "strike"
YFINANCE_VOLUME_TEXT = "volume"
YFINANCE_OPEN_INTEREST_TEXT = "openInterest"
YFINANCE_IV_TEXT = "impliedVolatility"

# options
OPTIONS_WINDOW_TEXT = "Choose Option Contract"
OPTIONS_CALL_TEXT = "Call"
OPTIONS_PUT_TEXT = "Put"
OPTION_WINDOW_TICKER_INPUT_TEXT = "Enter Ticker"
OPTION_WINDOW_SEARCH_CONTRACT_BTN_TEXT = "Search Contracts"
OPTION_STRIKE_LABEL_TEXT = "Strike Price"
OPTION_VOLUME_LABEL_TEXT = "Volume"
OPTION_OPEN_INTEREST_LABEL_TEXT = "Open Interest"
OPTION_IV_LABEL_TEXT = "Implied Volatility"

# ticker search
TICKER_WINDOW_TEXT = "(Fintracker) Search Ticker"
TICKER_RADIO_BTN_CRYPTO_TEXT = "Crypto"
TICKER_RADIO_BTN_STOCK_TEXT = "Stock"
TICKER_RADIO_BTN_OPTION_TEXT = "Option"
TICKER_INFO_WINDOW_TEXT = "Ticker Information"
TICKER_INFO_WINDOW_TICKER_TEXT = "Enter Ticker"
TICKER_INFO_WINDOW_COUNT_TEXT = "Enter Count"
TICKER_INFO_WINDOW_BOUGHT_PRICE_TEXT = "Enter Bought Price"
TICKER_INFO_WINDOW_REASON_TEXT = "(Optional) Enter your reason"
TICKER_SEARCH_CRYPTO_STOCK_WINDOW_TEXT = "Search Crypto/Stock Info"
TICKER_INFO_WINDOW_CONTRACT_BTN_TEXT = "Choose Contract"
TICKER_INFO_WINDOW_CURRENT_PRICE_BTN_TEXT = "Current Price"

# fintracker
FINTRACKER_WINDOW_TEXT = "(Fintracker) Investment Tracker"
FINTRACKER_NEWS_BTN_TEXT = "News"
FINTRACKER_PROFIT_LABEL_TEXT = "Net Profit: "
FINTRACKER_PROFIT_TEXT = "0"
FINTRACKER_PROFIT_PERCENT_LABEL_TEXT = "Win-Rate: "
FINTRACKER_PROFIT_PERCENT_TEXT = "0.0%"
FINTRACKER_CLOSED_TRADES_TEXT = "Closed Trades"
FINTRACKER_OPEN_TRADES_TEXT = "Open Trades"
FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_TEXT = "Stock/Crypto"
FINTRACKER_OPEN_TRADES_OPTION_TABLE_TEXT = "Option"
FINTRACKER_OPEN_TRADES_VIEW_TRADE_TEXT = "View Trade"

# login
LOGIN_WINDOW_TEXT = "(FinTracker) Login"
LOGIN_INPUT_EMAIL_TEXT = "Enter E-Mail"
LOGIN_INPUT_PASS_TEXT = "Enter Password"
LOGIN_INPUT_ERROR_TEXT = "[ERROR] Invalid Login Credentials"
LOGIN_INPUT_BTN_TEXT = "Login"
LOGIN_REGISTER_BTN_TEXT = "Not a user? Sign up now!"
LOGIN_OFFLINE_BTN_TEXT = "Go Offline"

# register
REGISTER_WINDOW_TEXT = "(FinTracker) Register"
REGISTER_INPUT_EMAIL_TEXT = "Enter E-Mail"
REGISTER_INPUT_PASS_TEXT = "Enter Password"
REGISTER_INPUT_ERROR_TEXT = "[ERROR] E-Mail is currently being used and/or Confirm Password and Password are not the same."
REGISTER_BTN_TEXT = "Register"
REGISTER_LOGIN_BTN_TEXT = "Already have an account? Click Here"
REGISTER_INPUT_CONFIRM_PASS_TEXT = "Confirm Password"