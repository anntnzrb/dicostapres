from flask import Flask


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)

    def run(self):
        """Starts the Flask application."""
        self.app.run(host="0.0.0.0", port=5000)
