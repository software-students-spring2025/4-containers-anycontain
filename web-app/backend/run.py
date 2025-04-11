"""Entry point to run the Flask backend app."""
import sys
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5114
    app.run(host="0.0.0.0", port=port, debug=True)
