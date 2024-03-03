from os import path

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.responses import ErrorMessage

from app.database.crud import get_image


router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.get(
    "/{img_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Image not found",
        }
    },
)
def read_image(
    img_id: int,
    db: Session = Depends(get_db),
):
    image = get_image(db, img_id=img_id)
    if not image or not path.isfile(str(image.image_path)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return FileResponse(str(image.image_path))
