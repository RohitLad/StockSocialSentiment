import regex as re
from collections import Counter
import sqlite3
import pandas as pd
import pathlib
from nltk import word_tokenize
from nltk.corpus import stopwords
stops = stopwords.words('english')
stops.append('https')

def bag_of_words(series):

    document = ' '.join([row for row in series])

    tokens = [word for word in word_tokenize(document.lower()) if word.isalpha()]

    tokens = [word for word in re.findall(r'[A-Za-z]+', ' '.join(tokens))]

    no_stop = [word for word in tokens if word not in stops]

    return Counter(no_stop)

def get_tweet_data():
    con = sqlite3.connect('app/tweets.sqlite')
    statement = 'SELECT * FROM tweet'
    df = pd.read_sql_query(statement, con)
    return df

def preprocess_nltk(row):
    """
    preprocessing the user description for user tagging
    Parameters
    ----------
        row: string
            a single record of a user's profile description
    
    Returns
    -------
        string
            a clean string
    """

    # lowercasing, tokenization, and keep only alphabetical tokens
    tokens = [word for word in word_tokenize(row.lower()) if word.isalpha()]

    # filtering out tokens that are not all alphabetical
    tokens = [word for word in re.findall(r'[A-Za-z]+', ' '.join(tokens))]

    # remove all stopwords
    no_stop = [word for word in tokens if word not in stops]

    return ' '.join(no_stop)

chart_colors = [
    '#664DFF',
    '#893BFF',
    '#3CC5E8',
    '#2C93E8',
    '#0BEBDD',
    '#0073FF',
    '#00BDFF',
    '#A5E82C',
    '#FFBD42',
    '#FFCA30'
]

app_color = {
    "graph_bg": "rgb(221, 236, 255)",
    "graph_line": "rgb(8, 70, 151)",
    "graph_font":"rgb(2, 29, 65)"
}

keywords_to_hear = ['TSLA','MSFT','GOOG','AAPL']