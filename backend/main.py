from fastapi import FastAPI
from backend.schemas import (
    UserRequest,  
    UserResponse, 
    RoomRequest,  
    RoomResponse, 
    BookingRequest, 
    BookingResponse
)
#from backend.schemas.booking import BookingRequest
#from backend.schemas.room import RoomRequest
#from backend.schemas.user import UserRequest

app = FastAPI()

@app.get("/")#トップページ 非同期をつける
async def index():
    return {"message": "ここはトップページ"}

@app.post("/users")
async def users(user: UserRequest): #リクエストボディUserをuserで受け取る
    return {"user": user}
@app.post("/rooms")
async def users(room: RoomRequest): #リクエストボディUserをuserで受け取る
    return {"room": room}


@app.post("/bookings")
async def users(booking: BookingRequest): #リクエストボディUserをuserで受け取る
    return {"booking": booking}

