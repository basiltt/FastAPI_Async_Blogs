from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import engine, Base
from sqlalchemy.orm import sessionmaker
from routers import blog, user, authentication

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


@app.on_event("startup")
async def start_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
