from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AdvertisementBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class AdvertisementResponse(AdvertisementBase):
    id: int
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True
