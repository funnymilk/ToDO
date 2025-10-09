from fastapi import Depends, status, APIRouter
from requests import Session
from db.session import SessionLocal, get_db
from schemas.schemas import UserCreate, UserOut
from services.auth_service import create_user
from services.user_service import get_user

router = APIRouter()

@router.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoind(user: UserCreate, db: Session = Depends(get_db)):   
    return create_user(db, user)

@router.get("/users/{user_id}", response_model=UserOut)
def get_user_endpoind(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id, db)