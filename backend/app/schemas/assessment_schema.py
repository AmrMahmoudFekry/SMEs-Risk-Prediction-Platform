from pydantic import BaseModel, Field
from typing import Dict, Any, List


class AssessmentCreate(BaseModel):
    sme_id: int = Field(..., description="ID of the SME being assessed")
    financials: Dict[str, Any] = Field(
        ..., description="Financial data used by the ML model"
    )
    lang: str = Field(
        default="en", description="Language for recommendations: 'en' or 'ar'"
    )


class SHAPContribution(BaseModel):
    feature: str
    shap_value: float
    direction: str


class Recommendation(BaseModel):
    title: str
    description: str
    priority: str


class RiskProfile(BaseModel):
    risk_score: float
    risk_category: str
    confidence: float
    features_used: Dict[str, Any]


class AssessmentResponse(BaseModel):
    assessment_id: int
    risk_profile: RiskProfile
    shap_contributions: List[SHAPContribution]
    recommendations: List[Recommendation]
    ai_insights: str

    class Config:
        orm_mode = True