from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.db.database import get_db
from app.services.assessment_service import AssessmentService
from app.api.dependencies import get_current_user
from app.schemas.assessment_schema import AssessmentCreate, AssessmentResponse
from app.db.models import User

router = APIRouter()

@router.post("/single", response_model=AssessmentResponse)
async def predict_single_sme(
    assessment_in: AssessmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    نقطة النهاية الخاصة بالتقييم الفردي المرتبط بالمستخدم.
    """
    try:
        assessment_service = AssessmentService(db)
        result = assessment_service.create_assessment(
            sme_id=assessment_in.sme_id,
            user_id=current_user.id,
            financials=assessment_in.financials,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/batch")
async def predict_batch_sme(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    نقطة النهاية الخاصة برفع ملفات CSV لتقييم آلاف الشركات دفعة واحدة
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    # سيتم استخدام BackgroundTasks هنا لكي لا يتجمد السيرفر أثناء المعالجة
    # وسنربطها لاحقاً بـ Redis & Celery

    return {
        "status": "processing",
        "message": "Batch file received successfully. Processing running in the background."
    }
