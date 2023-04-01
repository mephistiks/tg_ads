from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    channel_id: int | str = Field(...)
    post_id: str = Field(...)
    id_type: str = Field(...)


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class PostSchemaManyChannel(BaseModel):
    channels_id: list = Field(...)
    post_id: str = Field(...)
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
