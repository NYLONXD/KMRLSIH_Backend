from api.app.config import pwd_context

def hash_password(password: str) -> str:
    """Hash password for storage"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify user password"""
    return pwd_context.verify(plain_password, hashed_password)
