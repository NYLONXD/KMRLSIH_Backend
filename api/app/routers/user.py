from fastapi import APIRouter
from api.app.config import supabase
from api.app.schemas.models import VIEWRequest, changeNameRequest, changePhoneRequest, changeEmailRequest, changeDepartmentRequest

router = APIRouter()

@router.get("/{user_id}")
async def get_profile(user_id: str):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return {"user": response.data}

@router.post("/cname")
async def change_name(request: changeNameRequest):
    response = supabase.table("users").update({"name": request.name}).eq("id", request.user_id).execute()
    return {"user": response.data}

@router.post("/cemail")
async def change_email(request: changeEmailRequest):
    response = supabase.table("users").update({"email": request.email}).eq("id", request.user_id).execute()
    return {"user": response.data}

@router.post("/cphone")
async def change_phone(request: changePhoneRequest):
    response = supabase.table("users").update({"phone": request.phone}).eq("id", request.user_id).execute()
    return {"user": response.data}

@router.post("/cdept")
async def change_department(request: changeDepartmentRequest):
    dept_response = supabase.table("departments").select("dept_id").eq("name", request.dept_name).execute()
    if not dept_response.data:
        return {"error": "Department not found"}
    dept_id = dept_response.data[0]['dept_id']
    response = supabase.table("users").update({"department": dept_id}).eq("id", request.user_id).execute()
    return {"user": response.data}

@router.get("/history/{user_id}")
async def history(user_id: str):
    response = supabase.table("views").select("*").eq("user_id", user_id).execute()
    if response.data:
        return {"history": response.data}
    return {"error": "No history found"}

@router.post("/viewed")
async def viewed(request: VIEWRequest):
    existing = supabase.table("views").select("*").eq("user_id", request.user_id).eq("doc_id", request.doc_id).execute()

    if existing.data:
        return {"message": "Already viewed"}

    supabase.table("views").insert({
        "user_id": request.user_id,
        "doc_id": request.doc_id
    }).execute()
    return {"message": "View logged"}
