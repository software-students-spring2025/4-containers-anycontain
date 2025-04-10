"""Entry point to run the Flask backend app."""
from flask import Flask
from flask_cors import CORS
import sys



def create_app():
    app = Flask(__name__)
    CORS(app)  # <- This is important if frontend and backend aren't served from same origin
    ...
    return app

app = create_app()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5114
    app.run(host="0.0.0.0", port=port, debug=True)
