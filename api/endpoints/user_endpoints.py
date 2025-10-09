from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from db.session import SessionLocal, get_db
from schemas.schemas import UserCreate, UserOut
from services.auth_service import create_user
from services.user_service import get_user

router = APIRouter()

@router.get("/users/{user_id}", response_model=UserOut)
def get_user_endpoind(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)