from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id: str
    password: str

class URLRequest(BaseModel):
    user_id: str
    url: str
    dept_name: str
    priority: str

class VIEWRequest(BaseModel):
    user_id: str
    doc_id: str

class SUMMARYRequest(BaseModel):
    doc_id: str

class HISTORYRequest(BaseModel):
    user_id: str

class TransactionRequest(BaseModel):
    from_user: str
    to_department: str
    doc_id: str
    timestamp: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    department: str
    role: str
    phone: str

class ListDocsRequest(BaseModel):
    user_id: str

class compliancesRequest(BaseModel):
    doc_id: str

class changeNameRequest(BaseModel):
    user_id: str
    name: str

class changeEmailRequest(BaseModel):
    user_id: str
    email: str

class changePhoneRequest(BaseModel):
    user_id: str
    phone: str

class changeDepartmentRequest(BaseModel):
    user_id: str
    dept_name: str

class searchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    doc_id: str
    chunk_id: str
    summary: str | None
    sentences: list[str] | None
    score: float