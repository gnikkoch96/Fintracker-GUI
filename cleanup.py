import configs
import firebase_conn


# calculates the total profit
def calculate_total_profit(self):
    # get all closed trades
    closed_trades_crypto_stock = firebase_conn.get_closed_trades_db(self.user_id, False)
    closed_trades_options = firebase_conn.get_closed_trades_db(self.user_id, True)

    # sum the net profit column for crypto stock table
    total_profit = 0
    for closed_trade_id in closed_trades_crypto_stock:
        closed_trade = firebase_conn.get_closed_trade_by_id(self.user_id, closed_trade_id, False)

        total_profit += float(closed_trade[configs.FIREBASE_NET_PROFIT])

    # sum the net profit column for options table
    for closed_trade_id in closed_trades_options:
        closed_trade = firebase_conn.get_closed_trade_by_id(self.user_id, closed_trade_id, True)

        total_profit += float(closed_trade[configs.FIREBASE_NET_PROFIT])

    return total_profit

# calculates the win rate
def calculate_win_rate(self):
    # get all closed trades
    closed_trades_crypto_stock = firebase_conn.get_closed_trades_db(self.user_id, False)
    closed_trades_options = firebase_conn.get_closed_trades_db(self.user_id, True)

    loss_trades = 0
    win_trades = 0

    # count the number of negative percentages and positive percentages for crypto and stock
    for closed_trade_id in closed_trades_crypto_stock:
        closed_trade = firebase_conn.get_closed_trade_by_id(self.user_id, closed_trade_id, False)

        if closed_trade[configs.FIREBASE_NET_PROFIT] > 0:
            win_trades += 1
        else:
            loss_trades += 1

    # count the number of negative percentages and positive percentages for options
    for closed_trade_id in closed_trades_options:
        closed_trade = firebase_conn.get_closed_trade_by_id(self.user_id, closed_trade_id, True)

        if closed_trade[configs.FIREBASE_NET_PROFIT] > 0:
            win_trades += 1
        else:
            loss_trades += 1

    # win-rate is the number of wins from total trade
    return round(win_trades/(loss_trades+win_trades), 2)

