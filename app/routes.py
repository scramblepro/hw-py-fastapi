from fastapi import APIRouter, HTTPException
import crud
import schemas
import dependencies

router = APIRouter()

@router.post("/ads/", response_model=crud.AdvertisementResponse)
async def create_advertisement(
    ad: crud.AdvertisementCreate, db: dependencies.SessionDependency
):
    return await schemas.create_ad(db, ad)

@router.get("/ads/{ad_id}", response_model=crud.AdvertisementResponse)
async def get_advertisement(ad_id: int, db: dependencies.SessionDependency):
    ad = await schemas.get_ad_by_id(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad

@router.get("/ads/", response_model=list[crud.AdvertisementResponse])
async def list_advertisements(db: dependencies.SessionDependency):
    return await schemas.get_all_ads(db)

@router.put("/ads/{ad_id}", response_model=crud.AdvertisementResponse)
async def update_advertisement(
    ad_id: int, ad_update: crud.AdvertisementUpdate, db: dependencies.SessionDependency
):
    return await schemas.update_ad(db, ad_id, ad_update)

@router.delete("/ads/{ad_id}")
async def delete_advertisement(ad_id: int, db: dependencies.SessionDependency):
    await schemas.delete_ad(db, ad_id)
    return {"detail": "Advertisement deleted"}