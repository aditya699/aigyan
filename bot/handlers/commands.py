'''
This file contains the command handlers for the bot.
(command handlers are used to handle the commands that are sent to the bot)
'''
from config import logger
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()

async def start_command(update, context):
    user = update.effective_user
    welcome_message = f'''
    Hi {user.first_name}! Welcome to AI Gyan Bot!
    This bot is used to give free ai resources , latest ai updates and helps you to get started with ai and become master in ai.
    Use /about to know more about the bot.
    Use /news to get latest ai news.
    '''

    logger.info(f"Sending welcome message to {user.first_name}")
    await update.message.reply_text(welcome_message)

async def about_command(update, context):
    user = update.effective_user
    about_message = f"This bot is used to give free ai resources , latest ai updates and helps you to get started with ai and become master in ai."
    logger.info(f"Sending about message to {user.first_name}")
    await update.message.reply_text(about_message)

async def news_command(update, context):

    today=datetime.now().strftime("%Y-%m-%d")

    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type":"web_search_preview"}],
        input=f"Go to web and search latest ai news on {today}"
      
    )
    await update.message.reply_text(response.output_text)

async def get_help(update, context):
    user = update.effective_user
    help_message = f"This bot can help you to get started with ai and become master in ai. \n Use /start to get started. \n Use /news to get latest ai news. \n Use /about to know more about the"
    logger.info(f"Sending help message to {user.first_name}")
    await update.message.reply_text(help_message)


# Add more command handlers here