from sqlalchemy.orm import Session
from typing import Dict, Any

from app.repositories.assessment_repository import AssessmentRepository
from app.services.ml_service import ml_service
from app.services.ai_service import ai_analyzer
from app.services.recommendation_service import generate_recommendations
from app.services.shap_service import shap_explainer_service
from app.db.models import Assessment, Prediction, SME
from app.core.exceptions import SMENotFoundError, SMEAccessDeniedError


class AssessmentService:
    def __init__(self, db: Session):
        self.db = db
        self.assessment_repo = AssessmentRepository(db)

    def _validate_sme_ownership(self, sme_id: int, organization_id: int) -> SME:
        """
        التحقق من أن المنشأة (SME) المطلوب تقييمها تابعة فعليًا لنفس مؤسسة
        المستخدم الحالي. هذا الفحص أساسي لعزل البيانات بين المستأجرين
        (tenant isolation) في بيئة multi-tenant، ولمنع ثغرات IDOR.
        """
        sme = self.db.query(SME).filter(SME.id == sme_id).first()
        if not sme:
            raise SMENotFoundError(f"SME with id {sme_id} was not found.")
        if sme.organization_id != organization_id:
            raise SMEAccessDeniedError(
                "The requested SME does not belong to your organization."
            )
        return sme

    def create_assessment(
        self,
        sme_id: int,
        user_id: int,
        organization_id: int,
        financials: Dict[str, Any],
        lang: str = "en",
    ) -> Dict[str, Any]:
        # 1. Tenant isolation check — يجب أن يمر قبل أي معالجة أخرى
        self._validate_sme_ownership(sme_id, organization_id)

        # 2. ML Prediction
        ml_results = ml_service.predict_risk(financials)

        # 3. Rule-based deterministic recommendations (auditable، بدون أي
        #    تدخل من الذكاء الاصطناعي التوليدي)
        recommendations = generate_recommendations(
            financials=financials,
            risk_score=ml_results["risk_score"],
            lang=lang,
        )

        # 4. SHAP explainability — تفسير مستوى الخاصية للقرار
        try:
            shap_contributions = shap_explainer_service.explain_single(financials)
        except Exception:
            # لا نُفشل التقييم بالكامل لو تفسير SHAP فشل لأي سبب تقني؛
            # التقييم الائتماني نفسه أهم من التفسير الإضافي.
            shap_contributions = []

        # 5. سرد استشاري تكميلي مبني على الذكاء الاصطناعي التوليدي (Gemini)
        #    لا يحل محل القرار الحتمي أعلاه بأي شكل، بل يفسّره بلغة طبيعية.
        ai_insights = ai_analyzer.generate_credit_recommendation(
            risk_score=ml_results["risk_score"],
            financials=financials,
        )

        # 6. حفظ التقييم في جدول Assessment
        new_assessment = Assessment(
            sme_id=sme_id,
            user_id=user_id,
            risk_score=ml_results["risk_score"],
            risk_category=ml_results["risk_category"],
            confidence=ml_results["confidence"],
            model_version="v1.0",
            features_json=financials,
            shap_values_json=shap_contributions,
            recommendations_json=recommendations,
            ai_insights=ai_insights,
        )
        saved = self.assessment_repo.create(new_assessment)

        # 7. حفظ سجل تدقيق منفصل في جدول Prediction — سجل غير قابل للتعديل
        #    لكل استدعاء فعلي للنموذج (مطلوب لأغراض المراجعة والامتثال
        #    البنكي، مستقل عن جدول Assessment).
        audit_prediction = Prediction(
            assessment_id=saved.id,
            model_version="v1.0",
            probability=ml_results["risk_score"] / 100.0,
            category=ml_results["risk_category"],
            input_payload=financials,
            output_payload=ml_results,
        )
        self.db.add(audit_prediction)
        self.db.commit()

        return {
            "assessment_id": saved.id,
            "risk_profile": ml_results,
            "shap_contributions": shap_contributions,
            "recommendations": recommendations,
            "ai_insights": ai_insights,
        }