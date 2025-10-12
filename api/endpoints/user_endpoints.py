from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.schemas import UserOut
from services.user_service import get_user

router = APIRouter()

@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoind(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)