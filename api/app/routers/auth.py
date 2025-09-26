from fastapi import APIRouter, HTTPException
from httpx import request
from api.app.config import supabase
from api.app.schemas.models import LoginRequest, RegisterRequest
from api.app.utils.security import hash_password, verify_password

router = APIRouter()

@router.post("/register")
async def register(request: RegisterRequest):
    response = supabase.table("users").select("*").eq("email", request.email).execute()
    if response.data:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = request.password

    dept_resp = supabase.table("departments").select("dept_id").eq("name", request.department).execute()
    if not dept_resp.data:
        raise HTTPException(status_code=400, detail="Department not found")
    dept_id = dept_resp.data[0]["dept_id"]

    response_1 = supabase.table("users").insert({
        "email": request.email,
        "password": hashed_password,
        "role": request.role,
        "name": request.name,
        "department": dept_id,
        "phone": request.phone
    }).execute()
    return {"success": True, "message": "User registered successfully","user_id" : response_1.data[0]["id"]}


@router.post("/login")
async def login(request: LoginRequest):
    try:
        # Fetch user by ID
        response = (
            supabase.table("users")
            .select("*")
            .eq("id", request.user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = response.data[0]

        # Successful login
        if request.password == user["password"]:
            return {"success": True, "message": "Login successful", "user": user}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except HTTPException:
        raise  # re-raise known errors
    except Exception as e:
        # Log the error (replace with proper logging in prod)
        print("Login error:", str(e))
        raise HTTPException(status_code=500, detail="Login failed. Please try again.")

@router.post("/department")
async def create_department(name: str):
    response = supabase.table("departments").insert({"name": name}).execute()
    return {"success": True, "message": response.data[0]}

@router.get("/dept_name")
async def get_dept_name(dept_id: str):
    response = supabase.table("departments").select("name").eq("dept_id", dept_id).execute()
    # print(response,"<= response")
    return {"success": True, "message": response.data[0]["name"] if response.data else "Department not found"}