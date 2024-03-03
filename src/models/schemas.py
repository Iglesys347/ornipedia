from typing import Any
from pydantic import BaseModel, model_validator

from app.database import db_models


class TranslationBase(BaseModel):
    name: str
    species: str
    sub_species: str | None = None
    details: str | None = None


class TranslationNoID(TranslationBase):
    language_code: str


class Translation(TranslationNoID):
    id: int
    bird_id: int


class BirdBase(BaseModel):
    id: int
    latin_name: str


class Bird(BirdBase, TranslationNoID):

    @model_validator(mode="before")
    @classmethod
    def convert_db_bird(cls, data: Any) -> Any:
        if isinstance(data, db_models.Bird):
            return data.flat_dict()
        return data


class Image(BaseModel):
    id: int
    bird_id: int
    image_path: str


class BirdWithImages(Bird):
    image_ids: list[int]
