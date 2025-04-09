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
    CORS(app)
    app.register_blueprint(routes)
    return app
