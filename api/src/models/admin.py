from pydantic import BaseModel, Field, field_validator


class TranslationIn(BaseModel):
    language_code: str = Field(pattern=r"^[a-z]{2}$")
    name: str = Field(min_length=1, max_length=200)
    species: str = Field(min_length=1, max_length=200)
    sub_species: str | None = Field(default=None, max_length=200)
    details: str | None = None

    @field_validator("name", "species", "sub_species", "details", mode="before")
    @classmethod
    def strip(cls, value):
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value


class BirdIn(BaseModel):
    latin_name: str = Field(min_length=1, max_length=200)
    translations: list[TranslationIn] = Field(min_length=1)

    @field_validator("latin_name", mode="before")
    @classmethod
    def strip(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("translations")
    @classmethod
    def one_translation_per_language(cls, translations):
        languages = [t.language_code for t in translations]
        if len(languages) != len(set(languages)):
            raise ValueError("only one translation per language")
        return translations


class BirdCreated(BaseModel):
    id: int
    latin_name: str


class AuthorOut(BaseModel):
    id: int
    name: str | None = None
    link: str | None = None


class LicenseOut(BaseModel):
    id: int
    short_name: str
    full_name: str
    link: str


class CommonsPhotoOut(BaseModel):
    title: str
    page_url: str
    thumbnail_url: str
    width: int
    height: int
    description: str
    author_name: str
    author_link: str | None = None
    license_short_name: str
    license_full_name: str
    license_link: str
    # this photo is already in Ornipedia
    already_added: bool


class CommonsSearchOut(BaseModel):
    items: list[CommonsPhotoOut]
    # offset of the next results, None when there are no more results
    next_offset: int | None = None


class CommonsImport(BaseModel):
    title: str = Field(pattern=r"^File:.+", max_length=300)
