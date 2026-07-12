from pydantic import BaseModel, Field
from typing import Dict, Any

class AssessmentCreate(BaseModel):
    sme_id: int = Field(..., description="ID of the SME being assessed")
    financials: Dict[str, Any] = Field(..., description="Financial data used by the ML model")

class AssessmentResponse(BaseModel):
    assessment_id: int
    risk_profile: Dict[str, Any]
    ai_insights: str

    class Config:
        orm_mode = True
