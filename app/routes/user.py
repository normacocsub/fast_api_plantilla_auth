from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth_utils import auth_required

from app.services.user import get_user_by_email, create_user, get_user, update_user
from app.schemas.user import UserCreate, UserBase, User, UserUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(user=user, db=db)


@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db), token: str = Security(auth_required(["Usuario"]))):
    try:
        db_user = get_user(user_id=user_id, db=db)
        if db_user is None:
            return JSONResponse(content={"message": "User not found"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: " + str(e),
        )


@router.put("/{user_id}")
def update_userr(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = update_user(user_id=user_id, user=user, db=db)
        if db_user is None:
            return JSONResponse(content={"message": "User not found"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: " + str(e),
        )


@router.delete("/{user_id}")
def deletee_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = deletee_user(user_id=user_id, db=db)
        if db_user is None:
            return JSONResponse(content={"message": "User not found"},
                                status_code=status.HTTP_404_NOT_FOUND)
        return db_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: " + str(e),
        )
