"""
Celery Application Instance
==============================
نقطة الدخول الموحّدة لتشغيل مهام الخلفية (background tasks) بشكل غير
متزامن (asynchronous)، بعيدًا عن دورة حياة طلب HTTP في FastAPI. يُستخدم
هذا الملف من قبل الـ API (لإرسال المهام عبر .delay()) ومن قبل الـ worker
process نفسه (لاستقبال وتنفيذ المهام).
"""

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "sme_risk_platform",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=60 * 60 * 24,  # الاحتفاظ بنتيجة المهمة 24 ساعة
    worker_prefetch_multiplier=1,  # توزيع عادل للمهام بين عدة workers
)

# اكتشاف تلقائي لكل الـ tasks المعرّفة داخل app/tasks/
celery_app.autodiscover_tasks(["app.tasks"])