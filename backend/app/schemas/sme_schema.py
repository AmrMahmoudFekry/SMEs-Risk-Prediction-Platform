
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class SMEDataInput(BaseModel):
    """البيانات المطلوبة لتقييم الشركة"""
    legal_name: str = Field(..., description="Legal name of the SME")
    industry: str = Field(..., description="Industry sector")
    financials: Dict[str, float] = Field(..., description="Financial metrics matching the ML model features")

class AssessmentResponse(BaseModel):
    """شكل الاستجابة (Response) التي ستعود للواجهة الأمامية"""
    status: str
    assessment_id: int
    risk_score: float
    category: str
    confidence: float
    ai_insights: str

class DashboardStats(BaseModel):
    """إحصائيات لوحة القيادة"""
    total_smes: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    average_confidence: float