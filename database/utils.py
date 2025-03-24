from database.get_client import get_client
from database.schemas import MessageHistory
from datetime import datetime

async def is_session_active( user_id: int, current_time_stamp: datetime):
    client_db = await get_client()
    #get the last session from the database and it's current time
    session = await client_db.ai_bot.MessageHistory.find_one({"user_id": user_id}, sort=[("current_time", -1)])

    #if session doesn't exist return false
    if session is None:
        return False
    
    #check if 1 hour has passed i.e session has expired
    if (current_time_stamp - session["current_time"]).total_seconds() > 3600:
        return False
    else:
        return True
   

