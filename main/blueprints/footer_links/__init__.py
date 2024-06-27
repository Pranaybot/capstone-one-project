from flask import Blueprint


footer_links_bp = Blueprint(
    "footer_links",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/footer_links/static'
)

from . import routes
