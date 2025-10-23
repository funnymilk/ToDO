from db.session import engine
from db.Base import Base   

def init_db():
    Base.metadata.create_all(bind=engine)
