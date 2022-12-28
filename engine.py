# The engine retrieves symbols from the mysql db
# and checks their status. If active, a call is made to Stocktwits.
# The data is pulled and stored to appropriate table if available.
# If unavailable, symbol is switched to inactive.
# Trigger at pre-determined intervals.

SLEEP_TIMER = 600 # seconds

from datetime import timedelta
import pandas as pd
import MySQLdb
import StockTwitsAPI as api

# establish DB connection
con = MySQLdb.connect(host="localhost",
                      user="root",
                      passwd="mysqldb",
                      db="sentiment_analytics")

query = "select * from sentiment_analytics.stocks"
stocks = pd.read_sql(query, con=con)
stocks = stocks.symbol.to_list()

for ticker in stocks:
    twit = api.Twits()