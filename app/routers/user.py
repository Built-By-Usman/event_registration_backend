from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import UserModel
from app.schemas.user import UserResponse, UserUpdate, UserBooking
from typing import List
from app.services.oauth2 import get_current_user
from sqlalchemy.sql import func

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).filter(UserModel.is_applied == True).all()
    return users


@router.put("/ticket-booking", response_model=UserResponse)
def ticket_booking(
    request: UserBooking,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    existing_roll_no = (
        db.query(UserModel).filter(UserModel.roll_no == request.roll_no).first()
    )
    if existing_roll_no:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this roll number is alrerady exist",
        )
    try:
        user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
        user.father_name = request.father_name
        user.roll_no = request.roll_no
        user.section = request.section
        user.semester = request.semester
        user.is_applied = True

        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")


@router.put("/update-status", response_model=UserResponse)
def update_user(request: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == request.id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # update only user fields
        if request.status is not None:
            user.status = request.status

        db.commit()
        db.refresh(user)

        return user

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")


@router.put("/scan-ticket/{user_id}", response_model=UserResponse)
def scan_ticket(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # prevent double scanning
        if user.is_ticket_used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This ticket is already scanned",
            )

        user.is_ticket_used = True
        user.entered_time = func.now()
        db.commit()
        db.refresh(user)

        return user

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this id is not available",
        )
    return user
