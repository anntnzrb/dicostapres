import json
import os
import time
from threading import Thread

import requests
import websocket
from dotenv import load_dotenv
from flask import Flask


class DiscordApp:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DISCORD_TOKEN")
        self.status = os.getenv("DISCORD_STATUS", "online")
        self.custom_status = os.getenv("DISCORD_STATUS_MSG", "dicostapres")
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}

        if not self.token:
            raise ValueError("Please add a token inside .env file.")

        validate = requests.get(
            "https://canary.discordapp.com/api/v9/users/@me", headers=self.headers
        )
        if validate.status_code != 200:
            raise ValueError("Your token might be invalid. Please check it again.")

        userinfo = validate.json()
        self.username = userinfo["username"]
        self.discriminator = userinfo["discriminator"]
        self.userid = userinfo["id"]

        self.app = Flask("")
        self.server = Thread(target=self.run_server)

    def run_server(self):
        @self.app.route("/")
        def main():
            return '<meta http-equiv="refresh" content="0; URL=https://github.com/anntnzrb/dicostapres"/>'

        self.app.run(host="0.0.0.0", port=8089)

    def onliner(self):
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        start = json.loads(ws.recv())
        heartbeat = start["d"]["heartbeat_interval"]
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
        ws.send(json.dumps({"op": 1, "d": "None"}))
        time.sleep(heartbeat / 1000)

    def run_onliner(self):
        print(f"Logged in as {self.username}#{self.discriminator} ({self.userid}).")
        while True:
            self.onliner()
            time.sleep(30)

    def run(self):
        self.server.start()
        self.run_onliner()


def main():
    app = DiscordApp()
    app.run()


if __name__ == "__main__":
    main()
