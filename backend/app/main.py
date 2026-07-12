
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, SessionLocal
from app.db.base import Base
from app.db.models import Role
from app.api.routes import prediction
from app.api.routes import analytics
from app.api.routes import auth, reports

# تهيئة تطبيق FastAPI بمعايير المؤسسات
app = FastAPI(
    title="SME Risk Intelligence Engine",
    description="Enterprise-grade Credit Risk Assessment API for Financial Institutions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد الـ CORS للسماح للـ Frontend (Next.js) بالاتصال بالخادم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# دمج مسارات الـ API (Routers) التي أنشأناها
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Enterprise Reports"])
app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Executive Analytics"]
)
app.include_router(
    prediction.router,
    prefix="/api/v1/assessment",
    tags=["Credit Risk Assessment"]
)

def seed_default_roles():
    db = SessionLocal()
    try:
        default_roles = [
            ("Admin", "System administrator with full access"),
            ("Analyst", "Risk analyst assigned to assessments"),
            ("Manager", "Risk manager with oversight capabilities"),
        ]
        for name, description in default_roles:
            if not db.query(Role).filter(Role.name == name).first():
                db.add(Role(name=name, description=description))
        db.commit()
    finally:
        db.close()


# إنشاء جداول قاعدة البيانات تلقائياً عند أول تشغيل
# في بيئة الإنتاج استخدم Alembic لإدارة المهاجرات
print("Verifying database tables...")
Base.metadata.create_all(bind=engine)
seed_default_roles()

# مسار لفحص حالة الخادم (Health Check) - أساسي في الـ DevOps
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "Operational", 
        "system": "SME Risk API",
        "database": "Connected"
    }