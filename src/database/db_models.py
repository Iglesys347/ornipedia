from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Bird(Base):
    __tablename__ = "birds"

    id = Column(Integer, primary_key=True, index=True)
    latin_name = Column(String, nullable=False)

    translations = relationship("Translation", back_populates="bird", lazy="noload")
    images = relationship("Image", back_populates="bird", lazy="joined")

    def flat_dict(self):
        bird_dict = {"id": self.id, "latin_name": self.latin_name}
        if self.translations:
            translation = self.translations[0]
            bird_dict.update(
                {
                    "name": translation.name,
                    "species": translation.species,
                    "sub_species": (
                        translation.sub_species if translation.sub_species else ""
                    ),
                    "details": translation.details if translation.details else "",
                    "language_code": translation.language_code,
                }
            )
        bird_dict["image_ids"] = []
        if self.images:
            bird_dict["image_ids"] = [image.id for image in self.images]
        return bird_dict


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    bird_id = Column(Integer, ForeignKey("birds.id"))
    language_code = Column(String)
    name = Column(String)
    species = Column(String)
    sub_species = Column(String)
    details = Column(String)

    bird = relationship("Bird", back_populates="translations")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    bird_id = Column(Integer, ForeignKey("birds.id"))
    image_path = Column(String)

    bird = relationship("Bird", back_populates="images")
