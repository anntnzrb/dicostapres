import os
from dotenv import load_dotenv
from dicostapres.discord_client import DiscordClient
from dicostapres.web_server import WebServer

def main():
    load_dotenv()

    discord_client = DiscordClient()
    web_server = WebServer(os.getenv("DICOSTAPRES_PORT"))

    web_server.start()
    discord_client.run()

if __name__ == "__main__":
    main()