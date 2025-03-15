import datetime
import uuid
from typing import Annotated, AsyncGenerator
from .config import async_session
from .config import TOKEN_TTL
from fastapi import Depends, Header, HTTPException
from .models import Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_db, use_cache=True)]

async def get_token(session: SessionDependency, x_token: Annotated[uuid.UUID | None, Header()] = None) -> Token:
    token_query = select(Token).where(
        Token.token == x_token,
        Token.creation_time >= datetime.datetime.utcnow() - datetime.timedelta(seconds=TOKEN_TTL),
    )
    token = (await session.scalars(token_query)).first()
    if token:
        return token
    raise HTTPException(status_code=401, detail="Invalid token")

TokenDependency = Annotated[Token, Depends(get_token)]