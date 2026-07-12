from sqlalchemy.orm import Session
from typing import Dict, Any
from app.repositories.assessment_repository import AssessmentRepository
from app.services.ml_service import ml_service
from app.services.ai_service import ai_analyzer
from app.db.models import Assessment

class AssessmentService:
    def __init__(self, db: Session):
        self.assessment_repo = AssessmentRepository(db)

    def create_assessment(self, sme_id: int, user_id: int, financials: Dict[str, Any]) -> Dict[str, Any]:
        ml_results = ml_service.predict_risk(financials)
        ai_insights = ai_analyzer.generate_credit_recommendation(
            risk_score=ml_results["risk_score"],
            financials=financials,
        )

        new_assessment = Assessment(
            sme_id=sme_id,
            user_id=user_id,
            risk_score=ml_results["risk_score"],
            risk_category=ml_results["risk_category"],
            confidence=ml_results["confidence"],
            model_version="v1.0",
            features_json=financials,
            shap_values_json={},
            ai_insights=ai_insights,
        )

        saved = self.assessment_repo.create(new_assessment)
        return {
            "assessment_id": saved.id,
            "risk_profile": ml_results,
            "ai_insights": ai_insights,
        }
