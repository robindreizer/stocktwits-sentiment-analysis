import re
import string
import html
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV


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


# stemmer is used to simplify words to their stem
stemmer = PorterStemmer()


# Stemmer function
def stem_sentences(sentence):
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
####################################################################################################
# Load Classification data!
df = pd.read_csv('dataset.csv', index_col = 0)
processed_df = tweets_preprocessing(df)

# GridSearchCV ML model K-fold training - Multinomial Naive Bayes
def train_model_naive_bayes(training_data):
    # Creating a train test set for labelled comments to train the model using a Moltuinomial NB classifier
    x_train, x_test, y_train, y_test = train_test_split(training_data['text'], training_data['sentiment'],
                                                        test_size=0.2, stratify=training_data['sentiment'])

    # Create pipeline
    pipeline = Pipeline([
        ('bow', CountVectorizer()),  # strings to token integer counts
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('classifier', MultinomialNB())  # train on TF-IDF vectors w/ Naive Bayes classifier
    ])

    # This is where we define the values for GridSearchCV to iterate over
    parameters = {
        'classifier__alpha': [0.00001, 0.0001, 0.001, 0.1, 1, 10],
        'classifier__fit_prior': [True, False]
    }

    # Do 10-fold cross validation for each of the 6 possible combinations of the above params
    grid = GridSearchCV(pipeline, cv=10, param_grid=parameters, verbose=1)
    grid.fit(x_train, y_train)

    return grid, x_test, y_test


# GridSearchCV ML model K-fold training - Logistic Regression
def train_model_logistic_regression(training_data):
    # Creating a train test set for 500k labelled comments to train the model using a Moltuinomial NB classifier
    x_train, x_test, y_train, y_test = train_test_split(training_data['text'], training_data['sentiment'],
                                                        test_size=0.2, stratify=training_data['sentiment'])

    # create pipeline
    pipeline = Pipeline([
        ('bow', CountVectorizer()),  # strings to token integer counts
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('classifier', LogisticRegression())  # train on TF-IDF vectors w/ Naive Bayes classifier
    ])

    # this is where we define the values for GridSearchCV to iterate over
    parameters = {
        'classifier__C': [0.00001, 0.0001, 0.001, 0.1, 1, 10, 100, 1000],
        'classifier__penalty': ['l1', 'l2', 'elasticnet']
    }
    # do 10-fold cross validation for each of the 6 possible combinations of the above params
    grid = GridSearchCV(pipeline, cv=10, param_grid=parameters, verbose=1)
    grid.fit(x_train, y_train)

    return grid, x_test, y_test


# Results & Classification Report
# GridSearch Results
def display_best_result(grid):
    print("\nBest Model: %f using %s" % (grid.best_score_, grid.best_params_))
    print('\n')
    means = grid.cv_results_['mean_test_score']
    stds = grid.cv_results_['std_test_score']
    params = grid.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("Mean: %f Stdev:(%f) with: %r" % (mean, stdev, param))


# Classification report for test set
def display_classification_report(df, grid, y_test, x_test):
    print('Test Set Classification Report')
    y_preds = grid.predict(x_test)
    print('accuracy score: ', accuracy_score(y_test, y_preds))
    print('\n')
    print('confusion matrix: \n', confusion_matrix(y_test, y_preds))
    print('\n')
    print(classification_report(y_test, y_preds))


def run_model(model):
    if model == "NB":
        grid, x_test, y_test = train_model_naive_bayes(training_data)
        display_best_result(grid)
        display_classification_report(processed_df, grid, y_test, x_test)
        return grid

    elif model == "LR":
        grid, x_test, y_test = train_model_logistic_regression(training_data)
        display_best_result(grid)
        display_classification_report(processed_df, grid, y_test, x_test)
        return grid

    else:
        print('Input either:\n1. "NB" - Naive Bayes\n2. "LR" - Logistic Regression')

import warnings
warnings.filterwarnings('ignore')

# Run
if __name__ == '__main__':
    data = processed_df[['sentiment','text']].copy()
    data = data[data["sentiment"].isin(["Bullish", "Bearish"])]  # Filter down into labelled comments

    # Under-sampling 15k of bullish, 15k of bearish to fix imbalance dataset
    bullish_df = data[data["sentiment"] == "Bullish"].sample(15000)
    bearish_df = data[data["sentiment"] == "Bearish"].sample(15000)
    training_data = pd.concat([bullish_df, bearish_df]).sample(frac=1)

    print('\nRunning LR\n')
    lr = run_model("LR") # run logistic regr
    print('\nRunning NB\n')
    nb = run_model("NB") # run naive bayes

    import pickle
    # save model as pickle
    with open('twit_classification_model.pkl','wb') as f:
        pickle.dump(lr,f)

