'''     
This file contains the initialization of the fastapi app.
'''
from fastapi import FastAPI
from config import logger

def create_app():
    app = FastAPI(title="AI Gyan Bot", 
                  description="Telegram bot API for AI information",
                  version="0.1.0")
    logger.info("FastAPI app created")
    return app