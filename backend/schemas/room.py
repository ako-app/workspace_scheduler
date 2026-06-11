from datetime import datetime
#from fastapi import FastAPI
from pydantic import BaseModel,Field

class RoomRequest(BaseModel):
    #room_id: int 
    manager_id: int
    room_name: str = Field(max_length=12)
    capacity: int

class RoomResponse(BaseModel):
    room_id: int 
    manager_id: int
    room_name: str = Field(max_length=12)
    capacity: int
    

