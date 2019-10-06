from tweepy import OAuthHandler, API, Stream
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from urllib3.exceptions import ProtocolError
#from config import TwitterKeys
from slistener import SListener
keywords_to_hear = ['TSLA','MSFT','GOOG','AAPL']

class TwitterKeys:
    KEY = 'xEGpeFLSEoWdLsDnhExw9OLFf'
    KEY_SECRET = '47tNPJem7XdNSGAPwMUrv7CfwYTFU2xLd3lYbFHJG4XjYu1B4N'
    TOKEN = '495699194-nep4t0NsbDzIRwc5yoCSKqqNtpD458MN5gm6Os3m'
    TOKEN_SECRET = 'LSxidWqwgOEtspAHM5dqHNcBKzzZQpM99UnH87t2omy60'

auth = OAuthHandler(TwitterKeys.KEY, TwitterKeys.KEY_SECRET)
auth.set_access_token(TwitterKeys.TOKEN, TwitterKeys.TOKEN_SECRET)
api = API(auth)

listen = SListener(api)
stream = Stream(auth,listen)


engine = create_engine("sqlite:///app/tweets.sqlite")
# if the database does not exist
if not database_exists(engine.url):
    # create a new database
    create_database(engine.url)
# begin collecting data
while True:
    # maintian connection unless interrupted
    try:
        stream.filter(track=keywords_to_hear)
    # reconnect automantically if error arise
    # due to unstable network connection
    except (ProtocolError, AttributeError):
        continue
