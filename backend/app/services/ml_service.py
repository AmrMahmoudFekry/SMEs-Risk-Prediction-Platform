
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import io
import traceback
from app.core.config import settings

class EnterpriseMLService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnterpriseMLService, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        """تحميل نموذج HistGradientBoostingClassifier في الذاكرة"""
        if self._model is None:
            try:
                print(f"Loading ML Pipeline from {settings.MODEL_PATH}...")
                self._model = joblib.load(settings.MODEL_PATH)
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {e}")
                self._model = None
        return self._model

    def calculate_confidence(self, probabilities: np.ndarray) -> float:
        """حساب نسبة الثقة في التوقع بناءً على الاحتمالات"""
        max_prob = np.max(probabilities)
        return round(float(max_prob * 100), 2)

    def predict_risk(self, sme_data: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة التقييم الفردي (Single Prediction)"""
        model = self.load_model()
        if not model:
            raise RuntimeError("Machine Learning model is not available.")

        try:
            # تحويل البيانات إلى DataFrame لتطابق مدخلات التدريب
            df_input = pd.DataFrame([sme_data])
            
            # استخراج الاحتماليات (افتراض أن المؤشر 1 يعبر عن خطر التعثر)
            probabilities = model.predict_proba(df_input)[0]
            risk_score = round(float(probabilities[1] * 100), 2)
            confidence = self.calculate_confidence(probabilities)
            
            # تحديد الفئة بناءً على معايير صارمة
            if risk_score >= 70:
                category = "High Risk"
            elif risk_score >= 40:
                category = "Medium Risk"
            else:
                category = "Low Risk"

            return {
                "risk_score": risk_score,
                "risk_category": category,
                "confidence": confidence,
                "features_used": sme_data
            }
        except Exception as e:
            raise ValueError(f"Error during prediction: {str(e)}")

    def process_batch_csv(self, file_content: bytes) -> List[Dict[str, Any]]:
        """معالجة التقييم المجمع من ملف CSV في الخلفية"""
        model = self.load_model()
        if not model:
            raise RuntimeError("Machine Learning model is not available.")

        try:
            # قراءة ملف الـ CSV
            df = pd.read_csv(io.BytesIO(file_content))
            
            # يمكنك إضافة كود هنا للتحقق من أسماء الأعمدة (Validation)
            
            # إجراء التوقعات لكل الصفوف دفعة واحدة
            probabilities_batch = model.predict_proba(df)
            
            results = []
            for i, probs in enumerate(probabilities_batch):
                risk_score = round(float(probs[1] * 100), 2)
                confidence = self.calculate_confidence(probs)
                
                category = "High Risk" if risk_score >= 70 else ("Medium Risk" if risk_score >= 40 else "Low Risk")
                
                results.append({
                    "row_index": i + 1,
                    "risk_score": risk_score,
                    "risk_category": category,
                    "confidence": confidence
                })
                
            return results
        except Exception as e:
            traceback.print_exc()
            raise ValueError(f"Error processing batch file: {str(e)}")

# إنشاء نسخة (Instance) جاهزة للاستخدام في مسارات الـ API
ml_service = EnterpriseMLService()