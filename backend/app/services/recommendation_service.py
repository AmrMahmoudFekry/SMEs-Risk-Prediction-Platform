"""
Rule-Based Recommendation Engine
==================================
منطق توصيات حتمي (deterministic) قائم على قواعد مالية صريحة وواضحة، بدون
أي تدخل من نماذج اللغة الكبيرة (LLM). الهدف هو ضمان أن القرار الائتماني له
أساس رقمي قابل للتدقيق (auditable) يتوافق مع متطلبات الامتثال البنكي،
بينما يُستخدم Gemini (ai_service.py) بشكل منفصل تمامًا لتوليد سرد استشاري
تكميلي فقط — لا يُسمح لمخرجات الذكاء الاصطناعي التوليدي بأن تحل محل هذا
المنطق الحتمي أو تتعارض معه.

العتبات (thresholds) هنا مطابقة تمامًا لمنطق نسخة Streamlit الأصلية لضمان
اتساق القرار الائتماني بين المنصتين خلال فترة الانتقال.
"""

from typing import Dict, Any, List

RECOMMENDATIONS_CONTENT: Dict[str, Dict[str, Dict[str, str]]] = {
    "en": {
        "dti": {
            "title": "Debt Optimization Strategy",
            "description": (
                "The business currently operates with elevated leverage "
                "exposure. Restructuring short-term liabilities and improving "
                "liquidity allocation is strongly recommended."
            ),
            "priority": "HIGH",
        },
        "credit": {
            "title": "Creditworthiness Enhancement",
            "description": (
                "The owner's credit profile negatively impacts financing "
                "eligibility. Improving repayment consistency and reducing "
                "outstanding obligations may strengthen lending approval "
                "chances."
            ),
            "priority": "HIGH",
        },
        "volatility": {
            "title": "Revenue Stabilization Plan",
            "description": (
                "Revenue fluctuations indicate unstable operational cash "
                "flow. Implement recurring revenue streams and reserve "
                "liquidity buffers."
            ),
            "priority": "MEDIUM",
        },
        "neg_days": {
            "title": "Liquidity Management Improvement",
            "description": (
                "Frequent negative balances suggest operational liquidity "
                "pressure. Enhancing receivable collection efficiency is "
                "recommended."
            ),
            "priority": "HIGH",
        },
        "nsf": {
            "title": "Operational Cash Buffer",
            "description": (
                "NSF activity impacts financial reliability indicators. "
                "Maintaining emergency liquidity reserves is advised."
            ),
            "priority": "MEDIUM",
        },
        "startup": {
            "title": "Early-Stage Business Risk",
            "description": (
                "Limited business operating history increases uncertainty. "
                "Providing audited projections and operational evidence is "
                "recommended."
            ),
            "priority": "MEDIUM",
        },
        "high_risk": {
            "title": "High-Risk Exposure",
            "description": (
                "The overall financial profile indicates elevated lending "
                "risk. A conservative financing approach is advised."
            ),
            "priority": "CRITICAL",
        },
        "healthy": {
            "title": "Healthy Financial Position",
            "description": (
                "The company demonstrates stable operational performance "
                "and balanced financial indicators."
            ),
            "priority": "LOW",
        },
    },
    "ar": {
        "dti": {
            "title": "استراتيجية تحسين الديون",
            "description": (
                "تعمل الشركة حاليًا بمستوى مرتفع من الرافعة المالية. يُوصى "
                "بشدة بإعادة هيكلة الالتزامات قصيرة الأجل وتحسين توزيع "
                "السيولة."
            ),
            "priority": "HIGH",
        },
        "credit": {
            "title": "تعزيز الجدارة الائتمانية",
            "description": (
                "يؤثر الملف الائتماني للمالك سلبًا على أهلية التمويل. قد "
                "يُسهم تحسين انتظام السداد وتقليل الالتزامات القائمة في "
                "تعزيز فرص الحصول على القرض."
            ),
            "priority": "HIGH",
        },
        "volatility": {
            "title": "خطة استقرار الإيرادات",
            "description": (
                "تشير تذبذبات الإيرادات إلى تدفق نقدي تشغيلي غير مستقر. "
                "يُنصح بتنويع مصادر الإيراد المتكررة وتكوين احتياطيات سيولة."
            ),
            "priority": "MEDIUM",
        },
        "neg_days": {
            "title": "تحسين إدارة السيولة",
            "description": (
                "تشير الأرصدة السلبية المتكررة إلى ضغط على السيولة "
                "التشغيلية. يُوصى بتعزيز كفاءة تحصيل الذمم المدينة."
            ),
            "priority": "HIGH",
        },
        "nsf": {
            "title": "احتياطي نقدي تشغيلي",
            "description": (
                "يؤثر نشاط NSF على مؤشرات الموثوقية المالية. يُنصح بالحفاظ "
                "على احتياطيات سيولة طارئة."
            ),
            "priority": "MEDIUM",
        },
        "startup": {
            "title": "مخاطر الشركات الناشئة",
            "description": (
                "يزيد محدودية السجل التشغيلي للشركة من حالة عدم اليقين. "
                "يُوصى بتقديم توقعات مدققة وأدلة تشغيلية."
            ),
            "priority": "MEDIUM",
        },
        "high_risk": {
            "title": "تعرض مرتفع للمخاطر",
            "description": (
                "يشير الملف المالي الإجمالي إلى مخاطر إقراض مرتفعة. يُنصح "
                "باتباع نهج تمويل محافظ."
            ),
            "priority": "CRITICAL",
        },
        "healthy": {
            "title": "وضع مالي سليم",
            "description": "تُظهر الشركة أداءً تشغيليًا مستقرًا ومؤشرات مالية متوازنة.",
            "priority": "LOW",
        },
    },
}


def generate_recommendations(
    financials: Dict[str, Any], risk_score: float, lang: str = "en"
) -> List[Dict[str, str]]:
    """
    يُنتج قائمة من التوصيات الاستراتيجية بناءً على عتبات مالية ثابتة
    ومُختبَرة مسبقًا، مطابقة تمامًا للمنطق المستخدم في نسخة Streamlit
    الأصلية لضمان اتساق القرار الائتماني بين المنصتين.
    """
    content = RECOMMENDATIONS_CONTENT.get(lang, RECOMMENDATIONS_CONTENT["en"])
    recommendations: List[Dict[str, str]] = []

    dti_monthly = float(financials.get("dti_monthly", 0))
    owner_credit_score = float(financials.get("owner_credit_score", 850))
    revenue_volatility_3m = float(financials.get("revenue_volatility_3m", 0))
    negative_days_3m = float(financials.get("negative_days_3m", 0))
    nsf_count_3m = float(financials.get("nsf_count_3m", 0))
    business_age_months = float(financials.get("business_age_months", 999))

    if dti_monthly > 0.45:
        recommendations.append(content["dti"])

    if owner_credit_score < 600:
        recommendations.append(content["credit"])

    if revenue_volatility_3m > 0.40:
        recommendations.append(content["volatility"])

    if negative_days_3m > 15:
        recommendations.append(content["neg_days"])

    if nsf_count_3m > 2:
        recommendations.append(content["nsf"])

    if business_age_months < 24:
        recommendations.append(content["startup"])

    if risk_score >= 70:
        recommendations.append(content["high_risk"])

    if len(recommendations) == 0:
        recommendations.append(content["healthy"])

    return recommendations