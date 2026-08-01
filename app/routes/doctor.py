from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Doctor
from ..schemas import DoctorCreate, DoctorLogin, DoctorResponse

# ===========================
# ROUTER
# ===========================

router = APIRouter(
    prefix="/doctor",
    tags=["Doctor"]
)

# ===========================
# SECURITY
# ===========================

SECRET_KEY = "medical_assistant_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/doctor/login"
)


# ===========================
# PASSWORD FUNCTIONS
# ===========================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ===========================
# JWT TOKEN
# ===========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    # ===========================
# DOCTOR REGISTRATION
# ===========================

@router.post("/register")
def register_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor already registered with this email."
        )

    # Create new doctor
    new_doctor = Doctor(
        full_name=doctor.full_name,
        email=doctor.email,
        password=hash_password(doctor.password),
        specialization=doctor.specialization,
        experience=doctor.experience,
        qualification=doctor.qualification,
        hospital=doctor.hospital,
        phone=doctor.phone,
        available_days=doctor.available_days,
        available_time=doctor.available_time
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {
        "success": True,
        "message": "Doctor registered successfully.",
        "doctor": {
            "id": new_doctor.id,
            "full_name": new_doctor.full_name,
            "email": new_doctor.email,
            "specialization": new_doctor.specialization
        }
    }
    # ===========================
# DOCTOR LOGIN
# ===========================

@router.post("/login")
def doctor_login(
    doctor: DoctorLogin,
    db: Session = Depends(get_db)
):
    db_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        doctor.password,
        db_doctor.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "doctor_id": db_doctor.id,
            "email": db_doctor.email
        }
    )

    return {
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "doctor": {
            "id": db_doctor.id,
            "full_name": db_doctor.full_name,
            "email": db_doctor.email,
            "specialization": db_doctor.specialization
        }
    }
   # ===========================
# GET CURRENT DOCTOR
# ===========================

def get_current_doctor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        doctor_id = payload.get("doctor_id")

        if doctor_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        raise credentials_exception

    return doctor


# ===========================
# DOCTOR PROFILE
# ===========================

@router.get(
    "/profile",
    response_model=DoctorResponse
)
def doctor_profile(
    current_doctor: Doctor = Depends(get_current_doctor)
):
    return current_doctor 