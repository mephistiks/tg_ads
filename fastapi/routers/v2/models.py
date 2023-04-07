from pydantic import BaseModel, Field


class NewPostSchema(BaseModel):
    file_name: str = Field(...)
    post_name: str = Field(...)
    post_text: str = Field(...)
    buttons: list = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class PostSchema(BaseModel):
    channel_id: int | str = Field(...)
    post_id: str = Field(...)
    #id_type: str = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
