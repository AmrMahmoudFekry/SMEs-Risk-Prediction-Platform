"""
SHAP Explainability Service
=============================
يوفر شفافية على مستوى كل خاصية (feature-level) لقرار النموذج، وهو مطلب
أساسي للامتثال البنكي (Model Risk Management / SR 11-7 وما شابه) حيث لا
يُقبل اتخاذ قرار ائتماني بناءً على "صندوق أسود" بدون تفسير قابل للمراجعة.

يعمل هذا السيرفس مباشرة على المُقدِّر (estimator) الأساسي داخل الـ pipeline
المدرَّب، متجاوزًا طبقة الـ CalibratedClassifierCV عند الحاجة، لأن SHAP
TreeExplainer يتطلب الوصول المباشر لنموذج الأشجار (tree-based model).
"""

from typing import Dict, Any, List

import pandas as pd
import shap

from app.services.ml_service import ml_service


class SHAPExplainerService:
    _explainer = None

    def _get_explainer(self):
        """
        بناء (وتخزين مؤقت) الـ SHAP TreeExplainer الخاص بالمُقدِّر الأساسي.
        يتم استخراج المُقدِّر الأساسي من داخل CalibratedClassifierCV إذا كان
        النموذج معايرًا (calibrated)، وإلا يُستخدم المُصنِّف مباشرة.
        """
        if self._explainer is None:
            model = ml_service.load_model()
            if model is None:
                raise RuntimeError("Machine Learning model is not available.")

            classifier = model.named_steps["classifier"]
            if hasattr(classifier, "calibrated_classifiers_"):
                estimator = classifier.calibrated_classifiers_[0].estimator
            else:
                estimator = getattr(classifier, "base_estimator", classifier)

            self._explainer = shap.TreeExplainer(estimator)

        return self._explainer

    def explain_single(self, sme_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        يُرجع أعلى 10 خصائص تأثيرًا على قرار التنبؤ لصف واحد، مرتبة تنازليًا
        حسب القيمة المطلقة لتأثير SHAP، مع اتجاه التأثير (يزيد/يقلل المخاطرة).
        """
        model = ml_service.load_model()
        if model is None:
            raise RuntimeError("Machine Learning model is not available.")

        df_input = pd.DataFrame([sme_data])
        df_input = ml_service.prepare_dataframe(df_input)

        feat_eng = model.named_steps["feat_eng"]
        preprocessor = model.named_steps["preprocessor"]

        prepared = feat_eng.transform(df_input)
        feature_names = list(prepared.columns)
        processed = preprocessor.transform(prepared)

        explainer = self._get_explainer()
        shap_values = explainer.shap_values(processed)

        if isinstance(shap_values, list):
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

        row_shap = shap_values[0]

        contributions = [
            {
                "feature": feature_names[i],
                "shap_value": round(float(row_shap[i]), 5),
                "direction": "increases_risk" if row_shap[i] > 0 else "decreases_risk",
            }
            for i in range(len(feature_names))
        ]

        contributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        return contributions[:10]


shap_explainer_service = SHAPExplainerService()