from fastapi import APIRouter, HTTPException, Depends, status
from models.schemas import ShowUser, User, ShowUserBase
import utilities.services as services
from typing import List
from models.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix='/user',
    tags=['Users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowUserBase)
async def create_user(request: User, db: AsyncSession = Depends(get_db)):
    return await services.create_user(db, request)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await services.get_user(db, id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")


@router.get('/', response_model=List[ShowUser])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await services.get_all_users(db)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=ShowUserBase)
async def update_user(id: int, request: User, db: AsyncSession = Depends(get_db)):
    out = await services.update_user(id, request, db)
    if out:
        return out
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    if await services.delete_user(id, db):
        return {'data': f'User with the id {id} deleted'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
