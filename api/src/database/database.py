from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.settings import DB_URL, DB_DEBUG

engine = create_engine(DB_URL, echo=DB_DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
