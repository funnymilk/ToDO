from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()