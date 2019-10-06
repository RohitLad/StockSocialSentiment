from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import StripeKeys
import stripe


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
stripe.api_key = StripeKeys.SECRET_KEY