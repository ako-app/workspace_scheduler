import datetime
#from fastapi import FastAPI
from pydantic import BaseModel,Field

class UserRequest(BaseModel):
    #user_id: int
    username: str = Field(max_length=12)

class UserResponse(BaseModel):
    user_id: int
    username: str = Field(max_length=12)
