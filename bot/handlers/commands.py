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
from database.utils import is_session_active
import uuid
import asyncio
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


#/news command is slow since it uses web search tool and then summarizes the news.()
# cache for stroring news data
# here i am creating a inmemory cache for storing news data
news_cache={
    "data":None,
    "last_updated":None
}
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
    Made by Aditya Bhatt
    Reach out to me on LinkedIn <https://www.linkedin.com/in/adityaabhatt/>
    Reach out to me on Instagram <https://www.instagram.com/your_data_scientist/>
    '''
    #push the user message , reply and time in the database
    client_db = await get_client()
    #these are static messages so we don't need to push them in the database
    try:
        logger.info(f"Sending welcome message to {user.first_name}")
        client_db.ai_bot.static_messages.insert_one({
            "message": welcome_message,
            "user_id": user.id,
            "user_name": user.first_name,
            "time": datetime.now(),
            "section": "start"
        })
        await update.message.reply_text(welcome_message)
     
    except Exception as e:
        await client_db.ai_bot.errors.insert_one({
            "error": str(e),
            "time": datetime.now(),
            "section": "start",
            "user_id": user.id,
            "user_name": user.first_name
        })
        logger.error(f"Error in inserting message into database: {str(e)}")

  

async def about_command(update, context):
    user = update.effective_user
    about_message = f"This bot is used to give free ai resources , latest ai updates and helps you to get started with ai and become master in ai."
    logger.info(f"Sending about message to {user.first_name}")
    #push the user message , reply and time in the database
    client_db = await get_client()
    try:
        client_db.ai_bot.static_messages.insert_one({
            "message": about_message,
            "user_id": user.id,
            "user_name": user.first_name,
            "time": datetime.now(),
            "section": "about"
        })
        await update.message.reply_text(about_message)
    except Exception as e:
        await client_db.ai_bot.errors.insert_one({
            "error": str(e),
            "time": datetime.now(),
            "section": "about",
            "user_id": user.id,
            "user_name": user.first_name
        })
        logger.error(f"Error in inserting message into database: {str(e)}")

   

# Create a cache at the module level (outside of any function)
# This cache will persist between function calls as long as the application is running
news_cache = {
    "data": None,  # The actual news content
    "timestamp": None  # When the data was cached
}

async def news_command(update, context):
    """
    Command handler for the /news command.
    Fetches and returns the latest AI news.
    Implements caching to reduce API calls and improve response time.
    """
    user = update.effective_user
    current_time = datetime.now()
    cache_expiry_seconds = 10800  # 3 hours in seconds (10800 seconds)
    
    # Check if we have valid cached data
    if news_cache["data"] and news_cache["timestamp"]:
        # Calculate how old the cache is
        time_difference = (current_time - news_cache["timestamp"]).total_seconds()
        
        # If cache is less than expiry time, use cached data
        if time_difference < cache_expiry_seconds:
            logger.info(f"Serving news from cache (age: {time_difference:.2f} seconds)")
            
            # Get database client
            client_db = await get_client()
            try:
                # Log this message in the database as usual
                client_db.ai_bot.static_messages.insert_one({
                    "message": news_cache["data"],
                    "user_id": user.id,
                    "user_name": user.first_name,
                    "time": current_time,
                    "section": "news",
                    "source": "cache"  # Added to track cache usage
                })
                # Send the cached response to the user
                await update.message.reply_text(news_cache["data"])
                return  # Exit function early since we've served from cache
            except Exception as e:
                # If there's an error with the database, log it but continue
                # This allows us to still serve the news even if DB logging fails
                logger.error(f"Error serving from cache: {str(e)}")
                # We'll fall through to the API call if we can't serve from cache
    
    # If we get here, either:
    # 1. Cache doesn't exist
    # 2. Cache is expired
    # 3. There was an error serving from cache
    logger.info("Cache miss or expired, fetching fresh news data")
    
    # Get today's date for the API call
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Make API calls to get fresh news data
    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type":"web_search_preview"}],
        input=f"Go to web and short summarize latest ai news on {today}"
    )
    
    response_summarizer = client.responses.create(
        model="gpt-4o-mini",
        input=f"Summarize the following news in short and concise manner and give links also in the end: {response.output_text}"
    )
    
    # Update the cache with new data
    news_cache["data"] = response_summarizer.output_text
    news_cache["timestamp"] = current_time
    logger.info("News cache updated with fresh data")
    
    # Get database client
    client_db = await get_client()
    try:
        # Store the message in the database
        client_db.ai_bot.static_messages.insert_one({
            "message": response_summarizer.output_text,
            "user_id": user.id,
            "user_name": user.first_name,
            "time": current_time,
            "section": "news",
            "source": "api"  # Added to track API usage
        })
        # Send the fresh response to the user
        await update.message.reply_text(response_summarizer.output_text)
    except Exception as e:
        # Log any database errors
        await client_db.ai_bot.errors.insert_one({
            "error": str(e),
            "time": current_time,
            "section": "news",
            "user_id": user.id,
            "user_name": user.first_name
        })
        logger.error(f"Error in inserting message into database: {str(e)}")
        
        # Still try to send the response even if DB logging fails
        await update.message.reply_text(response_summarizer.output_text)
    

async def get_help(update, context):
    user = update.effective_user
    help_message = f"This bot can help you to get started with ai and become master in ai. \n Use /start to get started. \n Use /news to get latest ai news. \n Use /about to know more about the bot \n Use /research to get latest research papers.\n Otherwise you can ask anything (if you need any resources or anything else) \n Made by Aditya Bhatt \n Reach out to me on LinkedIn <https://www.linkedin.com/in/adityaabhatt/> \n Reach out to me on Instagram <https://www.instagram.com/your_data_scientist/>"
    logger.info(f"Sending help message to {user.first_name}")
    #push the user message , reply and time in the database
    client_db = await get_client()
    try:
        client_db.ai_bot.static_messages.insert_one({
            "message": help_message,
            "user_id": user.id,
            "user_name": user.first_name,
            "time": datetime.now(),
            "section": "help"
        })
        await update.message.reply_text(help_message)

    except Exception as e:
        await client_db.ai_bot.errors.insert_one({
            "error": str(e),
            "time": datetime.now(),
            "section": "help",
            "user_id": user.id,
            "user_name": user.first_name
        })

        logger.error(f"Error in help command: {str(e)}")

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
            client_db.ai_bot.static_messages.insert_one({
                "message": response,
                "user_id": user.id,
                "user_name": user.first_name,
                "time": datetime.now(),
                "section": "research"
            })
            await update.message.reply_text(response)
        except Exception as e:
            await client_db.ai_bot.errors.insert_one({
                "error": str(e),
                "time": datetime.now(),
                "section": "research",
                "user_id": user.id,
                "user_name": user.first_name
            })
        
        
    except Exception as e:
        error_message = "Sorry, there was an error fetching research papers."
        logger.error(f"Error in research command: {str(e)}")
        await client_db.ai_bot.errors.insert_one({
            "error": str(e),
            "time": datetime.now(),
            "section": "research",
            "user_id": user.id,
            "user_name": user.first_name
        })

#function to run as background task to update cache
async def refresh_news_cache():
    """
    Background task to periodically refresh the news cache,
    so no user has to wait for a cache miss.
    """
    current_time = datetime.now()
    today = current_time.strftime("%Y-%m-%d")
    
    logger.info("Background task: Refreshing news cache")
    
    try:
        # Make API calls to get fresh news data
        response = client.responses.create(
            model="gpt-4o-mini",
            tools=[{"type":"web_search_preview"}],
            input=f"Go to web and short summarize latest ai news on {today}"
        )
        
        response_summarizer = client.responses.create(
            model="gpt-4o-mini",
            input=f"Summarize the following news in short and concise manner and give links also in the end: {response.output_text}"
        )
        
        # Update the cache with new data
        news_cache["data"] = response_summarizer.output_text
        news_cache["timestamp"] = current_time
        logger.info("News cache updated by background task")
    except Exception as e:
        logger.error(f"Background task error refreshing news cache: {str(e)}")

async def schedule_news_cache_refresh():
    """
    Schedule the periodic refresh of the news cache.
    This runs in the background as long as the bot is running.
    """
    while True:
        try:
            # Refresh the cache
            await refresh_news_cache()
            
            # Wait for 3 hours (10800 seconds) before refreshing again
            await asyncio.sleep(10800)
        except Exception as e:
            logger.error(f"Error in cache refresh schedule: {str(e)}")
            # If there's an error, wait a bit and try again
            await asyncio.sleep(300)  # Wait 5 minutes before retrying