from flask import Blueprint


payments_bp = Blueprint(
    "payments",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/payments/static'
)

from . import routes
