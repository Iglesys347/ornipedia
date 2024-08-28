from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
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
    bird_id = Column(Integer, ForeignKey("birds.id"), nullable=False)
    language_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    sub_species = Column(String, nullable=False)
    details = Column(String)

    bird = relationship("Bird", back_populates="translations")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    bird_id = Column(Integer, ForeignKey("birds.id"), nullable=False)
    license_id = Column(Integer, ForeignKey("image_licenses.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("image_authors.id"), nullable=False)
    image_path = Column(String, nullable=False)
    original_url = Column(String, nullable=False)

    bird = relationship("Bird", back_populates="images")
    license = relationship("ImageLicense")
    author = relationship("ImageAuthor")


class ImageLicense(Base):
    __tablename__ = "image_licenses"
    id = Column(Integer, primary_key=True, index=True)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    link = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("short_name", "link", name="img_license_uc"),)


class ImageAuthor(Base):
    __tablename__ = "image_authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String)

    __table_args__ = (UniqueConstraint("name", "link", name="img_author_uc"),)
