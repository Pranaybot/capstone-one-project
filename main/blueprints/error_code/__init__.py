from flask import Blueprint


error_code_bp = Blueprint(
    "error_code",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/error_code/static'
)

from . import routes