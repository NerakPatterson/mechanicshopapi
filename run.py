import os
from app import create_app

# Create the Flask app using the factory
app = create_app()

app.config["TESTING"] = True

if __name__ == "__main__":
    # Toggle debug mode based on FLASK_ENV
    debug = os.getenv("FLASK_ENV") == "development"

    # Allow host/port to be set via environment variables
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))

    app.run(host=host, port=port, debug=debug)
