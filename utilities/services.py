import asyncio

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas import Blog, User, ShowUser, ShowBlog, Login
import models.models as models
from utilities.hashing import Hash
from typing import List


async def get_user_login(request: Login, db: AsyncSession):
    db_execute = await db.execute(select(models.User).where(models.User.email == request.username))
    # print(db_execute.first())
    # await asyncio.sleep(10000)
    return db_execute.scalars().first()


async def create_user(db: AsyncSession, request: User):
    new_user = models.User(name=request.name, email=request.email, password=Hash.encrypt(request.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return ShowUser.from_orm(new_user)


async def get_user(db: AsyncSession, id: int):
    return await db.get(entity=models.User, ident=id)


async def get_all_users(db: AsyncSession):
    db_execute = await db.execute(select(models.User))
    return db_execute.scalars().all()


async def update_user(id: int, request: User, db: AsyncSession) -> ShowBlog:
    user_obj = await db.get(entity=models.User, ident=id)
    if user_obj:
        await db.execute(update(models.User).where(models.User.id == id).values(name=request.name, email=request.email,
                                                                                password=Hash.encrypt(
                                                                                    request.password)))
        await db.commit()
        await db.refresh(user_obj)
        return user_obj


async def delete_user(id: int, db: AsyncSession):
    user = await db.get(entity=models.User, ident=id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False


async def create_blog(db: AsyncSession, request: Blog) -> ShowBlog:
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


async def get_blog(db: AsyncSession, id: int):
    return await db.get(entity=models.Blog, ident=id)


async def get_all_blogs(db: AsyncSession):
    db_execute = await db.execute(select(models.Blog))
    return db_execute.scalars().all()


async def update_blog(id: int, request: Blog, db: AsyncSession) -> ShowBlog:
    blog_obj = await db.get(entity=models.Blog, ident=id)
    if blog_obj:
        await db.execute(
            update(models.Blog).where(models.Blog.id == id).values(title=request.title, body=request.body, user_id=1))
        await db.commit()
        await db.refresh(blog_obj)
        return blog_obj


async def delete_blog(id: int, db: AsyncSession) -> bool:
    blog = await db.get(entity=models.Blog, ident=id)
    if blog:
        await db.delete(blog)
        await db.commit()
        return True
    return False
