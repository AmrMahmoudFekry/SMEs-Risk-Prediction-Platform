"""
Custom Domain Exceptions
=========================
استثناءات خاصة بطبقة الأعمال (Domain/Service Layer)، مفصولة تمامًا عن
طبقة الـ HTTP (FastAPI). هذا يحافظ على مبدأ فصل الاهتمامات (Separation of
Concerns): طبقة الخدمات (services) لا يجب أن تعرف شيئًا عن HTTPException،
بينما طبقة الـ routes هي المسؤولة عن ترجمة هذه الاستثناءات إلى رموز حالة
HTTP مناسبة.
"""


class SMENotFoundError(Exception):
    """يُرفع عند عدم العثور على منشأة (SME) بالمعرف المحدد."""

    pass


class SMEAccessDeniedError(Exception):
    """
    يُرفع عند محاولة الوصول إلى منشأة تابعة لمؤسسة أخرى.
    يضمن عزل البيانات الصارم بين المستأجرين (Tenant Isolation) في بيئة
    multi-tenant SaaS، ويمنع ثغرات من نوع IDOR.
    """

    pass


class ModelNotAvailableError(Exception):
    """يُرفع عند عدم توفر نموذج التعلم الآلي المدرب (pipeline.pkl مفقود أو تالف)."""

    pass