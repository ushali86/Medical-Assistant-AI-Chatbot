from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt

from ..database import get_db
from ..models import User
from ..schemas import UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ===========================
# JWT CONFIG
# ===========================

SECRET_KEY = "medassist_secret_key_2026"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ===========================
# PASSWORD HASHING
# ===========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ===========================
# CREATE TOKEN
# ===========================

def create_access_token(data: dict):

    data_copy = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=24
    )

    data_copy.update({
        "exp": expire
    })

    return jwt.encode(
        data_copy,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ===========================
# VERIFY TOKEN
# ===========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


# ===========================
# REGISTER
# ===========================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(
            user.password
        )
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {

        "message": "Registration Successful",

        "user": {

            "id": new_user.id,

            "name": new_user.name,

            "email": new_user.email

        }

    }



# ===========================
# LOGIN FOR SWAGGER JWT
# ===========================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()


    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )


    if not verify_password(
        form_data.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )


    token = create_access_token({

        "user_id": db_user.id,

        "email": db_user.email

    })


    return {

        "access_token": token,

        "token_type": "bearer"

    }