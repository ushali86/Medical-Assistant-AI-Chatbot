from pydantic import BaseModel, EmailStr


# ===========================
# USER SCHEMAS
# ===========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


# ===========================
# DOCTOR SCHEMAS
# ===========================

class DoctorCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    specialization: str
    experience: int
    qualification: str
    hospital: str
    phone: str
    available_days: str
    available_time: str


class DoctorLogin(BaseModel):
    email: EmailStr
    password: str


class DoctorResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    specialization: str
    experience: int
    qualification: str
    hospital: str
    phone: str
    available_days: str
    available_time: str

    class Config:
        from_attributes = True


# ===========================
# CHAT SCHEMAS
# ===========================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    success: bool
    user_message: str
    ai_response: str


class ChatHistory(BaseModel):
    id: int
    user_message: str
    ai_response: str

    class Config:
        from_attributes = True