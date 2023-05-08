from flask_login import UserMixin
from datetime import datetime

from . import db, login_manager
from .utils import current_time
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(unique=True)
    password = db.StringField()

    # Integer field broke so commenting it for now
    # total_reviews = db.IntegerField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=1000)
    date = db.StringField(required=True)
    song_id = db.StringField(required=True, min_length=1, max_length=50)
    song_name = db.StringField(required=True, min_length=1, max_length=100)
    # commenting a broken integer field for now
    #rating = db.IntegerField(required=True,min="0",max="5")
