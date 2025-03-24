from pydantic import BaseModel
from datetime import datetime
from typing import List

class MessageHistory(BaseModel):
    session_id: str
    messages:dict
    current_time: datetime
    section: str
    user_id: int
    user_name: str

