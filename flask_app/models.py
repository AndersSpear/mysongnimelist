from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    total_reviews = db.IntegerField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=1000)
    date = db.DateField(required=True) # format='%Y-%m-%d
    rawg_id = db.StringField(required=True, min_length=1, max_length=50)
    game_title = db.StringField(required=True, min_length=1, max_length=100)
    avg_rating = db.DecimalField(required=True,places=2,rounding=Decimal.ROUND_HALF_EVEN)
