from pydantic import BaseModel, Field, ConfigDict

# 管理者ユーザー情報リクエストスキーマ
class UserRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=12,
        description="管理者ユーザー名",
        examples=["tanaka_taro"]              
    )
# 管理者ユーザー情報レスポンス用スキーマ
class UserResponse(BaseModel):
    id: int = Field(
        ...,
        description="管理者ユーザーID",
        examples=[1]
    )
    username: str = Field(
        ...,
        max_length=12,
        description="管理者ユーザー名",
        examples=["tanaka_taro"]
    ) 
    model_config = ConfigDict(
        from_attributes=True
    )
