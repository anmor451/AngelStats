from dotenv import load_dotenv
import os


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_API_TOKEN")
RIOT_TOKEN = os.getenv("RIOT_TOKEN")