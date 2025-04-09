from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Adverstiment_services_api",
    version="1.0",
    description="Ads API",
)

app.include_router(router)

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @app.get("/")
# def read_root():
#     return {"message": "API is running"}
                                                