import os
from fastapi import UploadFile

UPLOAD_DIR = "./temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    """Save uploaded file locally and return file path"""
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    content = await upload_file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path, content

def save_bytes(content: bytes, filename: str) -> str:
    """Save raw bytes (from URL download)"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path

def remove_file(path: str):
    """Delete file if it exists"""
    if os.path.exists(path):
        os.remove(path)
