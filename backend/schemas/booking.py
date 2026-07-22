from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict

# 予約情報リクエストスキーマ
class BookingRequest(BaseModel):
    room_id: int = Field(
        ...,
        description="会議室ID",
        examples=[1],
    )
    start_at: datetime = Field(
        ...,
        description="開始時刻",
    ) 
    end_at: datetime = Field(
        ...,
        description="終了時刻"
    ) 
    reserved_num: int = Field(
        ...,
        gt=0,
        description="予約人数",
        examples=[5],
    )

# 予約情報レスポンススキーマ
class BookingResponse(BaseModel):
    id: int = Field(
        ...,
        description="予約ID",
        examples=[1]
    )
    room_id: int = Field(
        ...,
        description="会議室ID",
        examples=[1],
    )
    start_at: datetime = Field(
        ...,
        description="開始時刻",
    )
    end_at: datetime = Field(
        ...,
        description="終了時刻",
    )
    reserved_num: int = Field(
        ...,
        gt=0,
        description="予約人数",
        examples=[5]  
    )
    created_at: datetime = Field(
        ...,
        description="作成日時",
    )
    updated_at: datetime =Field(
        ...,
        description="更新日時",
    ) 

    model_config = ConfigDict(
        from_attributes= True
    )

