from fastapi import APIRouter, HTTPException, Depends, status
from passlib.context import CryptContext
import crud
import schemas
import dependencies
from schemas import update_ad
from crud import AdvertisementResponse, AdvertisementUpdate
from dependencies import UserDependency, get_db, get_current_user
from models import User, Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth import create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Pydantic-модель для регистрации пользователя
class UserRegister(BaseModel):
    name: str
    password: str


@router.post("/users/register")
async def register_user(user_data: UserRegister, db: dependencies.SessionDependency):
    """Регистрация нового пользователя."""
    hashed_password = pwd_context.hash(user_data.password)
    user = User(name=user_data.name, password=hashed_password)
    db.add(user)
    await db.commit()
    return {"detail": "User registered"}


@router.post("/users/login")
async def login_user(db: dependencies.SessionDependency, user_data: UserRegister):
    """Авторизация пользователя."""
    result = await db.execute(select(User).where(User.name == user_data.name))
    user = result.unique().scalar_one_or_none()
    if not user or not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = await create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/roles/assign")
async def assign_role(user_id: int, role_id: int, db: dependencies.SessionDependency):
    """Назначение роли пользователю."""
    user = await db.get(User, user_id)
    role = await db.get(Role, role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    user.roles.append(role)
    await db.commit()
    return {"detail": "Role assigned"}


@router.get("/roles/")
async def list_roles(db: dependencies.SessionDependency):
    """Получение списка ролей."""
    result = await db.execute(select(Role))
    return result.scalars().all()


@router.post("/ads/", response_model=crud.AdvertisementResponse)
async def create_advertisement(
    ad: crud.AdvertisementCreate, 
    db: dependencies.SessionDependency, 
    current_user=Depends(get_current_user),
):
    """Создание объявления."""
    return await schemas.create_ad(db, ad, user_id=current_user.id)


@router.get("/ads/{ad_id}", response_model=crud.AdvertisementResponse)
async def get_advertisement(ad_id: int, db: dependencies.SessionDependency):
    """Получение объявления по ID."""
    ad = await schemas.get_ad_by_id(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@router.get("/ads/", response_model=list[crud.AdvertisementResponse])
async def list_advertisements(db: dependencies.SessionDependency):
    """Получение списка всех объявлений."""
    return await schemas.get_all_ads(db)


@router.put("/ads/{ad_id}", response_model=AdvertisementResponse)
async def update_ad_endpoint(
    ad_id: int,
    ad_data: AdvertisementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_ad = await update_ad(db, ad_id, ad_data, current_user.id)

    if updated_ad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объявление не найдено или у вас нет прав на его редактирование",
        )

    return updated_ad


@router.delete("/ads/{ad_id}")
async def delete_advertisement(
    ad_id: int,
    db: dependencies.SessionDependency,
    current_user=Depends(get_current_user),
):
    success = await schemas.delete_ad(db, ad_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Объявление не найдено или у вас нет прав на его удаление",
        )
    return {"detail": "Advertisement deleted"}


@router.get("/users/me")
async def get_current_user_info(current_user: UserDependency):
    return {"id": current_user.id, "name": current_user.name}
