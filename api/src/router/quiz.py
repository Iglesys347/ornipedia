from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
import random
from redis import Redis

from src.dependencies import get_db, get_redis
from src.database.sql.crud import get_random_image, get_bird
from src.database.sql import db_models
from src.models.responses import ErrorMessage

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


@router.get(
    "",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Quiz could not be generated",
        }
    },
)
def generate_quiz(
    # n_questions: int,
    species: str | None = None,
    sub_species: str | None = None,
    language: str = "fr",
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    random_image = get_random_image(db, species=species, sub_species=sub_species)
    if not random_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No birds or images available for the quiz",
        )

    correct_bird = get_bird(db, bird_id=random_image.bird_id, language=language)  # type: ignore
    if not correct_bird:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The selected bird could not be found",
        )

    incorrect_images_query = (
        db.query(db_models.Image.id)
        .join(db_models.Bird)
        .join(db_models.Translation)
        .filter(db_models.Translation.language_code == language)
        .filter(db_models.Image.bird_id != random_image.bird_id)
    )

    if species:
        incorrect_images_query = incorrect_images_query.filter(
            db_models.Translation.species == species
        )
    if sub_species:
        incorrect_images_query = incorrect_images_query.filter(
            db_models.Translation.sub_species == sub_species
        )

    total_incorrect_images = incorrect_images_query.count()
    if total_incorrect_images < 3:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enough images available for quiz options",
        )

    random_offsets = random.sample(range(total_incorrect_images), 3)
    incorrect_images = [
        incorrect_images_query.offset(offset).limit(1).one().id
        for offset in random_offsets
    ]

    options = incorrect_images + [random_image.id]
    random.shuffle(options)

    quiz_id = str(uuid4())

    redis.setex(
        f"quiz:{quiz_id}",
        600,
        random_image.id,  # type: ignore
    )

    return {
        "quiz_id": quiz_id,
        "quiz_image": random_image.id,
        "options": options,
    }


@router.post(
    "/validate",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Quiz not found or expired",
        },
    },
)
def validate_answer(
    quiz_id: str,
    selected_option: int,
    redis: Redis = Depends(get_redis),
):
    correct_answer = redis.get(f"quiz:{quiz_id}")
    if not correct_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found or expired",
        )

    is_correct = int(correct_answer) == selected_option  # type: ignore

    redis.delete(f"quiz:{quiz_id}")

    return {
        "is_correct": is_correct,
        "correct_answer": int(correct_answer),  # type: ignore
    }
