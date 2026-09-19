from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token

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
    access_token = create_access_token(
        data={"sub": form_data.username, "role": "lead_investigator"}
    )
    
    # FastAPI expects this exact JSON structure for OAuth2 logins
    return {"access_token": access_token, "token_type": "bearer"}