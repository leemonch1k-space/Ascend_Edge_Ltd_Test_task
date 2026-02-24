from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import Base, engine
from app.api import lead_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(title="Lead Management CRM", lifespan=lifespan)

app.include_router(lead_router.router)
