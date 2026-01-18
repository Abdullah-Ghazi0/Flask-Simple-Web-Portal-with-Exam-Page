from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from ..models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET","POST"])
def reg():
    
    if request.method == "POST":
        uname = request.form.get("username")
        pword = request.form.get("password")

        hashed_pw = generate_password_hash(pword)

        if Users.query.filter_by(username=uname).first():
            flash("User already Exist!")
        else:
            user = Users(
                username = uname,
                password = hashed_pw
            )
            db.session.add(user)
            db.session.commit()
            flash("Registered Sccessfully!")
            return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    
    if request.method == "POST":
        log_uname = request.form.get("username")
        log_pword = request.form.get("password")

        user = Users.query.filter_by(username=log_uname).first()
        if user and check_password_hash(user.password, log_pword):
            session["user_id"] = user.id
            flash("Login Sccessful!")
            return redirect(url_for('auth.dash'))

        else:
            flash("Wrong Username or Password!")

    return render_template("login.html")

@auth_bp.route("/dashboard")
def dash():
    if "user_id" in session:
        usrid = session.get("user_id")
        user = Users.query.get(usrid)
        name = user.username
        if name == "admin":
            return render_template("admin.html", name=name)

        return render_template("dashboard.html", name=name)
    else:
        return "<h1>You need to login to access dashboard!"
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    flash("Logout Successful!")
    return redirect(url_for('home'))

@auth_bp.route("/settings", methods=["GET","POST"])
def sett():
    if "user_id" in session:
        user_id = session.get("user_id")

        if request.method == "POST":
            o_pass = request.form.get("old_pass")
            n_pass = request.form.get("new_pass")
            c_pass = request.form.get("conf_pass")

            user_info = Users.query.get(user_id)
            if not check_password_hash(user_info.password, o_pass):
                flash("Current Password is incorrect!")
                return redirect(url_for('auth.sett'))
            
            if n_pass != c_pass:
                flash("New Password does not match!")
                return redirect(url_for('auth.sett'))
            
            new_hashed_pw = generate_password_hash(n_pass)
            user_info.password = new_hashed_pw
            db.session.commit()
            flash("Password Changed Sccessfully!")
            return redirect(url_for('auth.dash'))
        
        return render_template("setting.html")
    else:
        return "<h1>You need to login to access settings!"

@auth_bp.route("/delete", methods = ["POST"])
def delete():
    user_id = session.get("user_id")
    user = Users.query.get(user_id)
    
    if user:
        session.pop("user_id")
        db.session.delete(user)
        db.session.commit()
        
        flash("Your account has been successfully deleted.")
        return redirect(url_for('home'))
    