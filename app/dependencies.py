import datetime
import uuid
from typing import Annotated, AsyncGenerator
from config import async_session, TOKEN_TTL
from fastapi import Depends, Header, HTTPException
from models import Token, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth import verify_access_token
from fastapi.security import OAuth2PasswordBearer

# Создаем схему для OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных."""
    async with async_session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_db, use_cache=True)]


async def get_token(
    session: SessionDependency, x_token: Annotated[uuid.UUID | None, Header()] = None
) -> Token:
    """Получение токена из заголовка запроса."""
    token_query = select(Token).where(
        Token.token == x_token,
        Token.creation_time >= datetime.datetime.utcnow() - datetime.timedelta(seconds=TOKEN_TTL),
    )
    token = (await session.scalars(token_query)).first()
    if token:
        return token
    raise HTTPException(status_code=401, detail="Invalid token")


TokenDependency = Annotated[Token, Depends(get_token)]


async def get_current_user(
    db: SessionDependency, token: str = Depends(oauth2_scheme)
) -> User:
    """Получение текущего пользователя по токену."""
    user_id = await verify_access_token(token)
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


UserDependency = Annotated[User, Depends(get_current_user)]
