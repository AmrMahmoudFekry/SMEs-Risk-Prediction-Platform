import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import io
import traceback
from app.core.config import settings

# ضروري: يجب استيراد هذا الكلاس صراحةً عشان joblib/pickle يقدر يوصل لنفس
# الـ module path اللي اتحفظ بيه النموذج وقت التدريب (train_pipeline.py)
from app.ml.feature_engineering import SMEFeatureEngineer, TRAINING_COLUMN_ORDER  # noqa: F401


class EnterpriseMLService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnterpriseMLService, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        """تحميل نموذج الـ pipeline المدرّب (feat_eng + preprocessor + classifier)."""
        if self._model is None:
            try:
                print(f"Loading ML Pipeline from {settings.MODEL_PATH}...")
                self._model = joblib.load(settings.MODEL_PATH)
                print("Model loaded successfully.")
            except FileNotFoundError:
                print(
                    f"Model file not found at {settings.MODEL_PATH}. "
                    "Run `python -m app.ml.train_pipeline` first."
                )
                self._model = None
            except Exception as e:
                print(f"Error loading model: {e}")
                self._model = None
        return self._model

    def calculate_confidence(self, probabilities: np.ndarray) -> float:
        """حساب نسبة الثقة في التوقع بناءً على الاحتمالات."""
        max_prob = np.max(probabilities)
        return round(float(max_prob * 100), 2)

    def _categorize(self, risk_score: float) -> str:
        if risk_score >= 70:
            return "High Risk"
        elif risk_score >= 40:
            return "Medium Risk"
        return "Low Risk"

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """التحقق من الأعمدة المطلوبة وإعادة ترتيبها لتطابق ترتيب التدريب."""
        missing = [c for c in TRAINING_COLUMN_ORDER if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required model input features: {', '.join(missing)}")
        return df[TRAINING_COLUMN_ORDER].copy()

    def predict_risk(self, sme_data: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة التقييم الفردي (Single Prediction)."""
        model = self.load_model()
        if not model:
            raise RuntimeError("Machine Learning model is not available.")

        try:
            df_input = pd.DataFrame([sme_data])
            df_input = self._prepare_dataframe(df_input)

            probabilities = model.predict_proba(df_input)[0]
            risk_score = round(float(probabilities[1] * 100), 2)
            confidence = self.calculate_confidence(probabilities)
            category = self._categorize(risk_score)

            return {
                "risk_score": risk_score,
                "risk_category": category,
                "confidence": confidence,
                "features_used": sme_data,
            }
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Error during prediction: {str(e)}")

    def process_batch_csv(self, file_content: bytes) -> List[Dict[str, Any]]:
        """معالجة التقييم المجمع من ملف CSV."""
        model = self.load_model()
        if not model:
            raise RuntimeError("Machine Learning model is not available.")

        try:
            df = pd.read_csv(io.BytesIO(file_content))
            df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
            df = self._prepare_dataframe(df)

            probabilities_batch = model.predict_proba(df)

            results = []
            for i, probs in enumerate(probabilities_batch):
                risk_score = round(float(probs[1] * 100), 2)
                confidence = self.calculate_confidence(probs)
                category = self._categorize(risk_score)

                results.append(
                    {
                        "row_index": i + 1,
                        "risk_score": risk_score,
                        "risk_category": category,
                        "confidence": confidence,
                    }
                )

            return results
        except ValueError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ValueError(f"Error processing batch file: {str(e)}")


ml_service = EnterpriseMLService()