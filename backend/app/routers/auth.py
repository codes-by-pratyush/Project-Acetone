from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Mock user database check. Once M4 builds a Users table, query it here.
    if form_data.username != "admin" or form_data.password != "secret":
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate the JWT token containing the user's ID and role
    user_role = "lead_investigator"
    access_token = create_access_token(
        data={"sub": form_data.username, "role": user_role}
    )
    
    # FastAPI expects this exact JSON structure for OAuth2 logins
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": user_role
    }