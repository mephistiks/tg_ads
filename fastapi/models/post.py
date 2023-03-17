from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    chanel_id: int = Field(...)
    post_id: str = Field(...)
    date: str = Field()
    time: str = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Calendar(BaseModel):
    channels_id: list = Field(...)
    post_id: str = Field(...)
    times: list = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class NewPostSchema(BaseModel):
    img: str = Field(...)
    post_name: str = Field(...)
    post_text: str = Field(...)
    buttons: list = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Channels(BaseModel):
    delete: list = Field(...)
    add: list = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
