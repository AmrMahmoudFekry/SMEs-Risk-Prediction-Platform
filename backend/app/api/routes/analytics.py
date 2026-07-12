
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.db.models import Assessment
from app.schemas.sme_schema import DashboardStats

router = APIRouter()

@router.get("/dashboard-stats", response_model=DashboardStats)
async def get_executive_dashboard_stats(db: Session = Depends(get_db)):
    """جلب إحصائيات المحفظة الائتمانية بالكامل لعرضها للمديرين"""
    
    total_assessments = db.query(Assessment).count()
    
    high_risk = db.query(Assessment).filter(Assessment.risk_category == "High Risk").count()
    medium_risk = db.query(Assessment).filter(Assessment.risk_category == "Medium Risk").count()
    low_risk = db.query(Assessment).filter(Assessment.risk_category == "Low Risk").count()
    
    avg_conf = db.query(func.avg(Assessment.confidence)).scalar() or 0.0

    return DashboardStats(
        total_smes=total_assessments,
        high_risk_count=high_risk,
        medium_risk_count=medium_risk,
        low_risk_count=low_risk,
        average_confidence=round(avg_conf, 2)
    )

@router.get("/risk-trend")
async def get_risk_trend_over_time(db: Session = Depends(get_db)):
    """جلب بيانات اتجاه المخاطر الزمنية لتغذية رسم الـ Trend Line"""
    # استعلام متقدم لتجميع التقييمات حسب الشهر (يتم تنفيذه عبر MySQL)
    # Use PostgreSQL-friendly month truncation
    trends = db.query(
        func.to_char(func.date_trunc('month', Assessment.created_at), 'YYYY-MM').label('month'),
        Assessment.risk_category,
        func.count(Assessment.id).label('count')
    ).group_by(func.date_trunc('month', Assessment.created_at), Assessment.risk_category).all()
    
    # تنسيق البيانات لتناسب Apache ECharts
    result = {}
    for month, category, count in trends:
        if month not in result:
            result[month] = {"High Risk": 0, "Medium Risk": 0, "Low Risk": 0}
        result[month][category] = count
        
    return result