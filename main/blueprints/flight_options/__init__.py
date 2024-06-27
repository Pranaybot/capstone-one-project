from flask import Blueprint


flight_options_bp = Blueprint(
    "flight_options",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/flight_options/static'
)


from . import routes