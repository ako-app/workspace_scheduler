from datetime import datetime
#from fastapi import FastAPI
from pydantic import BaseModel,Field

class BookingRequest(BaseModel):
    #booking_id: int 
    user_id: int
    room_id: int
    start_at: datetime #開始時刻
    end_at: datetime #終了時刻
    reserved_num: int
    #created_at: datetime #作成日時
    #updated_at: datetime #更新日時

class BookingResponse(BaseModel):
    booking_id: int 
    user_id: int
    room_id: int
    start_at: datetime #開始時刻
    end_at: datetime #終了時刻
    reserved_num: int
    created_at: datetime #作成日時
    updated_at: datetime #更新日時

