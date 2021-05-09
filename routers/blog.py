from fastapi import APIRouter, HTTPException, Depends, status
from models.schemas import ShowBlog, Blog, User
import utilities.services as services
from typing import List
from models.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from security.oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['Blogs'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowBlog)
async def create_blog(request: Blog, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await services.create_blog(db, request)


@router.get("/{id}", response_model=ShowBlog)
async def get_blog(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = await services.get_blog(db, id=id)
    if blog:
        return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")


@router.get('/', response_model=List[ShowBlog])
async def get_all_blogs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    out = await services.get_all_blogs(db)
    return out


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
async def update_blog(id: int, request: Blog, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    out = await services.update_blog(id, request, db)
    if out:
        return out
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_blog(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if await services.delete_blog(id, db):
        return {'data': f'Blog with the id {id} deleted'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
