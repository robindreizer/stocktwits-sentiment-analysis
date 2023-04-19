import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import html
import string
import warnings
warnings.filterwarnings('ignore')

import StockTwitsAPI as tw

def get_dates(scraped_posts):
    return [msg['created_date'] for msg in scraped_posts]


def get_times(scraped_posts):
    return [msg['created_time'] for msg in scraped_posts]


def get_watchers(scraped_posts):
    return [msg['symbol']['watchlist_count'] for msg in scraped_posts]


def get_sentiment(scraped_posts):
    return [msg['sentiment'] for msg in scraped_posts]


def get_text(scraped_posts):
    return [msg['body'] for msg in scraped_posts]


def get_tickers(scraped_posts):
    return [msg['symbol']['symbol'] for msg in scraped_posts]


def get_datetimes(scraped_posts):
    dates = get_dates(scraped_posts)
    times = get_times(scraped_posts)

    datetimes = zip(dates, times)
    datetimes = pd.DataFrame(datetimes)
    datetimes = datetimes.loc[:, 0] + " " + datetimes.loc[:, 1]
    datetimes = pd.to_datetime(datetimes).dt.tz_convert('US/Eastern')

    return datetimes


def get_stocktwits(tickers, lookback_date, lookback_volume=20000):
    twits_db = []
    twits = tw.Twits()

    i = 0
    print('Scraping:\t', len(tickers), ' tickers')
    for ticker in tickers:
        i += 1
        print('Scraping:\t', ticker)
        res = twits.scrape_ticker(ticker, lookback_volume=lookback_volume, min_date=lookback_date)
        print('Scraped:\t', len(res), '\t twits\n')
        [twits_db.append(msg) for msg in res]

        print("Done ticker:\t", i, '\tof\t', len(tickers),'\n')
        # append ticker data to file
    return twits_db


def convert_to_df(twits_list):
    df = {'dates': get_dates(twits_list),
          'times': get_times(twits_list),
          'datetime': get_datetimes(twits_list),
          'ticker': get_tickers(twits_list),
          'watchers': get_watchers(twits_list),
          'sentiment': get_sentiment(twits_list),
          'text': get_text(twits_list)
          }

    df = pd.DataFrame(data=df)
    bins = np.arange(25)
    df['time_bin'] = pd.cut(df.datetime.dt.hour, bins, right=False)

    return df


# Preprocess & Cleaning
# Function to remove Stopwords
def remove_stopwords(row):
    stopword_list = stopwords.words('english')
    words = []
    for word in row:
        if word not in stopword_list:
            words.append(word)
    return words


# Function to remove emojis
def remove_emoji(tweets):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', tweets)


# Stemmer function
def stem_sentences(sentence):
    # stemmer is used to simplify words to their stem
    stemmer = PorterStemmer()

    tokens = sentence.split()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)


# Preprocessing Function
def tweets_preprocessing(df):
    raw_df = df.copy()

    print('1/10 removing tickers')
    # Removing all tickers from comments
    raw_df['text'] = raw_df['text'].str.replace(r'([$][a-zA-z]{1,5})', '')

    print('2/10 converting to lower case')
    # Make all sentences small letters
    raw_df['text'] = raw_df['text'].str.lower()

    # Converting HTML to UTF-8
    raw_df["text"] = raw_df["text"].apply(html.unescape)

    print('3/10 removing hashtags, etc')
    # Removing hastags, mentions, pagebreaks, handles
    # Keeping the words behind hashtags as they may provide useful information about the comments e.g. #Bullish #Lambo
    raw_df["text"] = raw_df["text"].str.replace(r'(@[^\s]+|[#]|[$])', ' ')  # Replace '@', '$' and '#...'
    raw_df["text"] = raw_df["text"].str.replace(r'(\n|\r)', ' ')  # Replace page breaks

    print('4/10 removing links')
    # Removing https, www., any links etc
    raw_df["text"] = raw_df["text"].str.replace(r'((https:|http:)[^\s]+|(www\.)[^\s]+)', ' ')

    print('5/10 removing numbers')
    # Removing all numbers
    raw_df["text"] = raw_df["text"].str.replace(r'[\d]', '')

    print('6/10 removing emojis')
    # Remove emoji
    raw_df["text"] = raw_df["text"].apply(lambda row: remove_emoji(row))

    print("7/10 tokenizing")
    # Tokenization
    raw_df['text'] = raw_df['text'].apply(word_tokenize)

    print('8/10 removing stopwords')
    # Remove Stopwords
    raw_df['text'] = raw_df['text'].apply(remove_stopwords)

    print('9/10 removing punctuation')
    # Remove Punctuation
    raw_df['text'] = raw_df['text'].apply(lambda row: [word for word in row if word not in string.punctuation])

    # Combining back to full sentences
    raw_df['text'] = raw_df['text'].apply(lambda row: ' '.join(row))

    # Remove special punctuation not in string.punctuation
    raw_df['text'] = raw_df['text'].str.replace(r"\“|\”|\‘|\’|\.\.\.|\/\/|\.\.|\.|\"|\'", '')

    print('10/10 applying stemmer')
    # Apply stemmer
    raw_df['text'] = raw_df['text'].apply(stem_sentences)

    # Remove all empty rows
    processed_df = raw_df[raw_df['text'].str.contains(r'^\s*$') == False]

    return processed_df


if __name__ == "__main__":

    path = '#path where files are to be written'
    tickers = pd.read_csv(path + 'tickers.csv')
    tickers = tickers.ticker.tolist()
    step = 100
    
    for i in range(600,len(tickers),step):
        
        tkrs = tickers[i:i+step]
        rng = " ticker range "+str(i)+"_"+str(i+step)
        print(rng)
        
        lookback_date = '2022-04-02'
        today = datetime.today().strftime("%d-%m-%Y")
    
        print("\nInitializing twits query")
        twits_db = get_stocktwits(tkrs, lookback_date)
        twits_df = convert_to_df(twits_db)
        print("\nGot twits: ", rng)
        print(twits_df.shape)
    
        # Clean up twits
        print('\nprocessing twits')
        twits_df = tweets_preprocessing(twits_df)
    
        # load model
        with open('twit_classification_model.pkl', 'rb') as f:
            clf = pickle.load(f)
    
        print('\nClassifying no sentiment twits')
        not_classified = twits_df.sentiment == 'N/A'
        twits_df[~not_classified].to_csv(path + "\\ScrapedTwits\\" + 'labeled_twits_data ' + lookback_date + '_to_' + today + rng +'.csv')
    
        twits_df.sentiment[not_classified] = clf.predict(twits_df[not_classified].text)
        print('\nFinished')
    
        twits_df.to_csv(path + "\\ScrapedTwits\\" + 'scraped_twits_data ' + lookback_date + '_to_' + today + rng +'.csv')
        print('\nfile written')
        
    # Combine all separate files in one
    
    # Pivot and produce final file
    #data = pd.pivot_table(data, values='watchers', index=['dates', 'ticker'],
    #                columns=['sentiment'], aggfunc='count', fill_value=0)
    #data.to_csv(path+"SentimentDB\\SentimentData "+ lookback_date + '_to_' + today + rng +'.csv'')
    












































