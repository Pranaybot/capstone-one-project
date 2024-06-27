from flask import Blueprint


travel_options_bp = Blueprint(
    "travel_options",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/travel_options/static'
)

from . import routes
