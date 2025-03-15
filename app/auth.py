from bcrypt import checkpw, gensalt, hashpw
from config import DEFAULT_ROLE
from fastapi import HTTPException
from models import Right, Role, Token, User, user_roles, role_rights
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


async def check_access_rights(
    session: AsyncSession,
    token: Token,
    model,
    write: bool = False,
    read: bool = False,
    owner_field: str = "user_id",
    raise_exception: bool = True,
) -> bool:
    """
    Проверяет права владельца токена на модель.
    """
    where_args = [User.id == token.user_id, Right.model == model.__tablename__]
    
    if write:
        where_args.append(Right.write.is_(True))
    if read:
        where_args.append(Right.read.is_(True))
    
    if hasattr(model, owner_field) and getattr(model, owner_field) != token.user_id:
        where_args.append(Right.only_own.is_(False))
    
    rights_query = (
        select(func.count(User.id))
        .join(user_roles, user_roles.c.user_id == User.id)
        .join(Role, Role.id == user_roles.c.role_id)
        .join(role_rights, role_rights.c.role_id == Role.id)
        .join(Right, Right.id == role_rights.c.right_id)
        .where(*where_args)
    )
    
    rights_count = (await session.execute(rights_query)).scalar()
    
    if not rights_count and raise_exception:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return rights_count > 0


async def get_default_role(session: AsyncSession) -> Role:
    """
    Возвращает роль по умолчанию.
    """
    return (await session.scalars(select(Role).where(Role.name == DEFAULT_ROLE))).first()
