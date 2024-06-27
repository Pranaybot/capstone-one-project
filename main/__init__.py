# main/__init__.py
from flask import Flask
from main.models import User, OneWayTripPayment, RoundTripPayment, OneWayTripReview, RoundTripReview
from main.extensions.connect_db import connect_db, db
from dotenv import load_dotenv
from main.blueprint_collection import register_blueprints
import os

# Load environment variables from .env file
load_dotenv()


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Load all environment variables into main.config
    app.config.update(os.environ)

    register_blueprints(app)

    app.app_context().push()
    connect_db(app)

    with app.app_context():
        db.create_all()

    return app