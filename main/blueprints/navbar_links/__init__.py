from flask import Blueprint


navbar_links_bp = Blueprint(
    "navbar_links",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/navbar_links/static'
)

from . import routes
