import json
import os
import time
import requests
import websocket
from dotenv import load_dotenv
import logging

API_BASE_URL = "https://canary.discordapp.com/api/v9"
WEBSOCKET_URL = "wss://gateway.discord.gg/?v=9&encoding=json"

class DiscordClient:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DISCORD_TOKEN")
        self.status = os.getenv("DISCORD_STATUS", "online")
        self.custom_status = os.getenv("DISCORD_STATUS_MSG", "debug")
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}

        self._validate_token()
        self.user_info = self._get_user_info()
        self.username = self.user_info["username"]
        self.discriminator = self.user_info["discriminator"]
        self.user_id = self.user_info["id"]

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_token(self):
        try:
            validate = requests.get(f"{API_BASE_URL}/users/@me", headers=self.headers)
            validate.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Token validation failed: {e}")

    def _get_user_info(self):
        validate = requests.get(f"{API_BASE_URL}/users/@me", headers=self.headers)
        return validate.json()

    def _connect_to_websocket(self):
        ws = websocket.WebSocket()
        ws.connect(WEBSOCKET_URL)
        return ws

    def _send_authentication(self, ws):
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

    def _send_custom_status(self, ws):
        custom_status = {
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
        ws.send(json.dumps(custom_status))

    def _send_heartbeat(self, ws):
        heartbeat_interval = json.loads(ws.recv())["d"]["heartbeat_interval"]
        time.sleep(heartbeat_interval / 1000)

    def _maintain_online_status(self):
        ws = self._connect_to_websocket()
        self._send_authentication(ws)
        self._send_custom_status(ws)
        ws.send(json.dumps({"op": 1, "d": "None"}))
        self._send_heartbeat(ws)

    def run(self):
        self.logger.info(f"Logged in as {self.username}#{self.discriminator} ({self.user_id}).")
        while True:
            try:
                self._maintain_online_status()
            except Exception as e:
                self.logger.error(f"Error in maintaining online status: {e}")
            time.sleep(30)