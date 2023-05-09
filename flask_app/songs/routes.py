from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import song_client
from ..forms import SongReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time, calc_avg_rating


songs=Blueprint('songs', __name__)

@songs.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("songs.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@songs.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = song_client.search(query)
        if results == None:
            flash("No results found.")
            return redirect(url_for("songs.index"))
        # for result in results:
        #     print(result["name"])

    except Exception as e:
        flash(str(e))
        return redirect(url_for("songs.index"))

    return render_template("query.html", results=results)


@songs.route("/songs/<song_id>", methods=["GET", "POST"])
def song_detail(song_id):
    try:
        result = song_client.get_song(song_id)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("songs.index"))

    form = SongReviewForm()
    print("i got here")
    print(form.validate_on_submit())
    print(current_user.is_authenticated)
    if form.validate_on_submit() and current_user.is_authenticated:
        print("statement is true")
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            song_id=song_id,
            song_name=result.song_name,
        )
        print("i got here 2")
        review.save()
        print("i got here 3")
        return redirect(request.path)

    reviews = Review.objects(song_id=song_id)
    
    # avg = calc_avg_rating(reviews)

    return render_template(
        "song_detail.html", form=form, song=result, reviews=reviews
    )


@songs.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)

@songs.route("/about")
def about():
    return render_template("about.html")
