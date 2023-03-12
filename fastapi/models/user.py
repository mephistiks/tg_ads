from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from fastapi import PyObjectId


class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    perms = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Иван Иванов",
                "email": "test@test.com",
                "password": "qwe123"
            }
        }