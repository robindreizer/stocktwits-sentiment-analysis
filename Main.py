# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 21:07:46 2021

@author: Ardi
"""

import requests
import pandas as pd
import numpy as np
import StockTwitsAPI as api
import time
import datetime

n = 0
loop = 0

symbols = ["AAPL"]

while True:
    # restart loop on symbols
    loop += 1

    twit = api.Twits()
    ticker = symbols[0]
    symbol, conn = twit.get_symbol_data(ticker, limit=0)
    cur_time = datetime.datetime.now()
    watchers = int(symbol['watchlist_count'])

    data_row = pd.DataFrame({'ticker': ticker,
                             'watchers': watchers,
                             'Timestamp': cur_time},
                            index=[0])

    #data_row.to_csv("C:\\Users\\Ardi\\Desktop\\StockWatchers\\watchersdata.csv",
    #                mode='a', header=False)

    for ticker in symbols:
        n += 1

        if n % 1000 == 0:
            print("Updated:\t", n)

        try:
            symbol, conn = twit.get_symbol_data(ticker, limit=0)
        except:
            print("Cannot recognize Ticker")
            if ticker in symbols:
                symbols.remove(ticker)
            continue

        try:
            ticker = symbol['symbol']
            watchers = int(symbol['watchlist_count'])

        except:
            print(ticker, " not able to get watchers")
            continue
        # calls_left = int(conn['X-RateLimit-Remaining'])
        # limit = int(conn['X-RateLimit-Limit'])
        cur_time = datetime.datetime.now()
        # limit_reset = datetime.datetime.fromtimestamp(int(conn['X-RateLimit-Reset']))

        data_row = pd.DataFrame({'ticker': ticker,
                                 'watchers': watchers,
                                 'Timestamp': cur_time},
                                index=[0])

        data_row.to_csv("C:\\Users\\robin\\OneDrive\\Desktop\\watchers\\watchersdata.csv",
                        mode='a', header=True)

        # print("recorded\t", ticker, "\twatchers:\t", watchers, '\t time:\t', cur_time)

    print("Number of loops:\t", loop)
    print("All Symbols done")
    print("6 hr break break")
    print("Limit reset at:", datetime.datetime.now() + datetime.timedelta(hours=6))
    time.sleep(60 * 60 * 6)




















