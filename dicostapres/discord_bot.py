import json
import time

import requests
import websocket


class DiscordBot:
    def __init__(self, token, status="online", custom_status=""):
        self.token = token
        self.status = status
        self.custom_status = custom_status
        self.ws = websocket.create_connection(
            "wss://gateway.discord.gg/?v=9&encoding=json"
        )

    def _authenticate(self):
        """Sends authentication data to Discord via WebSocket."""
        auth_payload = self._get_auth_payload()
        self.ws.send(json.dumps(auth_payload))
        if self.custom_status:
            self.ws.send(json.dumps(self._get_custom_status_payload()))

    def _get_auth_payload(self):
        """Constructs the authentication payload."""
        return {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "linux",
                    "$browser": "my_client",
                    "$device": "my_device",
                },
                "presence": {"status": self.status, "afk": False},
            },
        }

    def _get_custom_status_payload(self):
        """Constructs the custom status payload."""
        return {
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

    def fetch_user_info(self):
        """Fetches user information from Discord API."""
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        response.raise_for_status()
        return response.json()

    def setup_websocket_connection(self):
        """Establishes a websocket connection to the Discord gateway and maintains it."""
        self._authenticate()

    def maintain_connection(self):
        """Keeps the websocket connection alive."""
        if not self.ws:
            print("WebSocket connection not established.")
            return
        try:
            while True:
                heartbeat_interval = json.loads(self.ws.recv())["d"][
                    "heartbeat_interval"
                ]
                while True:
                    self.ws.send(json.dumps({"op": 1, "d": None}))
                    time.sleep(heartbeat_interval / 1000)
        finally:
            self.ws.close()
