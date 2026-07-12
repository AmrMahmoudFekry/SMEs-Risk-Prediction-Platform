# 📁 SME Risk Platform - الملفات الرئيسية والمسارات

## 🎯 الملفات الحساسة والمهمة

### Backend - ملفات Core

#### `/backend/app/main.py` 🔴 (الملف الأساسي)
```python
✓ FastAPI App Initialization
✓ CORS Configuration
✓ Router Registration
✓ Database Seeding
✓ Health Check Endpoint
```

#### `/backend/app/api/routes/auth.py` 🔐 (المصادقة)
```
POST   /login      → Authenticate user, return JWT token
POST   /register   → Create new user account
GET    /me         → Get current user profile
GET    /users      → List all users (Admin only)
```

#### `/backend/app/api/routes/prediction.py` 🤖 (التنبؤات)
```
POST   /single     → Single SME Risk Assessment
POST   /batch      → Batch CSV Processing
```

#### `/backend/app/api/routes/analytics.py` 📊 (التحليلات)
```
GET    /dashboard-stats  → Portfolio Statistics
GET    /risk-trend       → Risk Trends Over Time
```

#### `/backend/app/api/routes/reports.py` 📄 (التقارير)
```
GET    /history         → Assessment History
POST   /generate/{id}   → Generate PDF Report
GET    /download/{id}   → Download Report
```

#### `/backend/app/api/dependencies.py` 🔑 (التوثيق)
```
✓ JWT Token Extraction
✓ Current User Validation
✓ Admin Permission Check
✓ OAuth2 Scheme Setup
```

#### `/backend/app/services/` 🛠️ (الخدمات الأساسية)
```
auth_service.py       → Login, Register, JWT Creation
assessment_service.py → ML + AI Orchestration
ml_service.py         → scikit-learn Model Inference
ai_service.py         → Gemini AI Integration
pdf_service.py        → Report PDF Generation
```

#### `/backend/app/models/` 🗄️ (قاعدة البيانات - ORM)
```
user.py              → User Table
role.py              → Role Table (Admin, Analyst, Manager)
sme.py               → SME/Business Records
assessment.py        → Risk Assessment Records
report.py            → Generated Reports
organization.py      → Organization Table
audit_log.py         → Activity Logging
...و المزيد
```

#### `/backend/app/core/` ⚙️ (الإعدادات)
```
config.py   → Database URL, API Keys, Settings
security.py → JWT, Password Hashing Functions
```

---

### Frontend - ملفات Core

#### `/frontend/src/app/layout.tsx` 🎨 (الـ Root Layout)
```
✓ Global HTML Structure
✓ Dark Mode Setup
✓ Tailwind CSS Init
✓ Metadata & Fonts
```

#### `/frontend/src/app/page.tsx` 🏠 (الصفحة الرئيسية)
```
✓ Landing Page
✓ Feature Overview
✓ Sign In / Register Links
✓ Enterprise Branding
```

#### `/frontend/src/app/(auth)/` 🔐 (مجموعة المصادقة)
```
login/page.tsx     → Email + Password Login
register/page.tsx  → New Account Registration
```

#### `/frontend/src/app/(dashboard)/layout.tsx` 📋 (لوحة التحكم)
```
✓ Sidebar Navigation
✓ Top Header with User Info
✓ Auth Guard (Redirect if not logged in)
✓ Role-Based Navigation
✓ Logout Button
```

#### `/frontend/src/app/(dashboard)/` 📑 (الصفحات المحمية)
```
executive/page.tsx     → Executive Dashboard (KPIs, Stats)
analytics/page.tsx     → Model Performance Console
reports/page.tsx       → Report Management Hub
risk-center/page.tsx   → Risk Assessment Workflow
settings/page.tsx      → Admin Settings (Protected)
```

#### `/frontend/src/hooks/useAuth.ts` 🪝 (Auth Hook)
```
✓ Fetch current user from /auth/me
✓ Store JWT in localStorage
✓ Logout functionality
✓ Loading state
```

#### `/frontend/src/lib/api-client.ts` 🌐 (HTTP Client)
```
✓ Axios instance with baseURL
✓ JWT Bearer token injection
✓ 401 Redirect handling
✓ Request/Response Interceptors
```

#### `/frontend/src/store/useAssessmentStore.ts` 🎯 (Zustand Store)
```
✓ Form step tracking (1, 2, 3)
✓ SME data state
✓ Processing status
✓ Reset functionality
```

#### `/frontend/src/components/` 🧩 (المكونات)
```
charts/RiskTrendChart.tsx      → Risk Line Chart (ECharts)
risk-center/BusinessInfoStep.tsx → Company Info Form
risk-center/FinancialInfoStep.tsx → Financial Data Form
risk-center/ResultsPanel.tsx    → Risk Results Display
```

---

## 📋 ملفات الإعدادات والتكوين

### Root Level
```
.env                        → Environment Variables
docker-compose.yml         → Docker Compose Stack
.gitignore                 → Git Ignore File
PROJECT_STRUCTURE.md       → هذا الملف
```

### Backend Config
```
requirements.txt           → Python Dependencies
alembic.ini               → Database Migration Config
Dockerfile                → Backend Container
.dockerignore             → Docker Ignore
```

### Frontend Config
```
package.json              → Node Dependencies
tsconfig.json             → TypeScript Config
next.config.ts            → Next.js Config
postcss.config.mjs        → Tailwind PostCSS
eslint.config.mjs         → ESLint Config
.next/                    → Build Output (Git Ignored)
```

---

## 🔗 ملخص الاتصالات

### Frontend → Backend API

```
Frontend Component          Backend Endpoint              Method
─────────────────────────────────────────────────────────────
(auth)/login                /api/v1/auth/login           POST
(auth)/register             /api/v1/auth/register        POST
layout.tsx (useAuth)        /api/v1/auth/me              GET
executive/page.tsx          /api/v1/analytics/dashboard-stats  GET
analytics/page.tsx          (Placeholder + /risk-trend)   GET
reports/page.tsx            /api/v1/reports/history      GET
reports/page.tsx            /api/v1/reports/generate/{id} POST
reports/page.tsx            /api/v1/reports/download/{id} GET
risk-center/FinancialStep   /api/v1/assessment/single    POST
RiskTrendChart.tsx          /api/v1/analytics/risk-trend  GET
```

---

## 🚀 خطوات التشغيل

### 1️⃣ استخراج الملفات والإعدادات
```bash
cd "SMEs Risk Platform"

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

### 2️⃣ تشغيل البيئة
```bash
# Using Docker Compose
docker-compose up -d

# OR Manual Setup
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (في terminal منفصل)
cd frontend
npm install
npm run dev  # يفتح على http://localhost:3000
```

### 3️⃣ اختبار المسارات
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# Get Current User
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Dashboard Stats
curl -X GET http://localhost:8000/api/v1/analytics/dashboard-stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 جودة الكود

| Metric | Status |
|--------|--------|
| Type Safety (TypeScript) | ✅ 100% |
| API Documentation | ✅ FastAPI Docs at `/docs` |
| Error Handling | ✅ Implemented |
| CORS Configuration | ✅ Configured |
| Database Migrations | ⚠️ Via Alembic (Manual) |
| Environment Security | ✅ .env Configuration |
| Production Ready | ⚠️ Needs Testing |

---

## 🔐 ملفات الأمان المهمة

- ✅ JWT Tokens (python-jose)
- ✅ Password Hashing (bcrypt)
- ✅ CORS Middleware
- ✅ Bearer Token Injection
- ⚠️ Rate Limiting (Not Implemented)
- ⚠️ Input Validation (Basic)
- ⚠️ SQL Injection Protection (SQLAlchemy ORM)

---

## 📈 إحصائيات المشروع

| Component | Count | Status |
|-----------|-------|--------|
| Backend Routes | 13 | ✅ |
| Frontend Pages | 7 | ✅ |
| React Components | 6 | ✅ |
| Database Models | 12+ | ✅ |
| API Schemas | 4 | ✅ |
| Services | 5 | ✅ |
| Total Files | 50+ | ✅ |

---

## 💾 خطوات النسخ الاحتياطي والحفظ

```bash
# حفظ قاعدة البيانات
pg_dump sme_risk_db > backup.sql

# حفظ الملفات المرفوعة (إن وجدت)
tar -czf reports_storage.tar.gz reports_storage/

# حفظ البيئة
cp .env .env.backup
```

---

**آخر تحديث**: 2026-07-09 | **الإصدار**: 1.0.0
