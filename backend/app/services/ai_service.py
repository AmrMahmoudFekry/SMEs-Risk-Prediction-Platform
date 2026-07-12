# backend/app/services/ai_service.py

import google.generativeai as genai
from typing import Dict, Any
from app.core.config import settings
import traceback

class FinancialAIAnalyzer:
    def __init__(self):
        """تهيئة الاتصال بنموذج Gemini"""
        self.api_key = settings.GEMINI_API_KEY
        self.is_configured = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.is_configured = True
            except Exception as e:
                print(f"Failed to configure Gemini API: {e}")
        else:
            print("Warning: GEMINI_API_KEY is missing in environment variables.")

    def generate_credit_recommendation(self, risk_score: float, financials: Dict[str, Any]) -> str:
        """
        توليد تحليل مالي دقيق وتوصية ائتمانية.
        تمت صياغة الـ Prompt للحصول على رد بنكي احترافي.
        """
        if not self.is_configured or not hasattr(self, 'model'):
            return "AI Analysis unavailable: API configuration missing or invalid."

        prompt = f"""
        Act as a strict Senior Credit Risk Officer at an enterprise bank.
        Analyze the following SME profile and provide a highly concise, data-driven credit recommendation.
        Do NOT include generic greetings or executive summaries.

        [Data]
        - AI Calculated Risk Score: {risk_score}% (Where >70% is High Risk, <40% is Low Risk)
        - SME Financial Metrics: {financials}

        [Output Requirements]
        Provide exactly two sections:
        1. Key Risk Drivers: Bullet points explaining which financial metrics are driving the risk score.
        2. Final Recommendation: State clearly "Approve", "Reject", or "Conditional Approval", followed by a one-sentence justification.
        """
        
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            return "AI Analysis completed but returned no insights."
        except Exception as e:
            traceback.print_exc()
            return f"Error communicating with AI service: {str(e)}"

# إنشاء نسخة (Instance) جاهزة للاستخدام في مسارات الـ API
ai_analyzer = FinancialAIAnalyzer()