from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Token, UserCreate
from app.models.user import UserModel
from app.services.hashing import verify_password, get_hashed_password
from app.services.JWTtoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError


def login_user(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(UserModel).filter(UserModel.email == request.username).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(user=user, access_token=access_token, token_type="bearer")


def create_user(request: UserCreate, db: Session):
    existing_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email is already exist",
        )

    hashed_password = get_hashed_password(request.password)
    user = UserModel(
        name=request.name.title(),
        email=request.email,
        password=hashed_password,
    )

    try:
        db.add(user)
        db.commit()
        return {"detail": "Account created please login to continue"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )
