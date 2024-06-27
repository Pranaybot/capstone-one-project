from main.extensions.bcrypt_and_database import db


def connect_db(app):

    db.app = app
    db.init_app(app)
