import os
from pathlib import Path
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / '.env')

class Settings:
    PROJECT_NAME: str = "SME Risk Intelligence Platform"
    VERSION: str = "1.0.0"

    # إعدادات قاعدة البيانات
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/sme_risk_db"
    )

    # إعدادات Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # إعدادات الأمان والتشفير (JWT)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-dev")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # مسار نموذج الذكاء الاصطناعي (الناتج من app/ml/train_pipeline.py)
    MODEL_PATH: str = os.getenv("MODEL_PATH", "pipeline.pkl")

    # مفتاح ونموذج Gemini AI
    # ملاحظة: تحقق دائمًا من اسم الموديل الحالي في وثائق Google قبل الإنتاج.
    # كانت هذه القيمة قبل الإصلاح: os.getenv("gemini-3.1-flash-lite", "")
    # وهو خطأ لأن الوسيط الأول لـ os.getenv() يجب أن يكون اسم متغير البيئة
    # (GEMINI_API_KEY) وليس اسم الموديل نفسه، مما كان يجعل المفتاح فارغًا
    # دائمًا بصمت حتى لو تم تمريره بشكل صحيح في docker-compose.yml.
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-3.1-flash-lite")

    # التحكم في إنشاء الجداول تلقائيًا (create_all) — يُفضّل تعطيله في
    # الإنتاج والاعتماد كليًا على Alembic migrations لضمان schema versioning
    # آمن وقابل للتراجع (rollback) في بيئة بنكية.
    AUTO_CREATE_TABLES: bool = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"

# إنشاء نسخة عالمية (Singleton) للإعدادات
settings = Settings()