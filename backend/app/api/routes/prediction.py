import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.assessment_service import AssessmentService
from app.api.dependencies import get_current_user
from app.schemas.assessment_schema import AssessmentCreate, AssessmentResponse
from app.schemas.batch_schema import (
    BatchJobCreatedResponse,
    BatchJobStatusResponse,
    BatchJobResultsResponse,
)
from app.core.exceptions import SMENotFoundError, SMEAccessDeniedError
from app.db.models import User, BatchAssessmentJob
from app.tasks.batch_tasks import process_batch_assessment_task

router = APIRouter()

BATCH_UPLOAD_DIR = os.path.join(os.getcwd(), "storage", "batch_uploads")
MAX_BATCH_FILE_SIZE_BYTES = 20 * 1024 * 1024  # حد أقصى 20 ميجابايت لملف CSV الدفعي


@router.post("/single", response_model=AssessmentResponse)
async def predict_single_sme(
    assessment_in: AssessmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    نقطة النهاية الخاصة بالتقييم الفردي، مرتبطة بالمستخدم الحالي ومؤسسته.
    يتضمن الرد: درجة المخاطرة، تفسير SHAP، توصيات حتمية، وسرد استشاري
    مبني على الذكاء الاصطناعي التوليدي.
    """
    try:
        assessment_service = AssessmentService(db)
        result = assessment_service.create_assessment(
            sme_id=assessment_in.sme_id,
            user_id=current_user.id,
            organization_id=current_user.organization_id,
            financials=assessment_in.financials,
            lang=assessment_in.lang,
        )
        return result
    except SMENotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SMEAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/batch", response_model=BatchJobCreatedResponse, status_code=202)
async def submit_batch_assessment(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    استقبال ملف CSV لتقييم عدد كبير من الشركات دفعة واحدة. المعالجة الفعلية
    تتم بشكل غير متزامن (asynchronous) عبر Celery worker منفصل تمامًا عن
    عملية الـ API، لتفادي تجميد الخادم في حال كان الملف يحتوي على آلاف
    الصفوف. الـ endpoint يرجّع فورًا برقم مهمة (job_id) يُستخدم لمتابعة
    التقدم واسترجاع النتائج لاحقًا عبر /batch/{job_id}/status و
    /batch/{job_id}/results.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_content = await file.read()

    if len(file_content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(file_content) > MAX_BATCH_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 20MB size limit.")

    os.makedirs(BATCH_UPLOAD_DIR, exist_ok=True)
    stored_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(BATCH_UPLOAD_DIR, stored_filename)

    with open(file_path, "wb") as f:
        f.write(file_content)

    job = BatchAssessmentJob(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        filename=file.filename,
        status="pending",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    process_batch_assessment_task.delay(job.id, file_path)

    return BatchJobCreatedResponse(
        job_id=job.id,
        status=job.status,
        filename=job.filename,
        message="Batch file received successfully. Processing started in the background.",
    )


@router.get("/batch/{job_id}/status", response_model=BatchJobStatusResponse)
async def get_batch_job_status(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """يُستخدم من الواجهة الأمامية عبر polling دوري لمتابعة تقدم المهمة."""
    job = _get_owned_batch_job(job_id, current_user, db)
    return BatchJobStatusResponse(
        job_id=job.id,
        status=job.status,
        filename=job.filename,
        total_rows=job.total_rows,
        processed_rows=job.processed_rows,
        error_message=job.error_message,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
    )


@router.get("/batch/{job_id}/results", response_model=BatchJobResultsResponse)
async def get_batch_job_results(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """يُرجع النتائج النهائية فقط بعد اكتمال المهمة."""
    job = _get_owned_batch_job(job_id, current_user, db)
    if job.status != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Job is not completed yet (current status: {job.status}).",
        )
    return BatchJobResultsResponse(job_id=job.id, status=job.status, results=job.results_json or [])


def _get_owned_batch_job(job_id: int, current_user: User, db: Session) -> BatchAssessmentJob:
    """
    تحقق من عزل البيانات بين المستأجرين (tenant isolation) بنفس منطق
    الحماية المطبّق في /assessment/single، لمنع أي مستخدم من الاطلاع على
    مهام دفعية تابعة لمؤسسة أخرى.
    """
    job = db.query(BatchAssessmentJob).filter(BatchAssessmentJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Batch job not found.")
    if job.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="This batch job does not belong to your organization.")
    return job