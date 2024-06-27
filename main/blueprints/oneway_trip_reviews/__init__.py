from flask import Blueprint


oneway_trip_reviews_bp = Blueprint(
    "oneway_trip_reviews",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/oneway_trip_reviews/static'
)

from . import routes
