import os
basedir = os.path.abspath(os.path.dirname(__file__))

GRAPH_INTERVAL = 2000

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']

class StripeKeys:
    SECRET_KEY = 'sk_test_h36oicOrlA7ATkI9JJ6dUGyA'
    PUBLISHABLE_KEY = 'pk_test_8Xho4FfArFFuQspdH8V1KlHS'

class TwitterKeys:
    KEY = 'xEGpeFLSEoWdLsDnhExw9OLFf'
    KEY_SECRET = '47tNPJem7XdNSGAPwMUrv7CfwYTFU2xLd3lYbFHJG4XjYu1B4N'
    TOKEN = '495699194-nep4t0NsbDzIRwc5yoCSKqqNtpD458MN5gm6Os3m'
    TOKEN_SECRET = 'LSxidWqwgOEtspAHM5dqHNcBKzzZQpM99UnH87t2omy60'
