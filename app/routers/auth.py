from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import Token, UserCreate, UserResponse
from app.db.database import get_db
from app.repo.auth import (
    login_user,
    create_user,
)

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/create")
def signup(request: UserCreate, db: Session = Depends(get_db)):
    return create_user(request=request, db=db)


@router.post("/login", response_model=Token)
def create_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(request=request, db=db)
