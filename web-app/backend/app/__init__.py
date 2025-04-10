"""Module for creating the Flask application."""

import sys
import os
from flask import Flask
from flask_cors import CORS
from app.routes import routes


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    CORS(app, origins=["http://localhost:3000"])
    app.register_blueprint(routes)
    return app
