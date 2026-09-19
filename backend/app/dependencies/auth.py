from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token

# This tells FastAPI to look for the token in the "Authorization" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_investigator(token: str = Depends(oauth2_scheme)):
    """
    Dependency that enforces authentication.
    Inject this into any endpoint that needs protection.
    """
    payload = verify_token(token)
    
    # Extract user info from the token payload (e.g., investigator_id)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
        
    return {"investigator_id": user_id, "role": payload.get("role", "investigator")}