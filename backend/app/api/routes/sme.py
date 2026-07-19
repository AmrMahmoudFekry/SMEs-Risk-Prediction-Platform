from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.db.models import User
from app.services.sme_service import SMEService
from app.core.exceptions import SMENotFoundError, SMEAccessDeniedError
from app.schemas.sme_schema import (
    SMECreate,
    SMEUpdate,
    SMEOut,
    SMEListResponse,
    SMEDetailResponse,
    LatestAssessmentSummary,
)

router = APIRouter()


@router.post("/", response_model=SMEOut, status_code=201)
async def create_sme(
    sme_in: SMECreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """إنشاء منشأة (SME) جديدة داخل مؤسسة المستخدم الحالي."""
    service = SMEService(db)
    return service.create_sme(sme_in, current_user.organization_id)


@router.get("/", response_model=SMEListResponse)
async def list_smes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="Filter by legal name (partial match)"),
    industry: Optional[str] = Query(None, description="Filter by industry sector"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """قائمة كل المنشآت التابعة لمؤسسة المستخدم الحالي فقط (tenant isolation)."""
    service = SMEService(db)
    items, total = service.list_smes(current_user.organization_id, skip, limit, search, industry)
    return SMEListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{sme_id}", response_model=SMEDetailResponse)
async def get_sme(
    sme_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """تفاصيل منشأة واحدة مع ملخص آخر تقييم مخاطرة (إن وُجد)."""
    service = SMEService(db)
    try:
        sme, latest = service.get_sme_with_latest_assessment(sme_id, current_user.organization_id)
    except SMENotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SMEAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))

    latest_summary = None
    if latest:
        latest_summary = LatestAssessmentSummary(
            assessment_id=latest.id,
            risk_score=latest.risk_score,
            risk_category=latest.risk_category,
            confidence=latest.confidence,
            created_at=latest.created_at,
        )

    return SMEDetailResponse(sme=sme, latest_assessment=latest_summary)


@router.put("/{sme_id}", response_model=SMEOut)
async def update_sme(
    sme_id: int,
    sme_in: SMEUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """تحديث بيانات منشأة قائمة (كل الحقول اختيارية)."""
    service = SMEService(db)
    try:
        return service.update_sme(sme_id, current_user.organization_id, sme_in)
    except SMENotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SMEAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{sme_id}", status_code=204)
async def delete_sme(
    sme_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """حذف منشأة، بعد تأكيد صريح من الواجهة الأمامية قبل الاستدعاء."""
    service = SMEService(db)
    try:
        service.delete_sme(sme_id, current_user.organization_id)
    except SMENotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SMEAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return None