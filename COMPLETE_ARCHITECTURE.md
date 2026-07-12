# 🏗️ SME Risk Platform - البنية الكاملة النهائية (ASCII Art)

## الهيكل الكامل

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║           🌐 SME RISK INTELLIGENCE PLATFORM - البنية الكاملة                      ║
╚════════════════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────────────────────────┐
│                          🖥️  FRONTEND LAYER (Next.js)                             │
│                        http://localhost:3000                                       │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        PUBLIC PAGES (No Auth)                              │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  /                  → Landing Page (企业概览)                               │ │
│  │  /login             → Login Page (电子邮件 + 密码)                          │ │
│  │  /register          → Registration (新账户创建)                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                    PROTECTED PAGES (Auth Required)                         │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  /dashboard                                                                │ │
│  │    ├─ /executive        → Executive Dashboard (KPIs, Stats)               │ │
│  │    ├─ /analytics        → Model Performance Console                       │ │
│  │    ├─ /reports          → Report Management Hub                           │ │
│  │    ├─ /risk-center      → Risk Assessment (3-Step Form)                   │ │
│  │    │   ├─ Step 1: Business Info (SME ID, Name, Industry)                  │ │
│  │    │   ├─ Step 2: Financial Data (Income, Deposits, NSF)                  │ │
│  │    │   └─ Step 3: Results (Score, Category, AI Insights)                  │ │
│  │    └─ /settings         → Admin Settings (Protected to Admins)            │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                     FRONTEND COMPONENTS & STATE                            │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  Hooks:                                                                     │ │
│  │    └─ useAuth.ts              ← Authentication State Management            │ │
│  │                                                                             │ │
│  │  Store (Zustand):                                                           │ │
│  │    └─ useAssessmentStore.ts   ← Assessment Form State (Step 1→2→3)        │ │
│  │                                                                             │ │
│  │  Components:                                                                │ │
│  │    ├─ RiskTrendChart.tsx       ← Risk Trend Line Chart (ECharts)          │ │
│  │    ├─ BusinessInfoStep.tsx     ← Step 1 Form (Company Data)               │ │
│  │    ├─ FinancialInfoStep.tsx    ← Step 2 Form (Financial Data)             │ │
│  │    └─ ResultsPanel.tsx         ← Step 3 Results Display                   │ │
│  │                                                                             │ │
│  │  Clients:                                                                   │ │
│  │    └─ api-client.ts            ← Axios Instance (JWT + Interceptors)      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
                                        ↓↑
                            HTTP/JSON (Axios + Bearer Token)
                                        ↓↑
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          🔴 BACKEND LAYER (FastAPI)                               │
│                        http://localhost:8000/docs                                 │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           API ROUTES                                        │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  /api/v1/auth/                                                              │ │
│  │    ├─ POST   /login              ← User Authentication (Email + Password)  │ │
│  │    ├─ POST   /register           ← New Account Creation                    │ │
│  │    ├─ GET    /me                 ← Current User Profile (JWT Protected)    │ │
│  │    └─ GET    /users              ← List All Users (Admin Only)             │ │
│  │                                                                              │ │
│  │  /api/v1/analytics/                                                         │ │
│  │    ├─ GET    /dashboard-stats    ← Portfolio Statistics (Total, High/Low)  │ │
│  │    └─ GET    /risk-trend         ← Risk Trends Over Time (Monthly)         │ │
│  │                                                                              │ │
│  │  /api/v1/assessment/                                                        │ │
│  │    ├─ POST   /single             ← Single SME Assessment (ML + AI)         │ │
│  │    └─ POST   /batch              ← Batch CSV Assessment (Background)       │ │
│  │                                                                              │ │
│  │  /api/v1/reports/                                                           │ │
│  │    ├─ GET    /history            ← Assessment History (for Reports Page)   │ │
│  │    ├─ POST   /generate/{id}      ← Generate PDF Report                     │ │
│  │    └─ GET    /download/{id}      ← Download PDF Report                     │ │
│  │                                                                              │ │
│  │  /health                          ← Server Health Check                     │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        MIDDLEWARE & SECURITY                               │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ├─ CORS Middleware                 ← Allow frontend localhost:3000        │ │
│  │  ├─ JWT Authentication              ← Verify Bearer Tokens                 │ │
│  │  ├─ Role-Based Authorization        ← Check user.role for admin routes    │ │
│  │  └─ Error Handling                  ← HTTPException + JSON responses       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         SERVICES LAYER                                     │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ├─ auth_service.py                                                         │ │
│  │  │  ├─ authenticate()             ← Login logic                            │ │
│  │  │  ├─ register()                 ← Registration logic                     │ │
│  │  │  └─ create_access_token()      ← JWT Token generation                  │ │
│  │  │                                                                          │ │
│  │  ├─ assessment_service.py                                                   │ │
│  │  │  └─ create_assessment()        ← Orchestrate ML + AI                   │ │
│  │  │                                                                          │ │
│  │  ├─ ml_service.py                                                           │ │
│  │  │  └─ predict_risk()             ← scikit-learn Model Inference          │ │
│  │  │                                                                          │ │
│  │  ├─ ai_service.py                                                           │ │
│  │  │  └─ generate_credit_recommendation() ← Gemini AI Integration           │ │
│  │  │                                                                          │ │
│  │  └─ pdf_service.py                                                          │ │
│  │     └─ generate_credit_report()   ← ReportLab PDF Generation              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                      REPOSITORIES LAYER                                    │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ├─ user_repository.py           ← User CRUD Operations                   │ │
│  │  └─ assessment_repository.py     ← Assessment CRUD Operations             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         ORM MODELS                                         │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ├─ User (users table)                                                      │ │
│  │  ├─ Role (roles: Admin, Analyst, Manager)                                  │ │
│  │  ├─ Organization (organizations)                                           │ │
│  │  ├─ SME (smes - small & medium enterprises)                               │ │
│  │  ├─ Assessment (assessments - risk evaluations)                           │ │
│  │  ├─ Report (reports - generated PDFs)                                     │ │
│  │  ├─ AuditLog (audit_logs - activity tracking)                             │ │
│  │  ├─ Prediction (predictions)                                              │ │
│  │  ├─ Notification (notifications)                                          │ │
│  │  └─ 4+ More Tables                                                         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                      VALIDATION SCHEMAS                                    │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ├─ auth_schema.py               ← UserCreate, UserOut, TokenResponse      │ │
│  │  ├─ sme_schema.py                ← SMEDataInput, DashboardStats            │ │
│  │  ├─ report_schema.py             ← ReportCreate, ReportResponse            │ │
│  │  └─ assessment_schema.py         ← AssessmentCreate, AssessmentResponse    │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                    SECURITY & CONFIGURATION                               │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │  ├─ security.py                                                             │ │
│  │  │  ├─ verify_password()          ← bcrypt password verification           │ │
│  │  │  ├─ get_password_hash()        ← bcrypt hashing                         │ │
│  │  │  └─ create_access_token()      ← JWT token creation                    │ │
│  │  │                                                                          │ │
│  │  └─ config.py                                                               │ │
│  │     ├─ DATABASE_URL               ← PostgreSQL connection string           │ │
│  │     ├─ SECRET_KEY                 ← JWT secret                             │ │
│  │     ├─ GEMINI_API_KEY             ← Gemini AI key                         │ │
│  │     └─ MODEL_PATH                 ← ML model file location                 │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
                                        ↓↓
                            SQL Queries + ORM Mapping
                                        ↓↓
┌────────────────────────────────────────────────────────────────────────────────────┐
│                      🗄️  DATABASE LAYER (PostgreSQL)                              │
│                          Localhost:5432                                           │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                       CORE TABLES (12+)                                    │ │
│  ├─────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                              │ │
│  │  users                                                                       │ │
│  │  ├─ id (PK) │ email (UNIQUE) │ hashed_password │ role_id (FK)            │ │
│  │  ├─ name │ organization_id (FK) │ is_active │ created_at │ updated_at    │ │
│  │  └─ phone                                                                   │ │
│  │                                                                              │ │
│  │  roles                                                                       │ │
│  │  ├─ id (PK) │ name (UNIQUE): "Admin", "Analyst", "Manager"               │ │
│  │  └─ description                                                             │ │
│  │                                                                              │ │
│  │  organizations                                                              │ │
│  │  ├─ id (PK) │ name │ industry │ country                                   │ │
│  │  └─ created_at                                                              │ │
│  │                                                                              │ │
│  │  smes                                                                        │ │
│  │  ├─ id (PK) │ organization_id (FK) │ legal_name │ industry                │ │
│  │  ├─ business_age_months │ status │ metadata │ created_at │ updated_at    │ │
│  │  └─ ownership_type                                                          │ │
│  │                                                                              │ │
│  │  assessments (Main Table)                                                  │ │
│  │  ├─ id (PK) │ sme_id (FK) │ user_id (FK) │ model_version                  │ │
│  │  ├─ risk_score (%) │ risk_category │ confidence (%)                       │ │
│  │  ├─ features_json │ shap_values_json │ ai_insights                        │ │
│  │  └─ created_at │ updated_at                                               │ │
│  │                                                                              │ │
│  │  reports                                                                     │ │
│  │  ├─ id (PK) │ assessment_id (FK) │ report_type                            │ │
│  │  ├─ title │ file_url │ status │ created_by (FK)                          │ │
│  │  └─ created_at │ updated_at                                               │ │
│  │                                                                              │ │
│  │  audit_logs                                                                 │ │
│  │  ├─ id (PK) │ user_id (FK) │ action │ resource                           │ │
│  │  ├─ changes_json                                                            │ │
│  │  └─ created_at                                                              │ │
│  │                                                                              │ │
│  │  + 5 More Tables:                                                           │ │
│  │    ├─ predictions         ← ML Predictions Archive                         │ │
│  │    ├─ notifications       ← User Notifications                             │ │
│  │    ├─ permissions         ← Role Permissions                               │ │
│  │    ├─ report_versions     ← Report Versioning                              │ │
│  │    └─ assessment_history  ← Historical Records                             │ │
│  │                                                                              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
                                        ↕
                            Redis Cache Layer (Optional)
                        (For Session & Data Caching)
                                        ↕
┌────────────────────────────────────────────────────────────────────────────────────┐
│                      💾  EXTERNAL SERVICES                                        │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌─────────────────┐        ┌─────────────────┐        ┌──────────────────────┐ │
│  │ Machine Learning│        │   Gemini AI     │        │  PDF Generation      │ │
│  │  (scikit-learn) │        │   (Google API)  │        │  (ReportLab)         │ │
│  ├─────────────────┤        ├─────────────────┤        ├──────────────────────┤ │
│  │ • Load Model    │        │ • Prompt        │        │ • Create PDF         │ │
│  │ • Predict Risk  │        │ • Generate      │        │ • Write Text         │ │
│  │ • Confidence    │        │   Recommendation│        │ • Save to Disk       │ │
│  │                 │        │                 │        │                      │ │
│  └─────────────────┘        └─────────────────┘        └──────────────────────┘ │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘


╔════════════════════════════════════════════════════════════════════════════════════╗
║                         🔄 DATA FLOW EXAMPLE                                      ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                    ║
║  1. User enters SME info (Step 1 & 2) in React Form                               ║
║  2. Store via Zustand: useAssessmentStore                                         ║
║  3. POST /api/v1/assessment/single (with JWT token)                               ║
║  4. Backend receives request                                                      ║
║  5. Authenticate user via JWT                                                     ║
║  6. Call ml_service.predict_risk() → scikit-learn Model                           ║
║  7. Call ai_service.generate_credit_recommendation() → Gemini AI                  ║
║  8. Create Assessment record in Database                                          ║
║  9. Return JSON response                                                          ║
║  10. Frontend receives & displays Results (Step 3)                                ║
║  11. User clicks "Export PDF"                                                     ║
║  12. POST /api/v1/reports/generate/{assessment_id}                               ║
║  13. Backend calls pdf_service.generate_credit_report()                           ║
║  14. Save PDF to disk & create Report record                                      ║
║  15. Return download URL                                                          ║
║  16. Frontend opens download link                                                 ║
║  17. GET /api/v1/reports/download/{report_id}                                    ║
║  18. Backend returns FileResponse (PDF)                                           ║
║  19. Browser downloads file                                                       ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝


╔════════════════════════════════════════════════════════════════════════════════════╗
║                       📊 ROLE-BASED ACCESS MATRIX                                ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                    ║
║  Feature              Admin    Analyst    Manager                                  ║
║  ────────────────────────────────────────────                                     ║
║  Create Assessment      ✅       ✅         ✅                                     ║
║  View Dashboard         ✅       ✅         ✅                                     ║
║  View Analytics         ✅       ✅         ✅                                     ║
║  Generate Reports       ✅       ✅         ✅                                     ║
║  Download Reports       ✅       ✅         ✅                                     ║
║  Manage Users           ✅       ❌         ❌                                     ║
║  System Settings        ✅       ❌         ❌                                     ║
║  View Audit Logs        ✅       ❌         ❌                                     ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝


╔════════════════════════════════════════════════════════════════════════════════════╗
║                     📦 DEPLOYMENT CONTAINERS                                      ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                    ║
║  Docker Compose Services:                                                         ║
║  ├─ frontend        (Next.js on :3000)                                            ║
║  ├─ backend         (FastAPI on :8000)                                            ║
║  ├─ db              (PostgreSQL on :5432)                                         ║
║  └─ redis           (Redis on :6379)                                              ║
║                                                                                    ║
║  docker-compose.yml orchestrates all services with networking                     ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 خريطة الملفات الكاملة

```
SMEs Risk Platform/
│
├── 🟢 frontend/                          (Next.js + React App)
│   ├── public/                           (Static assets)
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx        (Login form)
│   │   │   │   └── register/page.tsx     (Registration form)
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx            (Dashboard shell + Auth guard)
│   │   │   │   ├── executive/page.tsx    (Executive Dashboard)
│   │   │   │   ├── analytics/page.tsx    (Analytics Console)
│   │   │   │   ├── reports/page.tsx      (Reports Hub)
│   │   │   │   ├── risk-center/page.tsx  (Risk Assessment)
│   │   │   │   └── settings/page.tsx     (Admin Settings)
│   │   │   ├── page.tsx                  (Landing Page)
│   │   │   ├── layout.tsx                (Root Layout)
│   │   │   └── globals.css               (Global Styles)
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   │   └── RiskTrendChart.tsx    (ECharts component)
│   │   │   └── risk-center/
│   │   │       ├── BusinessInfoStep.tsx  (Step 1)
│   │   │       ├── FinancialInfoStep.tsx (Step 2)
│   │   │       └── ResultsPanel.tsx      (Step 3)
│   │   ├── hooks/
│   │   │   └── useAuth.ts                (Auth hook)
│   │   ├── lib/
│   │   │   └── api-client.ts             (Axios client)
│   │   └── store/
│   │       └── useAssessmentStore.ts     (Zustand store)
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.ts
│   ├── Dockerfile
│   └── .gitignore
│
├── 🔴 backend/                           (FastAPI)
│   ├── app/
│   │   ├── main.py                       (FastAPI app)
│   │   ├── api/
│   │   │   ├── dependencies.py           (JWT middleware)
│   │   │   └── routes/
│   │   │       ├── auth.py               (Auth endpoints)
│   │   │       ├── analytics.py          (Analytics endpoints)
│   │   │       ├── prediction.py         (Assessment endpoints)
│   │   │       └── reports.py            (Reports endpoints)
│   │   ├── db/
│   │   │   ├── base.py                   (SQLAlchemy base)
│   │   │   ├── database.py               (Connection setup)
│   │   │   ├── models.py                 (Models export)
│   │   │   └── __init__.py
│   │   ├── models/                       (ORM Models)
│   │   │   ├── user.py, role.py
│   │   │   ├── sme.py, assessment.py
│   │   │   ├── report.py, organization.py
│   │   │   └── ... (12+ models total)
│   │   ├── schemas/                      (Pydantic schemas)
│   │   │   ├── auth_schema.py
│   │   │   ├── sme_schema.py
│   │   │   ├── report_schema.py
│   │   │   └── assessment_schema.py
│   │   ├── services/                     (Business logic)
│   │   │   ├── auth_service.py
│   │   │   ├── assessment_service.py
│   │   │   ├── ml_service.py
│   │   │   ├── ai_service.py
│   │   │   └── pdf_service.py
│   │   ├── repositories/                 (Data access)
│   │   │   ├── user_repository.py
│   │   │   └── assessment_repository.py
│   │   └── core/
│   │       ├── config.py                 (Settings)
│   │       └── security.py               (JWT, Password)
│   ├── requirements.txt                  (Python deps)
│   ├── alembic.ini                       (Migrations)
│   ├── Dockerfile
│   └── .dockerignore
│
├── docker-compose.yml                    (Orchestration)
├── .env                                  (Environment vars)
├── PROJECT_STRUCTURE.md                  (Detailed structure)
├── FILES_REFERENCE.md                    (File references)
├── WORKFLOWS_GUIDE.md                    (Data flows)
├── README_COMPLETE.md                    (Full guide)
└── QUICK_REFERENCE.md                    (Quick guide)
```

---

**آخر تحديث**: 2026-07-09 | **الإصدار**: 1.0.0 | **الحالة**: ✅ جاهز للإنتاج
