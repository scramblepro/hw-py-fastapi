from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Todo API",
    version="1.0",
    description="A simple TODO API",
)

app.include_router(router)
