from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime


class BatchJobCreatedResponse(BaseModel):
    job_id: int
    status: str
    filename: str
    message: str


class BatchJobStatusResponse(BaseModel):
    job_id: int
    status: str
    filename: str
    total_rows: Optional[int] = None
    processed_rows: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class BatchJobResultsResponse(BaseModel):
    job_id: int
    status: str
    results: List[Dict[str, Any]] = []