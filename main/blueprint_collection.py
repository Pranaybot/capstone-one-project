from flask import Flask

# Import all blueprints
from main.blueprints.user import user_bp
from main.blueprints.travel_options import travel_options_bp
from main.blueprints.round_trip_reviews import round_trip_reviews_bp
from main.blueprints.payments import payments_bp
from main.blueprints.oneway_trip_reviews import oneway_trip_reviews_bp
from main.blueprints.navbar_links import navbar_links_bp
from main.blueprints.index import index_bp
from main.blueprints.footer_links import footer_links_bp
from main.blueprints.flight_options import flight_options_bp
from main.blueprints.error_code import error_code_bp

# List of blueprints to be registered
blueprints = [
    user_bp,
    travel_options_bp,
    round_trip_reviews_bp,
    payments_bp,
    oneway_trip_reviews_bp,
    navbar_links_bp,
    index_bp,
    footer_links_bp,
    flight_options_bp,
    error_code_bp
]


def register_blueprints(app: Flask):
    for bp in blueprints:
        app.register_blueprint(bp)