from flask import render_template, redirect, url_for, \
    flash, session, g, current_app
from main.forms import SignUpForm, LoginForm
from main.models import User
from main.extensions.bcrypt_and_database import db
from sqlalchemy.exc import IntegrityError
from . import user_bp


@user_bp.before_app_request
def add_user_to_g():

    if current_app.config['CURR_USER_KEY'] in session:
        g.user = User.query.get(session[current_app.config['CURR_USER_KEY']])
    else:
        g.user = None


@user_bp.after_app_request
def add_header(req):

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


def do_login(user):

    session[current_app.config['CURR_USER_KEY']] = user.id


def do_logout():

    session_keys = [current_app.config['CURR_USER_KEY'], "ONEWAY_TRIP_INFO",
                    "ROUND_TRIP_DEPARTURE_INFO", "ROUND_TRIP_ARRIVAL_INFO"]
    for key in session_keys:
        if key in session:
            del session[key]


@user_bp.route("/login_signup")
def login_signup():
    return render_template("login_signup.html")


@user_bp.route('/signup', methods=["GET", "POST"])
def signup():

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                name=form.name.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template("signup.html", form=form)

        do_login(user)
        flash("Account created successfully", "success")
        return redirect("/")

    else:
        return render_template("signup.html", form=form)


@user_bp.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template("login.html", form=form)


@user_bp.route('/logout')
def logout():

    flash("You logged out successfully", "success")
    do_logout()
    return redirect("/")
