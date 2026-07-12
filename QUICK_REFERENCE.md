# ⚡ SME Risk Platform - الملخص السريع

## 🎯 ماذا يفعل البرنامج؟
تطبيق ويب متكامل لتقييم **المخاطر الائتمانية للشركات الصغيرة والمتوسطة (SME)** باستخدام:
- 🤖 **Machine Learning** (scikit-learn) للتنبؤ الذكي
- 🧠 **AI (Gemini)** للتوصيات المالية المحترفة
- 📊 **لوحة تحكم** لرصد محفظة الائتمان
- 📄 **تقارير PDF** آلية

---

## 📊 البنية بنظرة سريعة

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Next.js + React + Tailwind + Zustand)           │
│  http://localhost:3000                                     │
├─────────────────────────────────────────────────────────────┤
│  Backend (FastAPI + SQLAlchemy + PostgreSQL)               │
│  http://localhost:8000                                     │
│  Docs: http://localhost:8000/docs                          │
├─────────────────────────────────────────────────────────────┤
│  Database (PostgreSQL)                                     │
│  Cache (Redis)                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ الملفات المهمة جداً

### Backend 🔴
```
app/main.py                    ← نقطة البداية
app/api/routes/auth.py         ← المصادقة
app/api/routes/prediction.py   ← التقييم
app/api/routes/analytics.py    ← الإحصائيات
app/api/routes/reports.py      ← التقارير
app/services/ml_service.py     ← نموذج ML
app/services/ai_service.py     ← Gemini AI
```

### Frontend 🟢
```
src/app/(auth)/login/page.tsx       ← تسجيل الدخول
src/app/(dashboard)/executive/      ← لوحة التحكم
src/app/(dashboard)/risk-center/    ← تقييم المخاطر
src/hooks/useAuth.ts                ← حالة المصادقة
src/lib/api-client.ts               ← الاتصال بالـ API
```

---

## 🔌 الـ API Endpoints (13 مسار)

| اسم العملية | الـ URL | الطريقة |
|-----------|--------|--------|
| 🔐 تسجيل الدخول | `/auth/login` | POST |
| 📝 التسجيل الجديد | `/auth/register` | POST |
| 👤 بيانات المستخدم | `/auth/me` | GET |
| 📋 قائمة المستخدمين | `/auth/users` | GET |
| 📊 إحصائيات اللوحة | `/analytics/dashboard-stats` | GET |
| 📈 اتجاهات المخاطر | `/analytics/risk-trend` | GET |
| 🎯 تقييم واحد | `/assessment/single` | POST |
| 📦 تقييم جماعي | `/assessment/batch` | POST |
| 📜 سجل التقييمات | `/reports/history` | GET |
| 🖨️ توليد التقرير | `/reports/generate/{id}` | POST |
| 📥 تنزيل التقرير | `/reports/download/{id}` | GET |

---

## 👥 الأدوار والصلاحيات (RBAC)

| الدور | الصلاحيات | الوصول |
|------|---------|--------|
| **Admin** | الكل | كل شيء + الإعدادات |
| **Analyst** | التقييم | لوحة + تقييم + تقارير |
| **Manager** | المراجعة | لوحة + تقارير فقط |

---

## 🚀 التشغيل السريع

### الطريقة 1️⃣: Docker (الأفضل)
```bash
cd "SMEs Risk Platform"

# إنشاء ملف البيئة
echo DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/sme_risk_db > .env
echo SECRET_KEY=super-secret-key >> .env
echo GEMINI_API_KEY=your-key >> .env
echo NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 >> .env

# تشغيل كل شيء
docker-compose up -d

# الروابط:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### الطريقة 2️⃣: يدوي (للتطوير)

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend** (في terminal منفصل)
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 بيانات اختبار

```
📧 Email: analyst@example.com
🔑 Password: password123
👤 Role: Analyst

📧 Email: admin@example.com
🔑 Password: password123
👤 Role: Admin
```

---

## 📱 تدفق المستخدم

```
Landing Page (/)
    ↓
[Login / Register]
    ↓
[Dashboard]
├─ Executive (إحصائيات)
├─ Risk Center (تقييم)
├─ Analytics (تحليل)
├─ Reports (تقارير)
└─ Settings (إدارة - Admin فقط)
```

---

## 🔄 خطوات التقييم

```
الخطوة 1️⃣: إدخال بيانات الشركة
├─ معرّف SME
├─ اسم الشركة
├─ القطاع الصناعي
└─ عمر النشاط

الخطوة 2️⃣: إدخال البيانات المالية
├─ مبلغ القرض
├─ متوسط الدخل الشهري
├─ إجمالي الودائع
└─ عدد الشيكات المرتجعة

الخطوة 3️⃣: النتائج
├─ درجة المخاطر (%)
├─ تصنيف (Low/Medium/High)
├─ مستوى الثقة (%)
├─ توصية الـ AI
└─ تنزيل PDF
```

---

## 🗄️ قاعدة البيانات (12+ جداول)

```
users          → المستخدمين
roles          → الأدوار
organizations  → الشركات
smes           → الشركات الصغيرة
assessments    → التقييمات
reports        → التقارير
audit_logs     → السجل
predictions    → التنبؤات
notifications  → التنبيهات
...و المزيد
```

---

## 🛠️ التكنولوجيا المستخدمة

### Backend 🔴
```
FastAPI          → الإطار الرئيسي
SQLAlchemy       → قاعدة البيانات (ORM)
PostgreSQL       → قاعدة البيانات
scikit-learn     → نموذج ML
Gemini AI        → التوصيات الذكية
ReportLab        → توليد PDF
JWT              → المصادقة
Pydantic         → التحقق من البيانات
```

### Frontend 🟢
```
Next.js          → الإطار الرئيسي
React 19         → واجهات المستخدم
Tailwind CSS     → التنسيق
Zustand          → إدارة الحالة
Axios            → طلبات HTTP
ECharts          → الرسوم البيانية
Lucide React     → الأيقونات
TypeScript       → أمان النوع
```

---

## 📊 الإحصائيات

| العنصر | العدد | الحالة |
|--------|-------|--------|
| API Routes | 13 | ✅ |
| Frontend Pages | 7 | ✅ |
| Components | 6+ | ✅ |
| DB Tables | 12+ | ✅ |
| Backend Code | ~2000 سطر | ✅ |
| Frontend Code | ~3000 سطر | ✅ |
| Dependencies (Back) | 16 | ✅ |
| Dependencies (Front) | 8 | ✅ |

---

## ✅ الميزات المنجزة

✅ المصادقة الكاملة (Login/Register)
✅ إدارة الأدوار (RBAC)
✅ لوحة تحكم تنفيذية
✅ تقييم متعدد الخطوات
✅ نموذج ML للتنبؤ
✅ توصيات Gemini AI
✅ توليد PDF
✅ تحليلات ورسوم بيانية
✅ واجهة احترافية
✅ معالجة الأخطاء

---

## ⚠️ القيود والتطورات المستقبلية

⏳ معالجة CSV الجماعية
⏳ التنبيهات الفورية
⏳ لوحات تحكم متقدمة
⏳ تطبيق موبايل
⏳ دعم عدة لغات
⏳ Rate Limiting
⏳ GraphQL API

---

## 🐛 استكشاف الأخطاء

| المشكلة | الحل |
|--------|------|
| Module not found | `pip install -r requirements.txt` |
| DB Connection Failed | تحقق من DATABASE_URL و PostgreSQL |
| CORS Error | تحقق من NEXT_PUBLIC_API_URL |
| Model File Missing | ضع pipeline.pkl في الجذر |
| Token Not Working | امسح localStorage أو سجل دخول مجدداً |

---

## 📁 المستندات المرفقة

```
📄 PROJECT_STRUCTURE.md   ← الخريطة الكاملة
📄 FILES_REFERENCE.md      ← ملفات مهمة
📄 WORKFLOWS_GUIDE.md      ← تدفقات البيانات
📄 README_COMPLETE.md      ← دليل شامل
📄 QUICK_REFERENCE.md      ← هذا الملف
```

---

## 🎯 نقاط الدخول الرئيسية

| الجزء | الملف | الغرض |
|-------|-------|--------|
| Backend Entry | `backend/app/main.py` | إنشاء التطبيق |
| Frontend Entry | `frontend/src/app/layout.tsx` | الـ Root Layout |
| Auth Entry | `frontend/src/app/(auth)/login/page.tsx` | نقطة الدخول |
| Dashboard | `frontend/src/app/(dashboard)/layout.tsx` | الحماية |
| API Auth | `backend/app/api/dependencies.py` | التحقق من JWT |

---

## 🌐 الروابط الهامة

```
Frontend:       http://localhost:3000
Backend:        http://localhost:8000
API Docs:       http://localhost:8000/docs
Database:       localhost:5432
Redis:          localhost:6379
```

---

## 💾 متطلبات النظام

```
Python:   3.11+
Node.js:  18+
Docker:   20.10+
Memory:   2GB Min
Storage:  5GB Min
```

---

## 🎓 للبدء الآن

1. **انسخ المجلد** إلى جهازك
2. **أنشئ `.env`** بالبيانات المطلوبة
3. **شغّل `docker-compose up -d`**
4. **افتح `http://localhost:3000`**
5. **سجّل دخول** باستخدام البيانات الاختبارية
6. **ابدأ التقييم!** 🚀

---

**آخر تحديث**: 2026-07-09
**الإصدار**: 1.0.0
**الحالة**: جاهز للإنتاج ✅

---

**صُنع بـ ❤️ لـ DEPI SME Risk Intelligence Platform**
