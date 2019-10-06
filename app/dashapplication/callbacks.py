from dash.dependencies import Input
from dash.dependencies import Output
from utils import get_tweet_data, bag_of_words, chart_colors, preprocess_nltk, app_color
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import deque, Counter
import plotly
import plotly.graph_objs as go
import numpy as np
import datetime
from utils import keywords_to_hear

sid = SentimentIntensityAnalyzer()
num_tags_scatter = 5
X_universal = deque(maxlen=30)
sentiment_dict = {}
for word in keywords_to_hear:
    sentiment_dict[word] = deque(maxlen=30)

def register_callbacks(dashapp):
    @dashapp.callback(Output('sentiment_scores', 'figure'),
    [Input('query_update', 'n_intervals')])

    def update_graph(interval):
       
        # query tweets from the database
        df = get_tweet_data()
        # preprocess the text column
        #df['text_processed'] = df.text.apply(preprocess_nltk)
        wt = 0.5
        sentiments = {word: 0. for word in keywords_to_hear}

        for sentence in df['text']:
            processed_sentence = preprocess_nltk(sentence)
            for word in keywords_to_hear:
                if word in sentence:
                    sentiment = sid.polarity_scores(processed_sentence)['compound']
                    sentiments[word] = wt*sentiments[word] + (1.-wt)*sentiment

        for word in keywords_to_hear:
            sentiment_dict[word].append(sentiments[word])

        # get the current time for x-axis
        time = datetime.datetime.now().strftime('%D, %H:%M:%S')
        X_universal.append(time)

        data=[go.Scatter(
            x=list(X_universal),
            y=list(sentiment_dict[ticker]),
            name=ticker,
            mode = 'lines+markers') for ticker in keywords_to_hear]


        layout = go.Layout(
                xaxis={
                    'automargin': False,
                    'range': [min(X_universal), max(X_universal)],
                    'title': 'Current Time (GMT)',
                    'nticks': 2,
                },
                yaxis={
                    'autorange': True,
                    'title': 'Sentiment Score'
                },
                height=400,
                plot_bgcolor=app_color["graph_bg"],
                paper_bgcolor=app_color["graph_bg"],
                font={"color": app_color["graph_font"]},
                autosize=False,
                legend={
                    'orientation': 'v',
                },
                margin=go.layout.Margin(
                    l=75,
                    r=25,
                    b=70,
                    t=25,
                    pad=4
                ),
            )

        return go.Figure(
            data=data,
            layout=layout,)


def register_callbacks_mod(dashapp):
    @dashapp.callback(Output('sentiment_scores', 'figure'),
    [Input('query_update', 'n_intervals')])

    def update_graph(interval):
       
        # query tweets from the database
        df = get_tweet_data()
        # get the number of tweets for each keyword
        cnt = bag_of_words(df['text'])

        # get top-N words
        top_N = cnt.most_common(num_tags_scatter)
        top_N_words = [keyword for keyword, cnt in top_N]

        # preprocess the text column
        df['text'] = df.text.apply(preprocess_nltk)

        sentiments = {keyword:[] for keyword in top_N_words}

        for row in df['text']:
        # print(row)
            for keyword in top_N_words:
                # print(keyword)
                if keyword.lower() in row.lower():
                    # print(sid.polarity_scores(row)['compound'])
                    sentiments[keyword].append(sid.polarity_scores(row)['compound'])

        avg_sentiments = {}

        for keyword, score_list in sentiments.items():
            avg_sentiments[keyword] = [np.mean(score_list), np.std(score_list)]

        # get the current time for x-axis
        time = datetime.datetime.now().strftime('%D, %H:%M:%S')
        X_universal.append(time)

        to_pop = []
        for keyword, score_queue in sentiment_dict.items():
            if score_queue:
                while score_queue and (score_queue[0][1] <= X_universal[0]):
                    score_queue.popleft()
            else:
                to_pop.append(keyword)

        for keyword in to_pop:
            sentiment_dict.pop(keyword)

        for keyword, score in avg_sentiments.items():
            if keyword not in sentiment_dict:
                sentiment_dict[keyword] = deque(maxlen=30)
                sentiment_dict[keyword].append([score, time])
            else:
                sentiment_dict[keyword].append([score, time])

        new_colors = chart_colors[:len(sentiment_dict)]

        # plot the scatter plot
        data=[go.Scatter(
            x=[time for score, time in score_queue],
            y=[score[0] for score, time in score_queue],
            error_y={
                "type": "data",
                "array": [score[1]/30 for score, time in score_queue],
                "thickness": 1.5,
                "width": 1,
                "color": "#000",
            },
            name=keyword,
            mode='markers',
            opacity=0.7,
            marker=dict(color=color)
        ) for color, (keyword, score_queue) in list(zip(new_colors, sentiment_dict.items()))]

        # specify the layout
        layout = go.Layout(
                xaxis={
                    'automargin': False,
                    'range': [min(X_universal), max(X_universal)],
                    'title': 'Current Time (GMT)',
                    'nticks': 2,
                },
                yaxis={
                    'autorange': True,
                    'title': 'Sentiment Score'
                },
                height=400,
                plot_bgcolor=app_color["graph_bg"],
                paper_bgcolor=app_color["graph_bg"],
                font={"color": app_color["graph_font"]},
                autosize=False,
                legend={
                    'orientation': 'v',
                    # 'xanchor': 'right',
                    # 'yanchor': 'middle',
                    # 'x': 0.5,
                    # 'y': 1.025
                },
                margin=go.layout.Margin(
                    l=75,
                    r=25,
                    b=70,
                    t=25,
                    pad=4
                ),
            )

        return go.Figure(
            data=data,
            layout=layout,)