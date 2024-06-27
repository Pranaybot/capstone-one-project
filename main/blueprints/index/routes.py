from flask import render_template, url_for
from . import index_bp


@index_bp.route("/")
def root():
    return render_template("index.html")