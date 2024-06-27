from flask import render_template, url_for
from . import travel_options_bp


@travel_options_bp.route("/airport_rules")
def airport_rules():
    return render_template("airport_rules.html")


@travel_options_bp.route("/boarding_pass")
def boarding_pass():
    return render_template("boarding_pass.html")


@travel_options_bp.route("/bags")
def bags():
    return render_template("bags.html")


@travel_options_bp.route("/special_assistance")
def special_assistance():
    return render_template("special_assistance.html")
