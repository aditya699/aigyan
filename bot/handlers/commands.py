'''
This file contains the command handlers for the bot.
(command handlers are used to handle the commands that are sent to the bot)
'''
from config import logger


async def start_command(update, context):
    user = update.effective_user
    welcome_message = f'''
    Hi {user.first_name}! Welcome to AI Gyan Bot!
    This bot is used to give free ai resources , latest ai updates and helps you to get started with ai and become master in ai.
    Use /about to know more about the bot.
    '''

    logger.info(f"Sending welcome message to {user.first_name}")
    await update.message.reply_text(welcome_message)

async def about_command(update, context):
    user = update.effective_user
    about_message = f"This bot is used to give free ai resources , latest ai updates and helps you to get started with ai and become master in ai."
    logger.info(f"Sending about message to {user.first_name}")
    await update.message.reply_text(about_message)


# Add more command handlers here