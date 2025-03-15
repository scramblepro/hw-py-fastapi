from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Advertisement
from crud import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse
from typing import List, Optional


async def create_ad(db: AsyncSession, ad_data: AdvertisementCreate, user_id: int) -> Optional[Advertisement]:
    """Создание объявления"""
    new_ad = Advertisement(
        title=ad_data.title,
        description=ad_data.description,
        price=ad_data.price,
        author_id=user_id,
    )
    db.add(new_ad)
    await db.commit()
    await db.refresh(new_ad)
    return new_ad


async def get_all_ads(db: AsyncSession) -> List[Advertisement]:
    """Получение списка всех объявлений"""
    result = await db.execute(select(Advertisement))
    return result.scalars().all()


async def get_ad_by_id(db: AsyncSession, ad_id: int) -> Optional[Advertisement]:
    """Получение объявления по ID"""
    result = await db.execute(select(Advertisement).where(Advertisement.id == ad_id))
    return result.scalar_one_or_none()


async def update_ad(db: AsyncSession, ad_id: int, ad_data: AdvertisementUpdate, user_id: int) -> Optional[Advertisement]:
    """Обновление объявления (пользователь может редактировать только свои объявления)"""
    result = await db.execute(select(Advertisement).where(Advertisement.id == ad_id, Advertisement.author_id == user_id))
    ad = result.scalar_one_or_none()

    if not ad:
        return None

    for key, value in ad_data.dict(exclude_unset=True).items():
        setattr(ad, key, value)

    await db.commit()
    await db.refresh(ad)
    return ad


async def delete_ad(db: AsyncSession, ad_id: int, user_id: int) -> bool:
    """Удаление объявления (только автор может удалить)"""
    result = await db.execute(select(Advertisement).where(Advertisement.id == ad_id, Advertisement.author_id == user_id))
    ad = result.scalar_one_or_none()

    if not ad:
        return False

    await db.delete(ad)
    await db.commit()
    return True


async def search_advertisements(db: AsyncSession, title: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[Advertisement]:
    """Поиск объявлений по заголовку и цене"""
    query = select(Advertisement)

    if title:
        query = query.where(Advertisement.title.ilike(f"%{title}%"))
    if min_price:
        query = query.where(Advertisement.price >= min_price)
    if max_price:
        query = query.where(Advertisement.price <= max_price)

    result = await db.execute(query)
    return result.scalars().all()