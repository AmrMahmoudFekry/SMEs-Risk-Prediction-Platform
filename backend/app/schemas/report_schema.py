
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportBase(BaseModel):
    report_type: str
    assessment_id: int

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    report_type: str
    assessment_id: int
    file_url: str
    created_at: datetime

    class Config:
        from_attributes = True