from flask import render_template, \
    redirect, url_for, flash, session, g, current_app
from . import navbar_links_bp


@navbar_links_bp.route("/flights")
def flights():
    return render_template("flights.html")


@navbar_links_bp.route("/payments")
def payments():
    if g.user:
        return render_template("payments.html", user=session[current_app.config['CURR_USER_KEY']])
    else:
        flash("You have to log in", 'warning')
        return redirect("/")


@navbar_links_bp.route("/reviews")
def reviews():
    if g.user:
        return render_template("reviews.html", user=session[current_app.config['CURR_USER_KEY']])
    else:
        flash("You have to log in", 'warning')
        return redirect("/")
