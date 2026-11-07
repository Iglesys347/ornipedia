"""Quiz: find a bird among a few choices (by its photo, by its name...)."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import db_models
from src.dependencies import get_db
from src.models.responses import ErrorMessage
from src.models.schemas import AuthorInfo, LicenseInfo
from src.quiz import new_question

# the birds already asked that the client can exclude
MAX_EXCLUDED = 200

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


class QuizImage(BaseModel):
    id: int
    # the photos are under free licenses: their credits are shown with them
    author: AuthorInfo
    license: LicenseInfo


class QuizChoice(BaseModel):
    bird_id: int
    name: str
    latin_name: str
    group: str
    subgroup: str | None = None
    image: QuizImage


class QuizQuestion(BaseModel):
    # the bird to find, one of the choices
    answer_id: int
    choices: list[QuizChoice]


@router.get(
    "/question",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Not enough birds with photos in this language",
        }
    },
    response_model=QuizQuestion,
)
def read_question(
    language: str = "fr",
    difficulty: Literal["easy", "hard"] = Query(
        default="easy",
        description="easy: the choices are random birds,"
        " hard: they are from the same subgroup or group as the answer when possible",
    ),
    exclude: list[int] = Query(
        default=[],
        max_length=MAX_EXCLUDED,
        description="Birds that should not be asked (e.g. the ones already asked)",
    ),
    db: Session = Depends(get_db),
):
    question = new_question(db, language, difficulty, exclude)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enough birds with photos in this language",
        )
    answer, choices, image_ids = question
    images = {
        image.id: image
        for image in db.query(db_models.Image)
        .filter(db_models.Image.id.in_(image_ids.values()))
        .all()
    }
    return QuizQuestion(
        answer_id=answer.id,
        choices=[
            QuizChoice(
                bird_id=bird.id,
                name=bird.name,
                latin_name=bird.latin_name,
                group=bird.group,
                subgroup=bird.subgroup,
                image=QuizImage(
                    id=image_ids[bird.id],
                    author=AuthorInfo.model_validate(
                        images[image_ids[bird.id]].author, from_attributes=True
                    ),
                    license=LicenseInfo.model_validate(
                        images[image_ids[bird.id]].license, from_attributes=True
                    ),
                ),
            )
            for bird in choices
        ],
    )
