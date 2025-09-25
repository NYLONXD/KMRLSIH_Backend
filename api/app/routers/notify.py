from fastapi import APIRouter, Form, UploadFile, File
import os
# from nlpPipelne.ProcessPipeline import process_file
from api.app.config import supabase
import cloudinary.uploader

router = APIRouter()

UPLOAD_DIR = "./temp"

@router.post("/email")
async def send_email(file: UploadFile = File(...), emailAdr: str = Form(...)):
    print(f"Received file: {file.filename} from email: {emailAdr}")
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(file_location, "wb") as f:
        f.write(content)

    try:
        # output = process_file(file_location)
        user_id = supabase.table("users").select("id").eq("email", emailAdr).execute().data[0]["id"]
        dept_id = supabase.table("users").select("department").eq("email", emailAdr).execute().data[0]["department"]

        upload_result = cloudinary.uploader.upload(content, resource_type="auto")

        doc_resp = supabase.table("documents").insert({
            "title": file.filename,
            "department": dept_id,
            "url": upload_result.get("public_url"),
            "doc_type": "general",
            "medium": "email",
            "priority": "normal",
        }).execute()
        inserted_doc = doc_resp.data[0] if doc_resp.data else None

        if inserted_doc:
            doc_id = inserted_doc["doc_id"]
            # supabase.table("summaries").insert({
            #     "doc_id": doc_id,
            #     "content": output.get("doc_summary", "")
            # }).execute()
            supabase.table("summaries").insert({
                "doc_id": doc_id,
                "content": ""
            }).execute()
            supabase.table("transexions").insert({
                "from_user": user_id,
                "to_department": dept_id,
                "doc_id": doc_id
            }).execute()

    finally:
        os.remove(file_location)

    # return {
    #     "document": doc_resp.data,
    #     "filename": file.filename,
    #     "processed": output,
    #     "cloudinary_url": upload_result.get("secure_url")
    # }
    return {
        "document": doc_resp.data,
        "filename": file.filename,
        "processed": "",
        "cloudinary_url": upload_result.get("secure_url")
    }

@router.post("/whatsapp")
async def send_message(file: UploadFile = File(...), phone: str = Form(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(file_location, "wb") as f:
        f.write(content)

    try:
        # output = process_file(file_location)
        user_id = supabase.table("users").select("id").eq("phone", phone).execute().data[0]["id"]
        dept_id = supabase.table("users").select("department").eq("phone", phone).execute().data[0]["department"]

        upload_result = cloudinary.uploader.upload(content, resource_type="auto")

        doc_resp = supabase.table("documents").insert({
            "title": file.filename,
            "department": dept_id,
            "url": upload_result.get("public_url"),
            "doc_type": "general",
            "medium": "whatsapp",
            "priority": "normal",
        }).execute()
        inserted_doc = doc_resp.data[0] if doc_resp.data else None

        if inserted_doc:
            doc_id = inserted_doc["doc_id"]
            # supabase.table("summaries").insert({
            #     "doc_id": doc_id,
            #     "content": output.get("doc_summary", "")
            # }).execute()
            supabase.table("summaries").insert({
                "doc_id": doc_id,
                "content": ""
            }).execute()
            supabase.table("transexions").insert({
                "from_user": user_id,
                "to_department": dept_id,
                "doc_id": doc_id
            }).execute()

    finally:
        os.remove(file_location)

    # return {
    #     "document": doc_resp.data,
    #     "filename": file.filename,
    #     "processed": output,
    #     "cloudinary_url": upload_result.get("secure_url")
    # }

    return {
        "document": doc_resp.data,
        "filename": file.filename,
        "processed": "",
        "cloudinary_url": upload_result.get("secure_url")
    }
