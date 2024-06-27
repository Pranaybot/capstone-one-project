from flask import Blueprint


round_trip_reviews_bp = Blueprint(
    "round_trip_reviews",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/round_trip_reviews/static'
)

from . import routes