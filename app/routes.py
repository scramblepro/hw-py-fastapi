from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas, dependencies  # <-- исправленный импорт

router = APIRouter()

async def get_db():
    async for session in dependencies.get_db():
        yield session

@router.post("/ads/", response_model=schemas.AdvertisementResponse)
async def create_advertisement(
    ad: schemas.AdvertisementCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_ad(db, ad)

@router.get("/ads/{ad_id}", response_model=schemas.AdvertisementResponse)
async def get_advertisement(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await crud.get_ad_by_id(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad

@router.get("/ads/", response_model=list[schemas.AdvertisementResponse])
async def list_advertisements(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_ads(db)

@router.put("/ads/{ad_id}", response_model=schemas.AdvertisementResponse)
async def update_advertisement(
    ad_id: int, ad_update: schemas.AdvertisementUpdate, db: AsyncSession = Depends(get_db)
):
    return await crud.update_ad(db, ad_id, ad_update)

@router.delete("/ads/{ad_id}")
async def delete_advertisement(ad_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_ad(db, ad_id)
    return {"detail": "Advertisement deleted"}
