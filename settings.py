from dotenv import load_dotenv
import os


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_API_TOKEN")
RIOT_TOKEN = os.getenv("RIOT_TOKEN")

CHANNEL_ID = 1137827436332073121
STATS_CHANNEL_ID = 1137828642202849300
BOT_COMMAND_CHANNEL_ID = 1136092594884067498