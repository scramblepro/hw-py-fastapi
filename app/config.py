import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB", "rest_na_fast")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "KiryhaTheBest")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


TOKEN_TTL = int(os.getenv("TOKEN_TTL", 60))

SQL_DEBUG = os.getenv("SQL_DEBUG", "False").lower() in ("true", "1")
DEFAULT_ROLE = os.getenv("DEFAULT_ROLE", "user")

engine = create_async_engine(PG_DSN, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)