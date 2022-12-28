# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 21:07:46 2021

@author: Ardi
"""

import requests
import pandas as pd
import numpy as np
import time
import datetime

class Twits():
    
    def __init__(self):
        self.token = "fda2d6a42e36b9337c7bfc0d5263a05ca04040f2"
        self.url = "https://api.stocktwits.com/api/2/"
        self.headers = {'Content-Type': 'application/json'}
        
    def printUrl(self):
        print(self.url)
        
    def get_user_msgs(self, user_id, since=0, max=0, limit=0, callback=None, filter=None):

        """Returns the most recent 30 messages for the specified user.
        Args:
            user_id (int) = User ID or Username of the stream's user
                            you want to show (Required)
            since (int) = Returns results with an ID greater than (
                          more recent than) the specified ID.
            max (int) = Returns results with an ID less than
                        (older than) or equal to the specified ID.
            limit (int) = Default and max limit is 30.
                          This limit must be a number under 30.
            callback = Define your own callback function name,
                       add this parameter as the value.
            filter (string) = Filter messages by links, charts, or videos.
                              (Optional)
        Return:
            raw_json (dict) = The JSON output unparsed
        """

        url = self.url + 'streams/user/' + user_id + '.json?access_token=' + self.token

        data = {
                 'since': '{}'.format(since),
                 'max': '{}'.format(max),
                 'limit': '{}'.format(limit),
                 # Fix when you figure out what this is
                 # 'callback' : '{}'.format(None),
                 'filter': '{}'.format(filter)
                }

        r = requests.get(url, headers=self.headers, params=data)
        if r.status_code != 200:
            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()
        return raw_json, r.headers

    def get_symbol_msgs(self, symbol_id, since=0, max=0, limit=0, callback=None, filter=None):

        '''Returns the most recent 30 messages for the specified symbol.
        Args:
            symbol_id:	Ticker symbol, Stock ID, or
                        RIC code of the symbol (Required)
            since:	Returns results with an ID greater than (more recent than)
                    the specified ID.
            max:	Returns results with an ID less than (older than) or
                    equal to the specified ID.
            limit:	Default and max limit is 30. This limit must be a
                    number under 30.
            callback:	Define your own callback function name,
                        add this parameter as the value.
            filter:	Filter messages by links, charts, videos,
                    or top. (Optional)
        Return:
            raw_json (dict) = The JSON output unparsed
        '''

        url = self.url + 'streams/symbol/' + symbol_id + '.json?access_token=' + self.token

        data = {
                 'since': '{}'.format(since),
                 'max': '{}'.format(max),
                 'limit': '{}'.format(limit),
                 # Fix when you figure out what this is
                 # 'callback' : '{}'.format(None),
                 'filter': '{}'.format(filter)
                }

        r = requests.get(url, headers=self.headers, params=data)
        if r.status_code != 200:
            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()
        return raw_json, r.headers

    def get_specified_conversation_msgs(self, conversation_id, since=0, max=0, limit=0, callback=None):

        '''
        Args:
            conversation_id:	The message ID of the parent message
                                to a conversation. (Required)
            since:	Returns results with an ID greater than (more recent than)
                    the specified ID.
            max:	Returns results with an ID less than (older than) or equal
                    to the specified ID.
            limit:	Default and max limit is 30. This limit must be a
                    number under 30.
            callback:	Define your own callback function name, add this
                        parameter as the value.
        Return:
            raw_json (dict) = The JSON output unparsed
        '''

        url = self.url + 'streams/conversation/' + conversation_id + '.json?access_token=' + self.token

        data = {
                 'since': '{}'.format(since),
                 'max': '{}'.format(max),
                 'limit': '{}'.format(limit)
                 # Fix when you figure out what this is
                 # 'callback' : '{}'.format(None),
                }

        r = requests.get(url, headers=self.headers, params=data)
        if r.status_code != 200:
            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()
        return raw_json, r.headers
    
    
    def get_trending_msgs(self, since=0, max=0, limit=0, callback=None):

        '''
        Returns the most recent 30 messages with trending symbols in the last 5 minutes.
        
        Args:
            since:	Returns results with an ID greater than (more recent than)
                    the specified ID.
            max:	Returns results with an ID less than (older than) or equal
                    to the specified ID.
            limit:	Default and max limit is 30. This limit must be a
                    number under 30.
            callback:	Define your own callback function name, add this
                        parameter as the value.
        Return:
            raw_json (dict) = The JSON output unparsed
        '''

        url = self.url + 'streams/trending'  + '.json?access_token=' + self.token

        data = {
                 'since': '{}'.format(since),
                 'max': '{}'.format(max),
                 'limit': '{}'.format(limit)
                 # Fix when you figure out what this is
                 # 'callback' : '{}'.format(None),
                }

        r = requests.get(url, headers=self.headers, params=data)
        if r.status_code != 200:
            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()
        return raw_json, r.headers
    
    def get_suggested_msgs(self, since=0, max=0, limit=0, callback=None):

        '''
        Returns the most recent 30 messages from our suggested users,
        a curated list of quality Stocktwits contributors.
        
        Args:
            since:	Returns results with an ID greater than (more recent than)
                    the specified ID.
            max:	Returns results with an ID less than (older than) or equal
                    to the specified ID.
            limit:	Default and max limit is 30. This limit must be a
                    number under 30.
            callback:	Define your own callback function name, add this
                        parameter as the value.
        Return:
            raw_json (dict) = The JSON output unparsed
        '''

        url = self.url + 'streams/suggested' + '.json?access_token=' + self.token

        data = {
                 'since': '{}'.format(since),
                 'max': '{}'.format(max),
                 'limit': '{}'.format(limit)
                 # Fix when you figure out what this is
                 # 'callback' : '{}'.format(None),
                }

        r = requests.get(url, headers=self.headers, params=data)
        if r.status_code != 200:
            if r.status_code == 429:
                raise Exception('Rate limit exceeded. Client may not make more than 400 requests an hour {}'
                                .format(r.status_code))
                                
            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()
        return raw_json, r.headers
    
    def get_symbol_data(self, symbol_id, since=0, max=0, limit=0, callback=None, filter=None):

        '''Returns the id, ticker, aliases, if following, watchlist count for given ticker.
        Args:
            symbol_id:	Ticker symbol, Stock ID, or
                        RIC code of the symbol (Required)
            since:	Returns results with an ID greater than (more recent than)
                    the specified ID.
            max:	Returns results with an ID less than (older than) or
                    equal to the specified ID.
            limit:	Default and max limit is 30. This limit must be a
                    number under 30.
            callback:	Define your own callback function name,
                        add this parameter as the value.
            filter:	Filter messages by links, charts, videos,
                    or top. (Optional)
        Return:
            raw_json (dict) = The JSON output unparsed
        '''

        url = self.url + 'streams/symbol/' + symbol_id + '.json?access_token=' + self.token

        data = {
                 'since': '{}'.format(since),
                 'max': '{}'.format(max),
                 'limit': '{}'.format(limit),
                 # Fix when you figure out what this is
                 # 'callback' : '{}'.format(None),
                 'filter': '{}'.format(filter)
                }

        r = requests.get(url, headers={'x-ratelimit-limit' : 'True'}, params=data)
        if r.status_code != 200:
            if r.status_code == 429:
                raise Exception('Rate limit exceeded. Client may not make more than 400 requests an hour {}'
                                .format(r.status_code))
                
            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()
        
        return raw_json['symbol'], r.headers
    
n = 0
loop = 0
symbols = pd.read_csv("C:\\Users\\Ardi\\Desktop\\StockWatchers\\symbols.txt").SYMS.to_list()

while True:
    # restart loop on symbols
    loop += 1

    twit = Twits()
    ticker = symbols[0]
    symbol, conn = twit.get_symbol_data(ticker, limit = 0)
    cur_time = datetime.datetime.now()
    watchers = int(symbol['watchlist_count'])

    data_row = pd.DataFrame({'ticker' : ticker,
                              'watchers' : watchers,
                              'Timestamp' : cur_time},
                               index = [0])

    data_row.to_csv("C:\\Users\\Ardi\\Desktop\\StockWatchers\\watchersdata.csv",
                    mode='a', header=False)
    
    for ticker in symbols:
        n+=1   

        if n % 1000 == 0 :
            print("Updated:\t", n)  
        
        try:
            symbol, conn = twit.get_symbol_data(ticker, limit = 0)
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
        #calls_left = int(conn['X-RateLimit-Remaining'])
        #limit = int(conn['X-RateLimit-Limit'])
        cur_time = datetime.datetime.now()
        #limit_reset = datetime.datetime.fromtimestamp(int(conn['X-RateLimit-Reset']))

        data_row = pd.DataFrame({'ticker' : ticker,
                                 'watchers' : watchers,
                                 'Timestamp' : cur_time},
                                  index = [0])
        
        data_row.to_csv("C:\\Users\\Ardi\\Desktop\\StockWatchers\\watchersdata.csv",
                        mode='a', header=False)
                   
        #print("recorded\t", ticker, "\twatchers:\t", watchers, '\t time:\t', cur_time)
        
        
    print("Number of loops:\t", loop)
    print("All Symbols done")
    print("6 hr break break")
    print("Limit reset at:", datetime.datetime.now() + datetime.timedelta(hours=6))
    time.sleep(60*60*6) 

        
    

















