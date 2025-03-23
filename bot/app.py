from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, logger
from bot.handlers.commands import start_command, about_command, news_command, get_help
from bot.handlers.messages import text_message_handler

def create_bot_application():
    # Initialize Telegram bot
    tg_app = ApplicationBuilder().token(BOT_TOKEN).build()
    logger.info("Telegram bot application initialized")
    
    # Register command handlers
    tg_app.add_handler(CommandHandler("start", start_command))
    tg_app.add_handler(CommandHandler("about", about_command))
    tg_app.add_handler(CommandHandler("news", news_command))
    tg_app.add_handler(CommandHandler("help", get_help))
    logger.info("Command handlers registered")
    
    # Register message handlers
    # This will handle all the messages that are not commands
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    logger.info("Message handlers registered")
    
    return tg_app