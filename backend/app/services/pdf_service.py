# backend/app/services/pdf_service.py

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.db.models import Assessment

class EnterpriseReportGenerator:
    def __init__(self):
        self.reports_dir = "reports_storage"
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_credit_report(self, assessment: Assessment) -> str:
        """توليد تقرير PDF رسمي بناءً على بيانات التقييم"""
        filename = f"Credit_Report_SME_{assessment.sme_id}_{datetime.now().strftime('%Y%md%H%M')}.pdf"
        filepath = os.path.abspath(os.path.join(self.reports_dir, filename))
        
        c = canvas.Canvas(filepath, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Enterprise Credit Risk Assessment Report")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Date: {assessment.created_at.strftime('%Y-%m-%d')}")
        c.drawString(50, 700, f"Assessment ID: {assessment.id}")
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 660, "Financial Risk Metrics")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 630, f"Risk Score: {assessment.risk_score}%")
        c.drawString(50, 610, f"Category: {assessment.risk_category}")
        c.drawString(50, 590, f"AI Confidence: {assessment.confidence}%")
        
        c.save()
        return filepath

report_generator = EnterpriseReportGenerator()