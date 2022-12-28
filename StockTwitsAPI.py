import requests

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

        url = self.url + 'streams/trending' + '.json?access_token=' + self.token

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

        r = requests.get(url, headers={'x-ratelimit-limit': 'True'}, params=data)
        if r.status_code != 200:
            if r.status_code == 429:
                raise Exception('Rate limit exceeded. Client may not make more than 400 requests an hour {}'
                                .format(r.status_code))

            raise Exception('Unable to Return Request {}'
                            .format(r.status_code))

        raw_json = r.json()

        return raw_json['symbol'], r.headers

    def scrape_ticker(self, symbol_id, lookback_volume):

        '''Returns a list of historical messages for the symbol, including msg text, user and symbol info.
        Args:
            ticker:	Ticker symbol, Stock ID, or
                        RIC code of the symbol (Required)
            lookback_volume: The amount of messages to retrieve

        Return:
            list of messages, user and symbol data
            contains:
                - ticker
                - company name
                - watchlist count
                - user info
                - sentiment
                - text
                - date and time
        '''
        counter = 0
        failures = 0
        msg_limit = 30

        master_contents = []

        try:
            msgs = self.get_symbol_msgs(symbol_id=symbol_id, limit=msg_limit)
            first_id = msgs[0]['messages'][0]['id'] - 1
            print('Querying Initialized')
        except Exception:
            print('Error:\tAPI Query Failed to Yield Messages on Initial Query\t', Exception)
            return -1

        for _ in range(int(msg_limit * lookback_volume / msg_limit)):

            try:
                time.sleep(1)
                msgs = self.get_symbol_msgs(symbol_id=symbol_id, max=int(first_id), limit=msg_limit)
                first_id = msgs[0]['messages'][-1]['id'] - 1
            except Exception:
                print('Error:\tAPI Query Failed to Yield Messages on Secondary Query\t', Exception)
                print('Sleeping 30 sec')
                time.sleep(30)
                print('Retrying')
                msgs = self.get_symbol_msgs(symbol_id=symbol_id, max=int(first_id), limit=msg_limit)
                first_id = msgs[0]['messages'][-1]['id'] - 1
                failures += 1

            for item in msgs[0]['messages']:
                ticker_dict = {}
                ticker_dict['msg_id'] = item['id']

                msg_sym_index = [symbol['symbol'] for symbol in item['symbols']].index(symbol_id)
                ticker_dict['symbol'] = item['symbols'][msg_sym_index]

                ticker_dict['ticker_title'] = item['symbols'][0]['title']
                ticker_dict['body'] = item['body']
                ticker_dict['created_date'] = item['created_at'].split('T')[0]
                ticker_dict['created_time'] = item['created_at'].split('T')[1]
                ticker_dict['user'] = item['user']

                try:
                    ticker_dict['sentiment'] = item['entities']['sentiment']['basic']
                except TypeError:
                    ticker_dict['sentiment'] = "N/A"

                master_contents.append(ticker_dict)

            counter += msg_limit
            if counter % 1000 == 0:
                print('Fetched:\t', counter, '\tFailures:\t', failures)

            if counter >= lookback_volume:
                break

        return master_contents

# improving the scraper function
# 1. remove the len(master contents) replace with an incrementer -- done
# 2. insert a start date limiter
# 3. insert a max id limiter, both can be none
# 4. insert a timer feature with T/F
# 5. figure out why the counter doesn't work past 10k
# 6. really need a better logging system / progress tracking
