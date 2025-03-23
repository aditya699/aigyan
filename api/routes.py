'''
This file contains the routes for the bot.
'''

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "AI Gyan Bot is running"}

# Add more routes here