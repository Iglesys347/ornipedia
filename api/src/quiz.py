"""Generation of the quiz questions: a bird to find among up to 4 choices.

The same question is used by all the quiz formats (photo -> name, name -> photo...):
each choice has a name and a photo, the front shows the ones it needs.
"""

import random
from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.database import db_models

CHOICES_COUNT = 4
DIFFICULTIES = ("easy", "hard")


@dataclass
class QuizBird:
    id: int
    name: str
    latin_name: str
    group: str
    subgroup: str | None


def _quiz_birds(db: Session, language: str) -> list[QuizBird]:
    """Birds having a translation in the language and at least one photo."""
    with_images = db.query(db_models.Image.bird_id).distinct()
    rows = (
        db.query(
            db_models.Bird.id,
            db_models.Translation.name,
            db_models.Bird.latin_name,
            db_models.Translation.group_name,
            db_models.Translation.subgroup_name,
        )
        .join(db_models.Translation, db_models.Translation.bird_id == db_models.Bird.id)
        .filter(db_models.Translation.language_code == language)
        .filter(db_models.Bird.id.in_(with_images))
        .all()
    )
    birds: dict[int, QuizBird] = {}
    for row in rows:
        # a single translation per bird and language is expected
        birds.setdefault(row[0], QuizBird(*row[:4], row[4] or None))
    return list(birds.values())


def _shuffled(birds: list[QuizBird]) -> list[QuizBird]:
    return random.sample(birds, len(birds))


def _distractors(answer: QuizBird, birds: list[QuizBird], difficulty: str) -> list[QuizBird]:
    """Other birds to choose from, the closest to the answer first when the quiz is hard
    (same subgroup, then same group, then any bird)."""
    others = [bird for bird in birds if bird.id != answer.id]
    if difficulty == "hard":
        same_subgroup = [b for b in others if answer.subgroup and b.subgroup == answer.subgroup]
        same_group = [b for b in others if b.group == answer.group and b not in same_subgroup]
        rest = [b for b in others if b.group != answer.group]
        candidates = _shuffled(same_subgroup) + _shuffled(same_group) + _shuffled(rest)
    else:
        candidates = _shuffled(others)

    chosen: list[QuizBird] = []
    names = {answer.name.lower()}
    for bird in candidates:
        # two choices with the same name could not be told apart
        if bird.name.lower() in names:
            continue
        chosen.append(bird)
        names.add(bird.name.lower())
        if len(chosen) == CHOICES_COUNT - 1:
            break
    return chosen


def _random_images(db: Session, bird_ids: list[int]) -> dict[int, int]:
    """A random photo of each bird."""
    rows = (
        db.query(db_models.Image.bird_id, db_models.Image.id)
        .filter(db_models.Image.bird_id.in_(bird_ids))
        .all()
    )
    images: dict[int, list[int]] = {}
    for bird_id, image_id in rows:
        images.setdefault(bird_id, []).append(image_id)
    return {bird_id: random.choice(ids) for bird_id, ids in images.items()}


def new_question(
    db: Session, language: str, difficulty: str = "easy", exclude: list[int] | None = None
) -> tuple[QuizBird, list[QuizBird], dict[int, int]] | None:
    """The bird to find, the shuffled choices (the bird included) and a photo of each choice.
    The excluded birds (e.g. the ones already asked) are not asked again while possible.
    None when there are not enough birds with photos to make a question."""
    birds = _quiz_birds(db, language)
    if len(birds) < 2:
        return None
    excluded = set(exclude or [])
    # every bird has been asked: the excluded ones are asked again
    answer = random.choice([b for b in birds if b.id not in excluded] or birds)
    distractors = _distractors(answer, birds, difficulty)
    if not distractors:
        return None
    choices = _shuffled([answer, *distractors])
    return answer, choices, _random_images(db, [bird.id for bird in choices])
