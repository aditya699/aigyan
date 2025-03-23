'''
It centralizes the configuration for the bot. 
It also provides a logger for the bot.
'''
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Bot token
BOT_TOKEN = os.getenv("TELEGRAM_API_KEY")
if not BOT_TOKEN:
    logger.error("No TELEGRAM_API_KEY found in environment variables!")
    raise ValueError("TELEGRAM_API_KEY is missing. Please check your .env file.")