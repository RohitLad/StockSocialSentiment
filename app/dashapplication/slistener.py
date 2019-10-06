from tweepy.streaming import StreamListener
import json
import time
import sys
import pandas as pd
from sqlalchemy import create_engine


class SListener(StreamListener):

    def __init__(self, api=None, fprefix='streamer'):
        
        self.api = api
        self.cnt = 0
        self.engine = create_engine('sqlite:///app/tweets.sqlite')

    def on_status(self, status):
        self.cnt+=1
        status_json = json.dumps(status._json)
        status_data = json.loads(status_json)
        full_text_list = [status_data['text']]

        if 'extended_tweet' in status_data:
            full_text_list.append(status_data['extended_tweet']['full_text'])
        if 'retweeted_status' in status_data and 'extended_tweet' in status_data['retweeted_status']:
            full_text_list.append(status_data['retweeted_status']['extended_tweet']['full_text'])
        if 'quoted_status' in status_data and 'extended_tweet' in status_data['quoted_status']:
            full_text_list.append(status_data['quoted_status']['extended_tweet']['full_text'])

        full_text = max(full_text_list, key=len)

        tweets = {
            'created_at': status_data['created_at'],
            'text':  full_text,
            #'user': status_data['user']['description']
        }

        #print("Writing tweet # {} to the database".format(self.cnt))
        #print("Tweet Created at: {}".format(tweets['created_at']))
        print("Tweets Content:{}".format(tweets['text']))
        #print("User Profile: {}".format(tweet['user']))
        #print()

        df = pd.DataFrame(tweets, index=[0])

        df['created_at'] = pd.to_datetime(df.created_at)
        df.to_sql('tweet', con=self.engine, if_exists='append')

        with self.engine.connect() as con:
            con.execute("""
                        DELETE FROM tweet
                        WHERE created_at in(
                            SELECT created_at
                                FROM(
                                    SELECT created_at, strftime('%s','now') - strftime('%s',created_at) AS time_passed
                                    From tweet
                                    WHERE time_passed >= 60))""")