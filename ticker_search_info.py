import configs
import yfinance_tool as yft
import cngko_tool as cgt


# desc: creates the window that displays information about the stock or crypto
class CryptoStockInfo:
    def __init__(self, dpg, ticker, is_crypto=False):
        self.dpg = dpg
        self.ticker = ticker
        self.is_crypto = is_crypto
        self.create_search_win()

    def create_search_win(self):
        # stock crypto info window
        with self.dpg.window(tag=configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID,
                             label=configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_TEXT,
                             width=configs.TICKER_SEARCH_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.TICKER_SEARCH_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup_aliases,
                             modal=True):

            if self.is_crypto:  # loads crypto info
                self.create_search_win_crypto_items()
            else:  # loads stock info
                self.create_search_win_stock_items()

    def create_search_win_crypto_items(self):
        # needs to be lowercase (coingecko api)
        lower_ticker = self.ticker.lower()

        # display name + ticker
        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_NAME_TEXT + self.ticker.capitalize())
        self.dpg.add_text(configs.TICKER_SEARCH_TICKER_TEXT + cgt.get_symbol(lower_ticker))

        # current price
        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_CURPRICE_TEXT + str(cgt.get_current_price(lower_ticker)))

        # change % 24 hrs
        self.dpg.add_text(
            configs.TICKER_SEARCH_CHANGE_PERCENT_24H_TEXT + str(cgt.get_price_change_percentage_24h(lower_ticker)))

        # market cap
        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_MRKTCAPTEXT + str(cgt.get_market_cap(lower_ticker)))

        # circulating supply
        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_CIRCSUPPLY_TEXT + str(cgt.get_circulating_supply(lower_ticker)))

        # total supply
        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_TOTSUPPLY_TEXT + str(cgt.get_total_supply(lower_ticker)))

        # hashing algo
        if cgt.get_hashing_algorithm(lower_ticker) is not None:
            hashing_algo = cgt.get_hashing_algorithm(lower_ticker)
        else:
            hashing_algo = configs.NOT_APPLICABLE_TEXT

        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_HASHALGO_TEXT + hashing_algo)

        # description
        self.dpg.add_text(configs.TICKER_SEARCH_CRYPTO_DESCRIPTION_TEXT)
        self.dpg.add_text(default_value=cgt.get_description(lower_ticker),
                          wrap=configs.TICKERS_SEARCH_WRAP_COUNT)

    def create_search_win_stock_items(self):
        upper_ticker = self.ticker.upper()

        # displays ticker
        self.dpg.add_text(configs.TICKER_SEARCH_TICKER_TEXT + upper_ticker)

        # market cap
        self.dpg.add_text(configs.TICKER_SEARCH_MARKET_CAP_STOCK_TEXT + yft.get_market_cap(upper_ticker))

        # shares shorted
        self.dpg.add_text(configs.TICKER_SEARCH_SHARES_SHORTED_STOCK_TEXT + yft.get_shares_short(upper_ticker))

        # shares shorted prior month
        self.dpg.add_text(
            configs.TICKER_SEARCH_SHARES_SHORTED_PRIOR_MONTH_TEXT + yft.get_shares_short_prior_month(upper_ticker))

        # short percent float
        self.dpg.add_text(configs.TICKER_SEARCH_SHORT_PERCENT_TEXT + yft.get_short_percent_float(upper_ticker))

        # summary of business
        self.dpg.add_text(configs.TICKER_SEARCH_SUMMARY_OF_BUSINESS_STOCK_TEXT)
        self.dpg.add_text(default_value=yft.get_long_business_summary(upper_ticker),
                          wrap=configs.TICKERS_SEARCH_WRAP_COUNT)

    def cleanup_aliases(self):
        self.dpg.remove_alias(configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID)
