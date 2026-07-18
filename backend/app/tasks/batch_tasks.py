"""
Celery Background Tasks — Batch SME Risk Assessment
======================================================
تنفيذ معالجة ملفات CSV الجماعية (Batch) بشكل غير متزامن، خارج دورة حياة
طلب HTTP، لتفادي تجميد الخادم عند معالجة آلاف الصفوف دفعة واحدة.

كل Task هنا يفتح جلسة قاعدة بيانات مستقلة خاصة به (وليس جلسة FastAPI
الخاصة بالطلب)، لأن الـ Celery worker يعمل داخل عملية (process) منفصلة
تمامًا عن عملية الـ API نفسها.
"""

import os
import traceback
from datetime import datetime

from app.core.celery_app import celery_app
from app.db.database import SessionLocal
from app.db.models import BatchAssessmentJob
from app.services.ml_service import ml_service


@celery_app.task(name="app.tasks.process_batch_assessment_task", bind=True)
def process_batch_assessment_task(self, job_id: int, file_path: str):
    """
    يقرأ ملف CSV المرفوع، يمرره لمحرك التعلم الآلي صفًا بصف، ويحفظ نتيجة
    كل صف (درجة المخاطرة، التصنيف، نسبة الثقة) داخل عمود results_json
    لسجل BatchAssessmentJob، مع تحديث حالة المهمة (pending → processing →
    completed/failed) بشكل قابل للاستعلام من الواجهة الأمامية عبر polling.
    """
    db = SessionLocal()
    try:
        job = db.query(BatchAssessmentJob).filter(BatchAssessmentJob.id == job_id).first()
        if not job:
            return {"status": "failed", "error": f"Job {job_id} not found."}

        job.status = "processing"
        job.started_at = datetime.utcnow()
        db.commit()

        with open(file_path, "rb") as f:
            file_content = f.read()

        results = ml_service.process_batch_csv(file_content)

        job.status = "completed"
        job.total_rows = len(results)
        job.processed_rows = len(results)
        job.results_json = results
        job.completed_at = datetime.utcnow()
        db.commit()

        return {"status": "completed", "total_rows": len(results)}

    except Exception as e:
        traceback.print_exc()
        db.rollback()
        job = db.query(BatchAssessmentJob).filter(BatchAssessmentJob.id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(e)[:1000]
            job.completed_at = datetime.utcnow()
            db.commit()
        return {"status": "failed", "error": str(e)}

    finally:
        # تنظيف الملف المؤقت من على القرص بعد المعالجة، سواء نجحت أو فشلت
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass
        db.close()