from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.presentation.api.routes.auth import router as auth_router

def create_app(container) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        pass
    
    app = FastAPI(
        title="MMORPG API", 
        version="0.1.0",
        description="Deal with bussines rules MMORPG",
    )

    app.state.container = container
    app.include_router(auth_router, prefix="/v1")
    
    return app
