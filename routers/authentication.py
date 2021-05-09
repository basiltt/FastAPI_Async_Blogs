from fastapi import APIRouter, HTTPException, Depends, status
from models.schemas import Login
from models.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import utilities.services as services
from models.schemas import ShowUser, User, ShowUserBase
from utilities.hashing import Hash
from datetime import timedelta
from security.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await services.get_user_login(request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
