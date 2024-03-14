import os
import sys
from threading import Thread

from dotenv import load_dotenv

from .discord_bot import DiscordBot
from .flask_app import FlaskApp

# load environment variables from .env file
load_dotenv()


class App:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        if not self.token:
            sys.exit(
                "DISCORD_TOKEN environment variable is required. Set it in the .env file."
            )

        self.status = os.getenv("DISCORD_STATUS", "online")
        self.custom_status = os.getenv("DISCORD_STATUS_MSG", "dicostapres")
        self.flask_app = FlaskApp()
        self.discord_bot = DiscordBot(self.token, self.status, self.custom_status)

    def run(self):
        """Runs the application."""
        Thread(target=self.flask_app.run).start()

        user_info = self.discord_bot.fetch_user_info()
        print(
            f"Logged in as {user_info['username']}#{user_info['discriminator']} ({user_info['id']})."
        )

        self.discord_bot.setup_websocket_connection()
        self.discord_bot.maintain_connection()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
