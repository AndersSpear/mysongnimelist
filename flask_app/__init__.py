# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
# from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_dance.contrib.discord import make_discord_blueprint, discord
import ssl

# stdlib
from datetime import datetime
import os

# local
from .client import SongClient


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
song_client = SongClient()
app = Flask(__name__)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

from .users.routes import users
from .songs.routes import songs
from .discord.routes import discordd 

def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_error_handler(404, page_not_found)

    app.register_blueprint(discordd, url_prefix="/login")
    app.register_error_handler(404, page_not_found)

    app.register_blueprint(songs)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app

# if __name__ == '__main__':

#     app.config.from_pyfile("config.py", silent=False)

#     db.init_app(app)
#     login_manager.init_app(app)
#     bcrypt.init_app(app)

#     app.register_blueprint(users)
#     app.register_error_handler(404, page_not_found)

#     app.register_blueprint(discordd)
#     app.register_error_handler(404, page_not_found)

#     app.register_blueprint(songs)
#     app.register_error_handler(404, page_not_found)

#     login_manager.login_view = "users.login"
#     app.run(debug=True, ssl_context=context)
