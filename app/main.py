from fastapi import FastAPI, HTTPException, Depends, status

from app.auth import (
    fake_users_db,
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.schemas import UserCreate, UserLogin, UserPublic, Token

app = FastAPI(
    title="Virtual Closet API",
    description="Backend API untuk Virtual Closet",
    version="1.0.0",
)


# GENERAL

@app.get("/", tags=["General"])
def home() -> dict[str, str]:
    return {"message": "Virtual Closet API is running"}


@app.get("/health", tags=["General"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# AUTHENTICATION

@app.post(
    "/auth/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
def register(user: UserCreate):
    email = str(user.email).lower()

    if email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email sudah terdaftar",
        )

    fake_users_db[email] = {
        "email": email,
        "hashed_password": hash_password(user.password),
    }

    return {"email": email}


@app.post(
    "/auth/login",
    response_model=Token,
    tags=["Authentication"],
)
def login(user: UserLogin):
    email = str(user.email).lower()
    stored_user = fake_users_db.get(email)

    if (
        not stored_user
        or not verify_password(
            user.password,
            stored_user["hashed_password"],
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get(
    "/auth/me",
    response_model=UserPublic,
    tags=["Authentication"],
)
def get_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["email"]}
