"""Groups of birds (e.g. "raptors") and their subgroups (e.g. "eagles")."""

from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from src.dependencies import get_db

from src.models.responses import MAX_PER_PAGE, PaginatedResponse

from src.database.crud import get_groups, get_subgroups


router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)


@router.get("", response_model=PaginatedResponse[str])
def read_groups(
    language: str = "fr",
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=25, ge=0, le=MAX_PER_PAGE),
    db: Session = Depends(get_db),
):
    return get_groups(db, language=language, page=page, per_page=per_page)


@router.get("/{group}", response_model=PaginatedResponse[str])
def read_subgroups(
    group: str,
    language: str = "fr",
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=25, ge=0, le=MAX_PER_PAGE),
    db: Session = Depends(get_db),
):
    return get_subgroups(db, group, language=language, page=page, per_page=per_page)
