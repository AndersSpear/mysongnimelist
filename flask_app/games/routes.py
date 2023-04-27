from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time


games=Blueprint('games', __name__)

@games.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("games.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@games.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = game_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("games.index"))

    return render_template("query.html", results=results)


@games.route("/games/<game_id>", methods=["GET", "POST"])
def game_Detail(game_id):
    try:
        result = game_client.retrieve_game_by_id(game_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    form = GameReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            rawg_id=game_id,
            game_title=result.title,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(rawg_id=game_id)

    return render_template(
        "game_detail.html", form=form, game=result, reviews=reviews
    )


@games.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)

