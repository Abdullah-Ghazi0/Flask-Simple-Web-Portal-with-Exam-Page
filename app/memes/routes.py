from flask import Blueprint, render_template, session
from .meme_api import memer

meme_bp = Blueprint("meme", __name__, url_prefix="/memes")

@meme_bp.route("/")
def show_meme():
    if "user_id" not in session:
        return "<h1>You don't have access to this page!"
    
    meme_post = memer()
    return render_template("meme.html", meme=meme_post)