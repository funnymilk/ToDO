from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.schemas import LoginData, UserCreate, UserOut
from services.auth_service import login, create_user

router = APIRouter()

@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoind(user: UserCreate, db: Session = Depends(get_db)):   
    return create_user(user, db)

@router.post("/login")
def login_endpoiint(user: LoginData, db: Session = Depends(get_db)):
    return login(user, db)