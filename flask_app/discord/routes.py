from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_dance.contrib.discord import make_discord_blueprint, discord

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User

discordd = make_discord_blueprint(
    client_id="1102379414114807878",
    client_secret="LAgNwjE9Qxh_DOZJWmipPOMFVuLSlEYe"
)


@discordd.route("/")
def index():
    if not discord.authorized:
        return redirect(url_for("discord.login"))
    resp = discord.get("/api/users/@me")
    return render_template("song.html")


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for('index'))