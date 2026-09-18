from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class VASPLabelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address: str
    vasp_name: str
    category: str
    chain: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    source: str
    suggested_action: Optional[str] = None