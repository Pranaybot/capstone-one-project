from flask import Blueprint


index_bp = Blueprint(
    "index",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/index/static'
)

from . import routes
