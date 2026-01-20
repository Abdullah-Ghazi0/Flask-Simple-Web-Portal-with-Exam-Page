from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from .word_adding import find_known_char
from ..models import db, Words

game_bp = Blueprint("game", __name__, url_prefix="/game")

@game_bp.route("/")
def game_play():
    return render_template("game.html")

@game_bp.route("/add-words", methods=["POST", "GET"])
def adding():
    if "user_id" in session and session["user_id"] == 1:
        if request.method == "POST":
            word = request.form.get("word")
            word = word.upper()

            word_len = len(word)

            new_word = Words(
                word = word,
                k_char = find_known_char(word_len)
            )
            db.session.add(new_word)
            db.session.commit()
            flash("Word Added Sccessfully!")
            return redirect(url_for("game.adding"))

        return render_template("adding_words.html")
    else:
        return "<h1>You are not allowed access this page!"