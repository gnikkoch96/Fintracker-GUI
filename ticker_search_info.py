import configs
import yfinance_tool as yft
import cngko_tool as cgt

class CryptoStockInfo:
    def __init__(self, dpg, ticker, is_crypto=False):
        self.dpg = dpg
        self.ticker = ticker
        self.is_crypto = is_crypto
        self.create_search_win()

    def create_search_win(self):
        with self.dpg.window(tag=configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID,
                             label=configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_TEXT,
                             width=configs.TICKER_SEARCH_WINDOW_VIEWPORT_SIZE[0],
                             height=configs.TICKER_SEARCH_WINDOW_VIEWPORT_SIZE[1],
                             on_close=self.cleanup,
                             modal=True):
            if self.is_crypto:  # loads crypto info
                self.create_search_win_crypto_items()
            else:  # loads stock info
                self.create_search_win_stock_items()

    def create_search_win_crypto_items(self):
        pass

    def create_search_win_stock_items(self):
        # displays ticker
        self.dpg.add_text(configs.TICKER_SEARCH_TICKER_STOCK_TEXT + self.ticker.upper())

        # market cap
        self.dpg.add_text(configs.TICKER_SEARCH_MARKET_CAP_STOCK_TEXT + yft.get_market_cap(self.ticker))

        # shares shorted
        self.dpg.add_text(configs.TICKER_SEARCH_SHARES_SHORTED_STOCK_TEXT + yft.get_shares_short(self.ticker))

        # shares shorted prior month
        self.dpg.add_text(
            configs.TICKER_SEARCH_SHARES_SHORTED_PRIOR_MONTH_TEXT + yft.get_shares_short_prior_month(self.ticker))

        # short percent float
        self.dpg.add_text(configs.TICKER_SEARCH_SHORT_PERCENT_TEXT + yft.get_short_percent_float(self.ticker))

        # summary of business
        self.dpg.add_text(configs.TICKER_SEARCH_SUMMARY_OF_BUSINESS_STOCK_TEXT)
        self.dpg.add_text(default_value=yft.get_long_business_summary(self.ticker),
                          wrap=configs.TICKERS_SEARCH_WRAP_COUNT)

    def cleanup(self):
        self.dpg.remove_alias(configs.TICKER_SEARCH_CRYPTO_STOCK_WINDOW_ID)
