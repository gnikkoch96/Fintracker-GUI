from datetime import date

# firebase
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

# ids======================================================================

# option window
OPTION_WINDOW_ID = "Options Window"
OPTION_WINDOW_TICKER_INPUT_ID = "Options Ticker Input"
OPTION_WINDOW_SEARCH_BTN_ID = "Options Search Button"
OPTION_WINDOW_OPTION_TYPE_COMBO_ID = "Options Type Combo"
OPTION_WINDOW_DATE_COMBO_ID = "Options Date Combo"
OPTION_WINDOW_SEARCH_CONTRACT_BTN_ID = "Options Contract Search Button"
OPTION_TABLE_ID = "Options Table"

# trade input window
TRADE_INPUT_WINDOW_ID = "Trade Input Window"
TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_ID = "Ticker Search Button"
TRADE_INPUT_INFO_WINDOW_ID = "Ticker Info"
TRADE_INPUT_ADD_BTN_ID = "Ticker Add"
TRADE_INPUT_RADIO_BTNS_ID = "Ticker Radio Buttons"
TRADE_INPUT_INFO_WINDOW_TICKER_ID = "Ticker Info Ticker"
TRADE_INPUT_INFO_WINDOW_COUNT_ID = "Ticker Info Count"
TRADE_INPUT_INFO_WINDOW_BOUGHT_PRICE_ID = "Ticker Info Bought Price"
TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID = "Ticker Search Crypto Stock"
TRADE_INPUT_INFO_WINDOW_REASON_ID = "Ticker Info Reason"
TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_ID = "Ticker Info Contract Button"
TRADE_INPUT_INFO_WINDOW_SHOW_CONTRACT_ID = "Ticker Info Show Contract"
TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_ID = "Ticker Info Current Price Button"

# fintracker window
FINTRACKER_WINDOW_ID = "Fintracker Window"
FINTRACKER_CLOSED_TRADES_ID = "Fintracker Closed Trades"
FINTRACKER_OPEN_TRADES_CONTAINER_ID = "Fintracker Open Trades Container"
FINTRACKER_OPEN_TRADES_ID = "Fintracker Open Trades"
FINTRACKER_OPEN_TRADES_BUTTONS_ID = "Fintracker Open Trades Buttons"
FINTRACKER_ADD_BTN_ID = "Fintracker Add Button"
FINTRACKER_NEWS_BTN_ID = "Fintracker News Button"
FINTRACKER_PROFIT_PERCENT_ID = "Fintracker Win_Rate"
FINTRACKER_PROFIT_ID = "Fintracker Profit"
FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_ID = "Fintracker Crypto Stock Open Trades Table"
FINTRACKER_OPEN_TRADES_OPTION_TABLE_ID = "Fintracker Options Open Trades Table"
FINTRACKER_OPEN_TRADES_CRYPTO_STOCK_TABLE_TEXT_ID = "Fintracker Stock Crypto Table Label"
FINTRACKER_OPEN_TRADES_OPTIONS_TABLE_TEXT_ID = "Fintracker Options Table Label"
FINTRACKER_CLOSED_TRADES_OPTION_TABLE_ID = "Fintracker Closed Trade Option Table"
FINTRACKER_CLOSED_TRADES_CRYPTO_STOCK_TABLE_ID = "Fintracker Closed Trade Stock Crypto Table"
FINTRACKER_CLOSED_OPEN_TRADES_GROUP_ID = "Fintracker Closed Open Trades Group"

# sell trade window
SELL_TRADE_WINDOW_ID = "Sell Trade Window"
SELL_TRADE_COUNT_ID = "Sell Trade Count"
SELL_TRADE_SOLD_PRICE_ID = "Sell Trade Sold Price"
SELL_TRADE_SELL_BTN_ID = "Sell Trade Sell Button"
SELL_TRADE_REASON_ID = "Sell Trade Reason"

# view trade window
VIEW_TRADE_WINDOW_ID = "View Trade ID"
VIEW_TRADE_INPUT_ID = "View Trade Trade Input"
VIEW_TRADE_DATE_ID = "View Trade Date Input"
VIEW_TRADE_TYPE_ID = "View Trade Type Input"
VIEW_TRADE_COUNT_ID = "View Trade Count Input"
VIEW_TRADE_REASON_ID = "View Trade Reason Input"
VIEW_TRADE_BOUGHT_PRICE_ID = "View Trade Bought Price Input"
VIEW_TRADE_EDIT_BTN_ID = "View Trade Edit Button"
VIEW_TRADE_SAVE_BTN_ID = "View Trade Save Button"
VIEW_TRADE_CHANGE_CONTRACT_BTN_ID = "View Trade Choose Contract Button"
VIEW_TRADE_CANCEL_BTN_ID = "View Trade Cancel Button"
VIEW_TRADE_CHANGE_DATE_BTN_ID = "View Trade Change Date Button"
VIEW_TRADE_DATE_PICKER_ID = "View Trade Date Picker"
VIEW_TRADE_DATE_PICKER_WINDOW_ID = "View Trade Date Picker Window"
VIEW_TRADE_SOLD_PRICE_ID = "View Trade Sold Price"
VIEW_TRADE_NET_PROFIT_ID = "View Trade Net Profit"
VIEW_TRADE_PROFIT_PERCENTAGE_ID = "View Trade Profit Percentage"

# login window
LOGIN_WINDOW_ID = "Login Window"
LOGIN_INPUT_EMAIL_ID = "Login E-Mail"
LOGIN_INPUT_PASS_ID = "Login Password"
LOGIN_INPUT_BTN_ID = "Login Button"
LOGIN_INPUT_ERROR_ID = "Login Error"
LOGIN_REGISTER_BTN_ID = "Login_Register"
LOGIN_OFFLINE_BTN_ID = "Offline Mode"

# register window
REGISTER_WINDOW_ID = "Register Window"
REGISTER_INPUT_EMAIL_ID = "Register Email"
REGISTER_INPUT_PASS_ID = "Register Pass"
REGISTER_INPUT_ERROR_ID = "Register Error"
REGISTER_BTN_ID = "Register Button"
REGISTER_LOGIN_BTN_ID = "Register_Login"
REGISTER_INPUT_CONFIRM_PASS_ID = "Password Confirmation"

# value=======================================================================
NOT_APPLICABLE_TEXT = "N/A"
FONT_SCALE = 1.25
DEFAULT_DATE = {'month': date.today().month - 1,
                'year': date.today().year - 1900,
                'month_day': date.today().day}

# height and width values
FINTRACKER_WINDOW_VIEWPORT_SIZE = (1700, 800)  # width x height
FINTRACKER_CLOSED_TRADES_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.48,
                                          FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65)
FINTRACKER_OPEN_TRADES_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.48,
                                        FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.65)
FINTRACKER_OPEN_TRADES_BUTTONS_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] * 0.45,
                                                FINTRACKER_WINDOW_VIEWPORT_SIZE[1] * 0.20)

TRADE_INPUT_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2,
                                    FINTRACKER_WINDOW_VIEWPORT_SIZE[1])
TRADE_INPUT_INFO_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2.5,
                                         FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5)
TRADE_INPUT_INFO_WINDOW_TICKER_WIDTH = FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 4

TICKER_SEARCH_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 3,
                                      FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5)

OPTIONS_WINDOW_VIEWPORT_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2,
                                FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5)
OPTIONS_WINDOW_COMBO_WIDTH = FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 10

VIEW_TRADE_WINDOW_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 2,
                          FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 1.5)

SELL_TRADE_WINDOW_SIZE = (FINTRACKER_WINDOW_VIEWPORT_SIZE[0] / 5,
                          FINTRACKER_WINDOW_VIEWPORT_SIZE[1] / 3)
# dearpygui keywords
DPG_DATE_PICKER_YEAR = "year"
DPG_DATE_PICKER_MONTH = "month"
DPG_DATE_PICKER_DAY = "month_day"

# firebase keywords
FIREBASE_DATE = "date"
FIREBASE_TICKER = "ticker"
FIREBASE_TYPE = "stock_type"
FIREBASE_COUNT = "count"
FIREBASE_BOUGHT_PRICE = "bought_price"
FIREBASE_REASON = "reason"
FIREBASE_CONTRACT = "contract"
FIREBASE_OPEN_TRADES = "Open Trades"
FIREBASE_CLOSE_TRADES = "Closed Trades"
FIREBASE_OPTION_TEXT = "Options"
FIREBASE_STOCK_CRYPTO = "Stock_Crypto"
FIREBASE_LOCAL_ID = "localId"
FIREBASE_SOLD_PRICE = "sold_price"
FIREBASE_NET_PROFIT = "net_profit"
FIREBASE_PROFIT_PERCENTAGE = "profit_per"

# coingecko keywords
COINGECKO_SYMBOL = "symbol"
COINGECKO_NAME = "name"
COINGECKO_HASHINGALGO = "hashing_algorithm"
COINGECKO_CATEGORIES = "categories"
COINGECKO_DESC = "description"
COINGECKO_CURRENTPRICE = "current_price"
COINGECKO_CIRCULATINGSUPPLY = "circulating_supply"
COINGECKO_TOTALSUPPLY = "total_supply"
COINGECKO_MARKETCAP = "market_cap"
COINGECKO_MARKETDATA = "market_data"
COINGECKO_USD = "usd"
COINGECKO_ENGLISH = "en"
COINGECKO_PRICECHANGEPERCENT24H = "price_change_percentage_24h"

# yfinance keywords
YFINANCE_REGULARMARKETPRICE = "regularMarketPrice"
YFINANCE_STRIKE_PRICE = "strike"
YFINANCE_VOLUME = "volume"
YFINANCE_OPEN_INTEREST = "openInterest"
YFINANCE_IV_TEXT = "impliedVolatility"
YFINANCE_LONGBUSINESSSUMMARY = "longBusinessSummary"
YFINANCE_SHARESHORT = "sharesShort"
YFINANCE_SHARESHORTPRIORMONTH = "sharesShortPriorMonth"
YFINANCE_SHORTPERCENTFLOAT = "shortPercentOfFloat"
YFINANCE_MARKETCAP = "marketCap"

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
OPTION_SEARCH_BTN_TEXT = "Enter Ticker"

# trade input
TRADE_INPUT_WINDOW_TEXT = "(Fintracker) Add Trade"
TRADE_INPUT_ADD_BTN_TEXT = "Add Trade"
TRADE_INPUT_INFO_WINDOW_SEARCH_BTN_TEXT = "Search Ticker"
TRADE_INPUT_INFO_WINDOW_TICKER_TEXT = "Enter Ticker"
TRADE_INPUT_INFO_WINDOW_REASON_TEXT = "(Optional) Enter your reason"
TRADE_INPUT_INFO_WINDOW_CONTRACT_BTN_TEXT = "Choose Contract"
TRADE_INPUT_INFO_WINDOW_CURRENT_PRICE_BTN_TEXT = "Current Price"
TRADE_INPUT_RADIO_BTN_CRYPTO_TEXT = "Crypto"
TRADE_INPUT_RADIO_BTN_STOCK_TEXT = "Stock"
TRADE_INPUT_RADIO_BTN_OPTION_TEXT = "Option"

# ticker search
TICKER_SEARCH_CRYPTO_STOCK_WINDOW_TEXT = "Search Crypto/Stock Info"
TICKER_SEARCH_TICKER_TEXT = "Ticker: "
TICKER_SEARCH_MARKET_CAP_STOCK_TEXT = "Market Cap: "
TICKER_SEARCH_SUMMARY_OF_BUSINESS_STOCK_TEXT = "Business Summary: "
TICKER_SEARCH_SHARES_SHORTED_STOCK_TEXT = "Shares Shorted: "
TICKER_SEARCH_SHARES_SHORTED_PRIOR_MONTH_TEXT = "Shares Shorted Prior Month: "
TICKER_SEARCH_SHORT_PERCENT_TEXT = "Short %: "
TICKER_SEARCH_CRYPTO_NAME_TEXT = "Name: "
TICKER_SEARCH_CRYPTO_HASHALGO_TEXT = "Hashing Algorithm: "
TICKER_SEARCH_CRYPTO_CATEGORIES_TEXT = "Category: "
TICKER_SEARCH_CRYPTO_DESCRIPTION_TEXT = "Description: "
TICKER_SEARCH_CRYPTO_CURPRICE_TEXT = "Current Price: "
TICKER_SEARCH_CRYPTO_CIRCSUPPLY_TEXT = "Circulating Supply: "
TICKER_SEARCH_CRYPTO_TOTSUPPLY_TEXT = "Total Supply: "
TICKER_SEARCH_CRYPTO_MRKTCAPTEXT = "Market Cap: "
TICKER_SEARCH_CHANGE_PERCENT_24H_TEXT = "24H Change %: "
TICKERS_SEARCH_WRAP_COUNT = 500


# fintracker
FINTRACKER_VIEWPORT_TITLE = "Fintracker - Record Your Trades!"
FINTRACKER_VIEWPORT_ICON_PATH = "resources/images/fintrack-logo.ico"
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
FINTRACKER_VIEW_TRADE_BTN_TEXT = "View Trade"
FINTRACKER_OPEN_TRADES_ROW_TEXT = "open_trade row "
FINTRACKER_CLOSED_TRADES_ROW_TEXT = "closed_trade row "
FINTRACKER_SELL_TEXT = "sell"
FINTRACKER_REMOVE_TEXT = "X"
FINTRACKER_ADD_BTN_TEXT = "Add"

# sell trade
SELL_TRADE_WINDOW_TEXT = "Selling Trade"
SELL_TRADE_COUNT_TEXT = "Number Sold: "
SELL_TRADE_SOLD_PRICE_TEXT = "Sold Price"
SELL_TRADE_SELL_BTN_TEXT = "Sell Trade"
SELL_TRADE_REASON_TEXT = "Reason"

# view trade
VIEW_TRADE_WINDOW_TEXT = "View Trade"
VIEW_TRADE_EDIT_BTN_TEXT = "Edit Trade"
VIEW_TRADE_SAVE_BTN_TEXT = "Apply Changes"
VIEW_TRADE_CHANGE_CONTRACT_BTN_TEXT = "Change Contract"
VIEW_TRADE_INPUT_TEXT = "Trade: "
VIEW_TRADE_DATE_TEXT = "Date Of Purhcase: "
VIEW_TRADE_TYPE_TEXT = "Type: "
VIEW_TRADE_COUNT_TEXT = "Count: "
VIEW_TRADE_BOUGHT_PRICE_TEXT = "Bought Price: "
VIEW_TRADE_REASON_TEXT = "Reason: "
VIEW_TRADE_CANCEL_BTN_TEXT = "Cancel"
VIEW_TRADE_CHANGE_DATE_BTN_TEXT = "Change Date"
VIEW_TRADE_DATE_PICKER_WINDOW_TEXT = "Choose Date"
VIEW_TRADE_SOLD_PRICE_TEXT = "Sold Price: "
VIEW_TRADE_NET_PROFIT_TEXT = "Net Profit: "
VIEW_TRADE_PROFIT_PERCENTAGE_TEXT = "Profit %: "

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
