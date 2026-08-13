from fastapi.responses import RedirectResponse
from src.core.settings import settings
from typing import List
from fastapi import APIRouter, Request, status
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["MMORPG API"])

# @router.post("/inventory-orders", response_model=InventoryOrderCreateResponseDTO, status_code=status.HTTP_201_CREATED)
# @router.get("/discord/login")
# async def login():
#     url = (
#         settings.redirect_uri
#     )

#     return RedirectResponse(url)
#     # url = discord_gateway.get_authorization_url()

#     # return RedirectResponse(url)

@router.get("/discord/callback")
async def callback(
    request: Request,
    code: str,
):
    use_case = request.app.state.container['authenticate_with_discord_uc']
    token = await use_case.execute(code)

    return token