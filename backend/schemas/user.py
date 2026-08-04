from pydantic import BaseModel, ConfigDict, Field


# 管理者ユーザー情報リクエストスキーマ
class UserRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=2,
        max_length=12,
        description="管理者ユーザー名",
        examples=["tanaka_taro"],
    )
    password: str = Field(
        ...,
        min_length=8,
        description="パスワード",
        examples=["password123"],
    )


# 管理者ユーザー情報更新スキーマ
class UserUpdate(BaseModel):
    username: str = Field(
        ...,
        min_length=2,
        max_length=12,
        description="ユーザー名",
        examples=["tanaka_taro"],
    )


# 管理者ユーザー情報レスポンス用スキーマ
class UserResponse(BaseModel):
    id: int = Field(
        ...,
        description="ユーザーID",
        examples=[1],
    )
    username: str = Field(
        ...,
        max_length=12,
        description="ユーザー名",
        examples=["tanaka_taro"],
    )
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="JWTアクセストークン",
    )
    token_type: str = Field(
        ...,
        examples=["bearer"],
    )
