from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SMECreate(BaseModel):
    """بيانات إنشاء منشأة (SME) جديدة"""
    legal_name: str = Field(..., min_length=2, max_length=255, description="Legal name of the SME")
    industry: Optional[str] = Field(None, description="Industry sector")
    business_age_months: Optional[int] = Field(None, ge=0, description="Business operating age in months")
    ownership_type: Optional[str] = Field(None, description="Ownership structure (e.g. Sole Proprietorship, LLC)")
    registration_date: Optional[datetime] = None


class SMEUpdate(BaseModel):
    """بيانات تحديث منشأة قائمة (كل الحقول اختيارية)"""
    legal_name: Optional[str] = Field(None, min_length=2, max_length=255)
    industry: Optional[str] = None
    business_age_months: Optional[int] = Field(None, ge=0)
    ownership_type: Optional[str] = None
    registration_date: Optional[datetime] = None
    status: Optional[str] = Field(None, description="active | inactive | archived")


class SMEOut(BaseModel):
    id: int
    organization_id: int
    legal_name: str
    industry: Optional[str] = None
    business_age_months: Optional[int] = None
    ownership_type: Optional[str] = None
    registration_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SMEListResponse(BaseModel):
    items: List[SMEOut]
    total: int
    skip: int
    limit: int


class LatestAssessmentSummary(BaseModel):
    assessment_id: int
    risk_score: float
    risk_category: str
    confidence: float
    created_at: datetime

    class Config:
        orm_mode = True


class SMEDetailResponse(BaseModel):
    sme: SMEOut
    latest_assessment: Optional[LatestAssessmentSummary] = None


class DashboardStats(BaseModel):
    """إحصائيات لوحة القيادة"""
    total_smes: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    average_confidence: float