'''
This file contains the command handlers for the bot.
(command handlers are used to handle the commands that are sent to the bot)
'''
from config import logger
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET
from database.get_client import get_client
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
    Use /research to get latest research papers.
    Otherwise you can ask anything (if you need any resources or anything else)
    '''
    #push the user message , reply and time in the database
    client_db = await get_client()
    try:
        await client_db.ai_bot.messages.insert_one({
            "user_message": update.message.text,
            "reply": welcome_message,
            "time": datetime.now(),
            "section": "start",
            "user_id": user.id,
            "user_name": user.first_name
        })
    except Exception as e:
        logger.error(f"Error in inserting message into database: {str(e)}")

    logger.info(f"Sending welcome message to {user.first_name}")
    await update.message.reply_text(welcome_message)

async def about_command(update, context):
    user = update.effective_user
    about_message = f"This bot is used to give free ai resources , latest ai updates and helps you to get started with ai and become master in ai."
    logger.info(f"Sending about message to {user.first_name}")
    #push the user message , reply and time in the database
    client_db = await get_client()
    try:
        await client_db.ai_bot.messages.insert_one({
            "user_message": update.message.text,
            "reply": about_message,
            "time": datetime.now(),
            "section": "about",
            "user_id": user.id,
            "user_name": user.first_name
        })
    except Exception as e:
        logger.error(f"Error in inserting message into database: {str(e)}")

    await update.message.reply_text(about_message)

async def news_command(update, context):
    user = update.effective_user
    today=datetime.now().strftime("%Y-%m-%d")

    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type":"web_search_preview"}],
        input=f"Go to web and short summarize latest ai news on {today}"
      
    )

    response_summarizer=client.responses.create(
        model="gpt-4o-mini",
        input=f"Summarize the following news in short and concise manner and give links also in the end: {response.output_text}"
    )
    #push the user message , reply and time in the database
    client_db = await get_client()
    try:
        await client_db.ai_bot.messages.insert_one({
            "user_message": update.message.text,
            "reply": response_summarizer.output_text,
            "time": datetime.now(),
            "section": "news",
            "user_id": user.id,
            "user_name": user.first_name
        })
    except Exception as e:
        logger.error(f"Error in inserting message into database: {str(e)}")

    await update.message.reply_text(response_summarizer.output_text)

async def get_help(update, context):
    user = update.effective_user
    help_message = f"This bot can help you to get started with ai and become master in ai. \n Use /start to get started. \n Use /news to get latest ai news. \n Use /about to know more about the bot \n Use /research to get latest research papers.Otherwise you can ask anything (if you need any resources or anything else)"
    logger.info(f"Sending help message to {user.first_name}")
    #push the user message , reply and time in the database
    client_db = await get_client()
    try:
        await client_db.ai_bot.messages.insert_one({
            "user_message": update.message.text,
            "reply": help_message,
            "time": datetime.now(),
            "section": "help",
            "user_id": user.id,
            "user_name": user.first_name
        })
    except Exception as e:
        logger.error(f"Error in inserting message into database: {str(e)}")

    await update.message.reply_text(help_message)

async def research_command(update, context):
    user = update.effective_user
    try:
        url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=lastUpdatedDate&sortOrder=descending&max_results=5'
        data = urllib.request.urlopen(url)
        xml_data = data.read().decode('utf-8')
        
        # Parse XML
        root = ET.fromstring(xml_data)
        
        # Format response
        response = "Latest AI Research Papers:\n\n"
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            link = entry.find('{http://www.w3.org/2005/Atom}id').text
            response += f"📄 {title}\n🔗 {link}\n\n"
            
        logger.info("Fetched research papers successfully")
        #push the user message , reply and time in the database
        client_db = await get_client()
        try:
            await client_db.ai_bot.messages.insert_one({
                "user_message": update.message.text,
                "reply": response,
                "time": datetime.now(),
                "section": "research",
                "user_id": user.id,
                "user_name": user.first_name
            })
        except Exception as e:
            logger.error(f"Error in inserting message into database: {str(e)}")

        await update.message.reply_text(response)
        
    except Exception as e:
        error_message = "Sorry, there was an error fetching research papers."
        logger.error(f"Error in research command: {str(e)}")
        await update.message.reply_text(error_message)

# Add more command handlers here