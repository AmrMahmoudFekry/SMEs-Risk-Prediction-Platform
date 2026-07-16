"""
SME Risk Feature Engineering
=============================
هذا الملف هو المصدر الوحيد (Single Source of Truth) لمنطق هندسة الخصائص
المستخدم في تدريب النموذج (train_pipeline.py) وفي وقت الاستدلال (ml_service.py).

المنطق مكتوب كدوال (functions) مباشرة وواضحة لسهولة المراجعة والتدقيق
(auditability) من قبل فرق الامتثال (Compliance) في البنوك، بدلاً من إخفائه
داخل طبقات OOP معقدة. الكلاس SMEFeatureEngineer هو مجرد غلاف رفيع (thin
wrapper) مطلوب فقط للتوافق مع واجهة sklearn.Pipeline.
"""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# =========================================================
# الأعمدة الأساسية المطلوبة من المستخدم/الواجهة
# =========================================================
REQUIRED_COLUMNS = [
    "credit_amount",
    "monthly_income_avg",
    "total_deposits_3m",
    "revenue_volatility_3m",
    "request_ratio",
    "dti_monthly",
    "nsf_count_3m",
    "negative_days_3m",
    "owner_percentage",
    "owner_credit_score",
    "business_age_months",
]

# الترتيب الحقيقي الذي تم تدريب النموذج عليه (يُستخدم لإعادة ترتيب أي DataFrame)
TRAINING_COLUMN_ORDER = [
    "credit_amount",
    "monthly_income_avg",
    "total_deposits_3m",
    "nsf_count_3m",
    "negative_days_3m",
    "business_age_months",
    "dti_monthly",
    "owner_percentage",
    "owner_credit_score",
    "revenue_volatility_3m",
    "request_ratio",
]


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """توحيد أسماء الأعمدة (lowercase, strip, replace spaces)."""
    df = df.copy()
    df.columns = (
        df.columns.str.lower().str.strip().str.replace(" ", "_")
    )
    return df


def validate_required_columns(df: pd.DataFrame) -> None:
    """التحقق من وجود كل الأعمدة المطلوبة، وإلا يتم رفع KeyError واضح."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required input columns: {', '.join(missing)}")


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    توليد 12 خاصية مشتقة (engineered features) من الخصائص الأساسية.

    كل خاصية مكتوبة بشكل صريح ومنفصل عشان يبقى سهل تتبع أثر أي متغير
    على قرار المخاطرة النهائي (مطلوب لأغراض الامتثال البنكي).
    """
    df = standardize_columns(df)
    validate_required_columns(df)
    df = df.copy()

    eps = 1e-5

    # 1. نسبة الائتمان إلى الدخل
    df["credit_income_ratio"] = df["credit_amount"] / (df["monthly_income_avg"] + eps)

    # 2. تغطية الإيداعات لمبلغ الائتمان
    df["deposit_coverage"] = df["total_deposits_3m"] / (df["credit_amount"] + eps)

    # 3. نسبة الدخل إلى متوسط الإيداع الشهري
    df["income_deposit_ratio"] = df["monthly_income_avg"] / (
        df["total_deposits_3m"] / 3 + eps
    )

    # 4. استقرار الإيرادات (عكس التذبذب)
    df["revenue_stability"] = 1.0 / (df["revenue_volatility_3m"] + eps)

    # 5. درجة استقرار العمر التشغيلي مع مراعاة التذبذب
    volatility_clipped = df["revenue_volatility_3m"].clip(0.0, 1.0)
    df["age_stability_score"] = df["business_age_months"] * (1 - volatility_clipped)

    # 6. الضغط المالي (الرافعة المالية × نسبة الطلب)
    df["financial_stress"] = df["dti_monthly"] * df["request_ratio"]

    # 7. نسبة مخاطر NSF بالنسبة لعمر الشركة
    df["nsf_risk_ratio"] = df["nsf_count_3m"] / (df["business_age_months"] + eps)

    # 8. نسبة أيام النشاط السلبي من إجمالي فترة المراقبة (90 يومًا)
    df["negative_activity_ratio"] = df["negative_days_3m"] / 90.0

    # 9. موثوقية المالك (الدرجة الائتمانية × نسبة الملكية)
    df["owner_reliability"] = (df["owner_credit_score"] / 850.0) * (
        df["owner_percentage"] / 100.0
    )

    # 10. تفاعل NSF مع نسبة الدين إلى الدخل
    df["nsf_dti_interaction"] = df["nsf_count_3m"] * df["dti_monthly"]

    # 11. نسبة الإيداعات إلى عدد حالات NSF
    df["deposit_nsf_ratio"] = df["total_deposits_3m"] / (df["nsf_count_3m"] + 1)

    # 12. نسبة ضغط السيولة (تغطية الإيداعات / الضغط المالي)
    df["liquidity_stress_ratio"] = df["deposit_coverage"] / (
        df["financial_stress"] + eps
    )

    return df


def prepare_input(data: dict | list[dict] | pd.DataFrame) -> pd.DataFrame:
    """
    نقطة الدخول الموحّدة لتجهيز أي مدخل (dict فردي أو batch) قبل التنبؤ.
    تُستخدم في طبقة الـ services قبل استدعاء النموذج مباشرة (خارج sklearn Pipeline)
    عند الحاجة لعرض الخصائص المشتقة (مثلاً في التقارير أو SHAP).
    """
    if isinstance(data, dict):
        input_df = pd.DataFrame([data])
    elif isinstance(data, list):
        input_df = pd.DataFrame(data)
    else:
        input_df = data.copy()

    input_df = standardize_columns(input_df)
    return create_features(input_df)


class SMEFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    غلاف رفيع (thin wrapper) متوافق مع sklearn.Pipeline.
    لا يحتوي على أي منطق خاص به — كل الحساب يتم تفويضه لدالة create_features
    أعلاه، حفاظًا على مبدأ "مصدر حقيقة واحد" (single source of truth).
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        return create_features(df)