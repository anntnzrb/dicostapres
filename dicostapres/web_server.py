from flask import Flask
from threading import Thread
import logging

HOME_URL = "https://github.com/anntnzrb/dicostapres"

class WebServer:
    def __init__(self, port):
        self.port = port
        self.app = Flask("")
        self.server = Thread(target=self._run_server)
        
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    def _run_server(self):
        @self.app.route("/")
        def main():
            return f'<meta http-equiv="refresh" content="0; URL={HOME_URL}"/>'

        self.app.run(host="0.0.0.0", port=self.port, debug=False)

    def start(self):
        self.server.start()