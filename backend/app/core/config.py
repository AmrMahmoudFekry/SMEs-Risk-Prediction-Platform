
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
    
    # مسار نموذج الذكاء الاصطناعي
    MODEL_PATH: str = os.getenv("MODEL_PATH", "pipeline.pkl")
    
    # مفتاح Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# إنشاء نسخة عالمية (Singleton) للإعدادات
settings = Settings()