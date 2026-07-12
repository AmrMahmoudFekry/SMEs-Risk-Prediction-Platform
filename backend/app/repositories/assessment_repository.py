from sqlalchemy.orm import Session
from app.db.models import Assessment

class AssessmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, assessment: Assessment) -> Assessment:
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def get_by_id(self, assessment_id: int) -> Assessment | None:
        return self.db.query(Assessment).filter(Assessment.id == assessment_id).first()

    def list_recent(self, limit: int = 50):
        return self.db.query(Assessment).order_by(Assessment.created_at.desc()).limit(limit).all()
