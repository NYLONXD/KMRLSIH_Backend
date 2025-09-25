from fastapi import APIRouter
from api.app.config import supabase

router = APIRouter()

@router.get("/{user_id}")
async def get_transexions(user_id: str):
    response = supabase.table("transexions").select("*").eq("from_user", user_id).execute()
    if not response.data:
        return {"message": "No transexions found"}
    return {"transexions": response.data}
