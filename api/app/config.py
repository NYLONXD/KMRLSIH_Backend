# backend/api/app/config.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

# ---- Supabase ----
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    raise RuntimeError("Missing Supabase credentials in environment")

# ---- Cloudinary ----
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

# ---- Password Hashing ----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
