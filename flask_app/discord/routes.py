from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_dance.contrib.discord import make_discord_blueprint, discord
from urllib import parse
from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User
import os, requests

API_ENDPOINT = 'https://discord.com/api/v10'
REDIRECT_URI = 'https://127.0.0.1:5000/callback'
OAUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id=1102379414114807878&redirect_uri={parse.quote(REDIRECT_URI)}&response_type=code&scope=identify'

discordd = make_discord_blueprint(
    client_id='1102379414114807878',
    client_secret='qC5nJBaWR6RgPmO8OUopkdCFbHfB-a1L',
    redirect_url='https://127.0.0.1:5000/callback',
)


@discordd.route("/")
def index():
    if not discord.authorized:
        return redirect(url_for("discord.login"))
    resp = discord.get("/api/users/@me")
    return redirect(url_for('discord.logout'))


@discordd.route("/callback")
def callback():
    code = request.args['code']
    data = {
        'client_id': '1102379414114807878',
        'client_secret': 'qC5nJBaWR6RgPmO8OUopkdCFbHfB-a1L',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    resp = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    json = resp.json()
    access_token = json['access_token']

    new_headers = {"Authorization": f"Bearer {access_token}"}
    resp2 = requests.get("https://discord.com/api/oauth2/@me", headers=new_headers)

    if resp2.status_code == 200:
        user_info = resp2.json()
        return "YOUR NAME IS " + user_info['user']['username']
    else:
        return "Invalid"


@discordd.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
