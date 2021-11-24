import yfinance as yf
import pandas as pd
import numpy as np

desired_width = 1000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 20)


dole = yf.Ticker("DOLE")
# info = dole.info
#
# print(info)

# crypto

# stocks
# print(info['longBusinessSummary'], info['currentPrice'], info['targetHighPrice'], info['targetMeanPrice'], info['sharesShort'], info['sharesShortPriorMonth'],
#       info['shortPercentOfFloat'], info['shortRatio'], info['floatShares'], info['marketCap'])
print(dole.recommendations)


print(dole.major_holders)
print(dole.institutional_holders)
# print(dole.news)

# options
# dole = yf.Ticker("tsla")
# print(len(dole.options))
# print(dole.get_info()['regularMarketPrice'])
# print(dole.option_chain(dole.options[0]))
#
# dole_options = dole.option_chain()
# # print(type(dole_options[0])) # 0 - calls and 1 - puts
# print(dole_options[0]) # 0 - calls and 1 - puts
# print(dole.option_chain(dole.options[0])[0])
# print(dole_options[8] * 100)

