from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Temporary seed users for initial development/testing
MOCK_USERS = {
    "lead_investigator": {"role": "Investigator", "password": "password123"},
    "lead_supervisor": {"role": "Supervisor", "password": "password123"},
    "admin_user": {"role": "Admin", "password": "password123"},
}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": form_data.username, "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}