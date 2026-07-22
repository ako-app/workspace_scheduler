from pydantic import BaseModel, Field, ConfigDict

# 会議室情報リクエストスキーマ
class RoomRequest(BaseModel):
    room_name: str = Field(
        ...,
        max_length=12,
        description="会議室名",
        examples=["会議室A"]
    )
    capacity: int = Field(
        ...,
        gt=0,
        description="収容人数",
        examples=[10], 
    )
# 会議室情報レスポンススキーマ
class RoomResponse(BaseModel):
    id: int = Field(
        ...,
        description="会議室ID",
        examples=[1],
    )
    room_name: str = Field(
        ...,
        max_length=12,
        description="会議室名",
        examples=["会議室A"]
    )
    capacity: int = Field(
        ...,
        gt=0,
        description="収容人数",
        examples=[10]
    )
    model_config = ConfigDict(
        from_attributes=True
    )


    

