
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Assessment, Report
from app.services.pdf_service import report_generator
from app.api.dependencies import get_current_user
from sqlalchemy import desc

router = APIRouter()

@router.get("/history")
async def get_assessments_history(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """جلب سجل التقييمات لصفحة التقارير في الواجهة"""
    assessments = db.query(Assessment).order_by(desc(Assessment.created_at)).limit(50).all()
    
    result = []
    for acc in assessments:
        sme_name = acc.features_json.get("legal_name", f"SME ID: {acc.sme_id}") if isinstance(acc.features_json, dict) else "Unknown"
        
        result.append({
            "id": f"RI-{acc.created_at.strftime('%Y%m%d')}-{acc.id}",
            "db_id": acc.id,
            "smeName": sme_name,
            "date": acc.created_at.strftime('%Y-%m-%d %H:%M'),
            "risk": acc.risk_category,
            "score": acc.risk_score,
            "status": "Completed"
        })
    return result

@router.post("/generate/{assessment_id}")
async def generate_report(assessment_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    filepath = report_generator.generate_credit_report(assessment)
    
    new_report = Report(
        assessment_id=assessment.id,
        report_type="Credit Assessment",
        title=f"Credit Report for SME {assessment.sme_id}",
        description="Generated enterprise credit assessment report.",
        status="generated",
        file_url=filepath,
        created_by=current_user.id,
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    download_url = f"/api/v1/reports/download/{new_report.id}"
    return {
        "status": "success",
        "message": "Report generated",
        "report_id": new_report.id,
        "download_url": download_url
    }

@router.get("/download/{report_id}")
async def download_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report or not report.file_url:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return FileResponse(path=report.file_url, filename=report.file_url.split("/")[-1], media_type='application/pdf')