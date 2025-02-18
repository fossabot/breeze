""" a flask application similar to Twitter just for fun!
"""
from breeze import exc
from breeze import utils
from breeze.auth import Auth
from breeze.blueprints import auth as auth_bp
from breeze.blueprints import index as index_bp
from breeze.blueprints import posts as posts_bp
from breeze.config import BreezeConfig
from breeze.models import Comment
from breeze.models import db
from breeze.models import Post
from breeze.models import Tag
from breeze.models import User

__version__ = "0.4.0-dev"


def create_app():
    """create a flask application with application Factory pattern
    `application Factory <https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/>`_

    :return:
        :class:`flask.Flask`: flask application
    """
    from flask import Flask, json
    from werkzeug.exceptions import HTTPException
    from sqlalchemy.exc import OperationalError

    app = Flask(__name__)
    app.config.from_object("breeze.Config")

    # register database
    try:
        with app.app_context():
            db.init_app(app)
            db.create_all()
    except OperationalError:
        pass

    # register app(s) from blueprints
    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(index_bp.bp)
    app.register_blueprint(posts_bp.bp)

    return app


class Config(BreezeConfig):
    """breeze configuration
    Inherit from :class:`breeze.BreezeConfig`

    """

    import logging
    import os
    from pathlib import Path

    from dotenv import find_dotenv, load_dotenv

    dotenv_path = find_dotenv()
    if not dotenv_path:
        logging.warning(".env not found")
        Path(".env").write_text(f"SECRET_KEY={utils.get_random_string(64)}")
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = True
