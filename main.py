import os
from fastapi import FastAPI
from telegram.ext import ApplicationBuilder
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

# Get bot token with validation
bot_token = os.getenv("TELEGRAM_API_KEY")
if not bot_token:
    logger.error("No TELEGRAM_API_KEY found in environment variables!")
    raise ValueError("TELEGRAM_API_KEY is missing. Please check your .env file.")
else:
    # Only show first few characters for security
    logger.info(f"Bot token loaded: {bot_token[:5]}...")

# Create FastAPI app
app = FastAPI(title="AI Gyan Bot")
logger.info("FastAPI app created")

# Initialize Telegram bot
tg_app = ApplicationBuilder().token(bot_token).build()
logger.info("Telegram bot application initialized")

# Simple handler for /start command
async def start_command(update, context):
    user = update.effective_user
    welcome_message = f"👋 Hi {user.first_name}! Welcome to AI Gyan Bot!"
    logger.info(f"Sending welcome message to {user.first_name}")
    await update.message.reply_text(welcome_message)

# Register the handler
from telegram.ext import CommandHandler
tg_app.add_handler(CommandHandler("start", start_command))
logger.info("Start command handler registered")

@app.get("/")
async def root():
    return {"message": "AI Gyan Bot is running"}

# Start the bot on startup
@app.on_event("startup")
async def startup():
    logger.info("STARTUP EVENT TRIGGERED - Starting bot...")
    await tg_app.initialize()
    logger.info("Bot initialized")
    await tg_app.start()
    logger.info("Bot started")
    await tg_app.updater.start_polling()
    logger.info("Bot polling started successfully!")

# Stop the bot when shutting down
@app.on_event("shutdown")
async def shutdown():
    logger.info("SHUTDOWN EVENT TRIGGERED - Stopping bot...")
    await tg_app.updater.stop()
    await tg_app.stop()
    await tg_app.shutdown()
    logger.info("Bot shut down successfully")

# Run the app directly if this file is executed
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)