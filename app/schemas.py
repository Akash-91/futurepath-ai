from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = {"from_attributes": True}
