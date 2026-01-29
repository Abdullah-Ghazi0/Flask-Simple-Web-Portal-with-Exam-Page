from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from .sending import send
from ..models import Users, Messages

msg_bp = Blueprint("message", __name__, url_prefix="/message")

@msg_bp.route("/send", methods=["POST", "GET"])
def msg_send():
    if "user_id" not in session:
        flash("You need to login first!")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        rcvr = request.form.get("reciever")

        if Users.query.filter_by(username=rcvr).first():

            msg = request.form.get("msg_content")
            send(rcvr, msg)
            flash("Message Sent!")
        else:
            flash("Please Send message to a valid user!")
            return redirect(url_for("message.msg_send"))

    return render_template("message.html")

@msg_bp.route("/inbox")
def inbox():
    if "user_id" not in session:
        flash("You need to login first!")
        return redirect(url_for("auth.login"))
    my_id = session["user_id"]
    if Messages.query.filter_by(r_id=my_id).all():
        all_msg = Messages.query.filter_by(r_id=my_id).order_by(Messages.time.desc()).all()
        
        return render_template("inbox.html", all_msg=all_msg)
    else:
        flash("No Messages yet!")
        return render_template("inbox.html")