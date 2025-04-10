"""Entry point to run the Flask backend app."""

import sys
from app import create_app


app = create_app()

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5114
=======
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5111
>>>>>>> f34c38d5f456a23b9b1d1448e89f02a1b3185457
    app.run(host="0.0.0.0", port=port, debug=True)
