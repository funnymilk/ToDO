from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings
from db.Base import Base   

settings = Settings()


engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)