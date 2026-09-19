from pydantic import BaseModel

class CaseCreateRequest(BaseModel):
    reported_wallet: str