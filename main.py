import uvicorn
from config import logger
from bot.app import create_bot_application
from api.app import create_app
from api.routes import router
from bot.handlers.commands import schedule_news_cache_refresh
import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
# Create applications
app = create_app()
tg_app = create_bot_application()

# Register routes
app.include_router(router)

# Startup and shutdown events
@app.on_event("startup")
async def startup():
    logger.info("STARTUP EVENT TRIGGERED - Starting bot...")
    await tg_app.initialize() #This is used to initialize the bot
    await tg_app.start() #This is used to start the bot
    await tg_app.updater.start_polling() #This is used to start the polling(which is used to check for new messages(continuous checking))
    logger.info("Bot polling started successfully!")
    # Schedule the news cache refresh
    asyncio.create_task(schedule_news_cache_refresh())
    logger.info("News cache refresh scheduled successfully!")

@app.on_event("shutdown")
async def shutdown():
    logger.info("SHUTDOWN EVENT TRIGGERED - Stopping bot...")
    await tg_app.updater.stop()
    await tg_app.stop()
    await tg_app.shutdown()
    logger.info("Bot shut down successfully")

if __name__ == "__main__":
    logger.info("Starting uvicorn server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)