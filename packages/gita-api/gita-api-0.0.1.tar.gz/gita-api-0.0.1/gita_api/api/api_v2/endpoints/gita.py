import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from gita.api import deps
from gita.models import gita as models
from gita.schemas import gita as schemas

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/chapters/", response_model=List[schemas.GitaChapter], tags=["chapters"])
def get_all_chapters(
    skip: int = 0, limit: int = 18, db: Session = Depends(deps.get_db)
):
    chapters = (
        db.query(models.GitaChapter)
        .order_by(models.GitaChapter.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return chapters


@router.get(
    "/chapters/{chapter_number}/", response_model=schemas.GitaChapter, tags=["chapters"]
)
def get_particular_chapter(chapter_number: int, db: Session = Depends(deps.get_db)):
    chapter = (
        db.query(models.GitaChapter)
        .filter(models.GitaChapter.chapter_number == chapter_number)
        .first()
    )
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.get("/verses/", response_model=List[schemas.GitaVerse], tags=["verses"])
def get_all_verses_from_all_chapters(
    skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)
):
    verses = (
        db.query(models.GitaVerse)
        .options(
            joinedload(models.GitaVerse.commentaries),
            joinedload(models.GitaVerse.translations),
        )
        .order_by(models.GitaVerse.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return verses


@router.get(
    "/chapters/{chapter_number}/verses/",
    response_model=List[schemas.GitaVerse],
    tags=["verses"],
)
def get_all_verses_from_particular_chapter(
    chapter_number: int, db: Session = Depends(deps.get_db)
):
    verses = (
        db.query(models.GitaVerse)
        .options(
            joinedload(models.GitaVerse.commentaries),
            joinedload(models.GitaVerse.translations),
        )
        .order_by(models.GitaVerse.id.asc())
        .filter(models.GitaVerse.chapter_number == chapter_number)
        .all()
    )
    if verses is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verses


@router.get(
    "/chapters/{chapter_number}/verses/{verse_number}/",
    response_model=schemas.GitaVerse,
    tags=["verses"],
)
def get_particular_verse_from_chapter(
    chapter_number: int, verse_number: int, db: Session = Depends(deps.get_db)
):
    verse = (
        db.query(models.GitaVerse)
        .options(
            joinedload(models.GitaVerse.commentaries),
            joinedload(models.GitaVerse.translations),
        )
        .filter(
            models.GitaVerse.chapter_number == chapter_number,
            models.GitaVerse.verse_number == verse_number,
        )
        .first()
    )
    if verse is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse
