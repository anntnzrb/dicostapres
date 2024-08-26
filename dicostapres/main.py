import json
import os
import time
from threading import Thread

import requests
import websocket
from dotenv import load_dotenv
from flask import Flask
import logging

API_BASE_URL = "https://canary.discordapp.com/api/v9"
WEBSOCKET_URL = "wss://gateway.discord.gg/?v=9&encoding=json"

class DiscordApp:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DISCORD_TOKEN")
        self.status = os.getenv("DISCORD_STATUS", "online")
        self.custom_status = os.getenv("DISCORD_STATUS_MSG", "dicostapres")
        self.port = int(os.getenv("DICOSTAPRES_PORT", 6111))
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}

        self.validate_token()
        self.userinfo = self.get_user_info()
        self.username = self.userinfo["username"]
        self.discriminator = self.userinfo["discriminator"]
        self.userid = self.userinfo["id"]

        self.app = Flask("")
        self.server = Thread(target=self.run_server)

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_token(self):
        try:
            validate = requests.get(f"{API_BASE_URL}/users/@me", headers=self.headers)
            validate.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Token validation failed: {e}")

    def get_user_info(self):
        validate = requests.get(f"{API_BASE_URL}/users/@me", headers=self.headers)
        return validate.json()

    def run_server(self):
        @self.app.route("/")
        def main():
            return '<meta http-equiv="refresh" content="0; URL=https://github.com/anntnzrb/dicostapres"/>'

        self.app.run(host="0.0.0.0", port=self.port)

    def connect_websocket(self):
        ws = websocket.WebSocket()
        ws.connect(WEBSOCKET_URL)
        return ws

    def send_auth(self, ws):
        auth = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "Windows 10",
                    "$browser": "Google Chrome",
                    "$device": "Windows",
                },
                "presence": {"status": self.status, "afk": False},
            },
            "s": None,
            "t": None,
        }
        ws.send(json.dumps(auth))

    def send_custom_status(self, ws):
        cstatus = {
            "op": 3,
            "d": {
                "since": 0,
                "activities": [
                    {
                        "type": 4,
                        "state": self.custom_status,
                        "name": "Custom Status",
                        "id": "custom",
                    }
                ],
                "status": self.status,
                "afk": False,
            },
        }
        ws.send(json.dumps(cstatus))

    def heartbeat(self, ws):
        heartbeat_interval = json.loads(ws.recv())["d"]["heartbeat_interval"]
        time.sleep(heartbeat_interval / 1000)

    def onliner(self):
        ws = self.connect_websocket()
        self.send_auth(ws)
        self.send_custom_status(ws)
        ws.send(json.dumps({"op": 1, "d": "None"}))
        self.heartbeat(ws)

    def run_onliner(self):
        self.logger.info(f"Logged in as {self.username}#{self.discriminator} ({self.userid}).")
        while True:
            try:
                self.onliner()
            except Exception as e:
                self.logger.error(f"Error in onliner: {e}")
            time.sleep(30)

    def run(self):
        self.server.start()
        self.run_onliner()


def main():
    app = DiscordApp()
    app.run()


if __name__ == "__main__":
    main()