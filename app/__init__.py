import dash
#import stripe
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from config import BaseConfig, StripeKeys, GRAPH_INTERVAL
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def nltk_downloader():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('vader_lexicon')

def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)
    #stripe.api_key = StripeKeys.SECRET_KEY
    nltk_downloader()
    register_dashapp(server)
    register_extensions(server)
    register_blueprints(server)
    return server


def register_dashapp(server):
    from app.dashapplication.layout import layout
    from app.dashapplication.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    dashapp = dash.Dash(__name__,
                        server=server,
                        url_base_pathname='/dashboard/',
                        assets_folder=get_root_path(__name__)+'/dashboard/assets/',
                        meta_tags = [meta_viewport]
    )
    
    with server.app_context():
        dashapp.title = 'Dashapp'
        dashapp.layout = layout
        register_callbacks(dashapp)

    _protect_dashviews(dashapp)

def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db, login, migrate
    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)

def register_blueprints(server):
    from app.webapp import server_bp
    server.register_blueprint(server_bp)