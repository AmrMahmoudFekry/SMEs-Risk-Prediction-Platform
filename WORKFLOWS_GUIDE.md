# 🔄 SME Risk Platform - العمليات والـ Workflows

## 📱 1. User Journey - رحلة المستخدم

### 🔵 Onboarding Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Landing Page (/)                      │
│  - Platform Overview                                     │
│  - Features Highlight                                   │
│  - Sign In / Register Buttons                           │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐
    │ Sign In      │ │ Register     │
    │ (/login)     │ │ (/register)  │
    └──────────────┘ └──────────────┘
          │               │
          └───────────────┼───────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │ POST /api/v1/auth/login         │
        │ or                              │
        │ POST /api/v1/auth/register      │
        │                                 │
        │ Response: JWT Token             │
        └─────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │ Store Token in localStorage     │
        │ Set useAuth Hook                │
        └─────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   Dashboard Layout              │
        │   (Protected Pages)             │
        └─────────────────────────────────┘
```

### 🟢 Dashboard Access Flow

```
Dashboard Layout (/dashboard/*)
├─ useAuth Hook Fetches /auth/me
├─ Token Injected via Axios Interceptor
├─ If 401: Redirect to /login
└─ If Success: Show Dashboard
    ├─ Sidebar Navigation
    ├─ Role-Based Menus
    └─ Top Header with User Info
```

---

## 🎯 2. Risk Assessment Workflow (الأساسي)

### 📋 Multi-Step Assessment Process

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ Step 1: Business Profile            │
├─────────────────────────────────────┤
│ Form Fields:                        │
│ - SME ID (Required)                 │
│ - Legal Company Name                │
│ - Industry Sector                   │
│ - Business Age (months)             │
│ - Owner Credit Score                │
│                                     │
│ State: useAssessmentStore (Step 1)  │
│ Action: "Next → Step 2"             │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Step 2: Financial Information       │
├─────────────────────────────────────┤
│ Form Fields:                        │
│ - Credit Amount                     │
│ - Monthly Income Average            │
│ - Total Deposits (3 months)         │
│ - NSF Count (Bounced Checks)        │
│                                     │
│ State: useAssessmentStore (Step 2)  │
│ Action: "Run AI Assessment"         │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ API Request                         │
│ POST /api/v1/assessment/single      │
├─────────────────────────────────────┤
│ Payload:                            │
│ {                                   │
│   "sme_id": 1,                      │
│   "financials": {                   │
│     "legal_name": "...",            │
│     "industry": "...",              │
│     "business_age_months": 24,      │
│     "credit_amount": 50000,         │
│     ...                             │
│   }                                 │
│ }                                   │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Backend Processing                  │
├─────────────────────────────────────┤
│ 1. Extract financials               │
│ 2. Call ML Service                  │
│    - Load model (scikit-learn)      │
│    - Predict risk_score             │
│    - Calculate confidence           │
│ 3. Call AI Service (Gemini)         │
│    - Generate credit recommendation │
│ 4. Create Assessment Record         │
│ 5. Store in Database                │
│ 6. Return response                  │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ API Response                        │
├─────────────────────────────────────┤
│ {                                   │
│   "assessment_id": 42,              │
│   "risk_profile": {                 │
│     "risk_score": 65.5,             │
│     "risk_category": "Medium Risk", │
│     "confidence": 89.2              │
│   },                                │
│   "ai_insights": "Recommendation..."│
│ }                                   │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ Step 3: Results Display             │
├─────────────────────────────────────┤
│ - Risk Score Badge (65.5%)          │
│ - Risk Category (Medium)            │
│ - Confidence Level (89.2%)          │
│ - AI Credit Recommendation          │
│ - Action Buttons:                   │
│   * Export PDF                      │
│   * New Assessment                  │
└─────────────────────────────────────┘
  │
  ▼
END
```

---

## 📄 3. Report Generation & Download Flow

### 📋 Complete Report Process

```
┌─────────────────────────────────────┐
│ Reports Hub Page                    │
│ GET /api/v1/reports/history         │
├─────────────────────────────────────┤
│ Response: Array of Assessments      │
│ [                                   │
│   {                                 │
│     "id": "RI-20260709-42",        │
│     "db_id": 42,                    │
│     "smeName": "Company XYZ",       │
│     "date": "2026-07-09 14:30",    │
│     "risk": "Medium Risk",          │
│     "score": 65.5                   │
│   },                                │
│   ...                               │
│ ]                                   │
│                                     │
│ Display: Search + Filter List       │
└─────────────────────────────────────┘
         │
         │ User Clicks "Download"
         │ (Passes db_id = 42)
         ▼
┌─────────────────────────────────────┐
│ Generate Report                     │
│ POST /api/v1/reports/generate/{42}  │
├─────────────────────────────────────┤
│ Backend:                            │
│ 1. Fetch Assessment from DB         │
│ 2. Generate PDF using ReportLab     │
│ 3. Save file to reports_storage/    │
│ 4. Create Report Record in DB       │
│    - Set created_by = current_user  │
│    - Store file_url                 │
│ 5. Return download URL              │
│                                     │
│ Response:                           │
│ {                                   │
│   "status": "success",              │
│   "report_id": 5,                   │
│   "download_url": "/api/.../5"      │
│ }                                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Download PDF File                   │
│ GET /api/v1/reports/download/{5}    │
├─────────────────────────────────────┤
│ Backend:                            │
│ 1. Check if user is authenticated   │
│ 2. Fetch Report record              │
│ 3. Return FileResponse              │
│ 4. Browser downloads PDF            │
│                                     │
│ File Name:                          │
│ Credit_Report_SME_1_202607091430.pdf│
└─────────────────────────────────────┘
```

---

## 📊 4. Analytics & Dashboard Flow

### 📈 Dashboard Stats Loading

```
Executive Dashboard Page
         │
         ▼
┌─────────────────────────────────────┐
│ useEffect Hook                      │
│ Call: fetchStats()                  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ API Request                         │
│ GET /api/v1/analytics/dashboard-stats
├─────────────────────────────────────┤
│ Backend Query:                      │
│ 1. COUNT(assessments) → total_smes  │
│ 2. COUNT(WHERE risk='High') → high  │
│ 3. COUNT(WHERE risk='Low') → low    │
│ 4. AVG(confidence) → avg_confidence │
│                                     │
│ Response:                           │
│ {                                   │
│   "total_smes": 150,                │
│   "high_risk_count": 35,            │
│   "medium_risk_count": 60,          │
│   "low_risk_count": 55,             │
│   "average_confidence": 92.5        │
│ }                                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Update React State                  │
│ Display Dashboard Cards             │
│ - Total: 150                        │
│ - High Risk: 35                     │
│ - Low Risk: 55                      │
│ - Confidence: 92.5%                 │
└─────────────────────────────────────┘
```

### 📉 Risk Trend Chart Loading

```
RiskTrendChart Component
         │
         ▼
┌─────────────────────────────────────┐
│ useEffect Hook                      │
│ Call: fetchTrend()                  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ API Request                         │
│ GET /api/v1/analytics/risk-trend    │
├─────────────────────────────────────┤
│ Backend Query:                      │
│ GROUP BY Month, risk_category       │
│ COUNT assessments per month/risk    │
│                                     │
│ Response:                           │
│ {                                   │
│   "2026-06": {                      │
│     "High Risk": 12,                │
│     "Medium Risk": 25,              │
│     "Low Risk": 40                  │
│   },                                │
│   "2026-07": {                      │
│     "High Risk": 10,                │
│     "Medium Risk": 30,              │
│     "Low Risk": 45                  │
│   },                                │
│   ...                               │
│ }                                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Transform Data for ECharts          │
│ Months: ["2026-06", "2026-07", ...] │
│ Series:                             │
│ - High Risk: [12, 10, ...]          │
│ - Low Risk: [40, 45, ...]           │
│                                     │
│ Render Line Chart                   │
│ X-Axis: Months                      │
│ Y-Axis: Count                       │
└─────────────────────────────────────┘
```

---

## 🔐 5. Authentication & Authorization Flow

### 🔑 Login Process

```
User Enters Email + Password
         │
         ▼
┌─────────────────────────────────────┐
│ POST /api/v1/auth/login             │
│ Content-Type: form-urlencoded       │
│ username=email@example.com          │
│ password=password123                │
├─────────────────────────────────────┤
│ Backend:                            │
│ 1. Query: user = find by email      │
│ 2. Check: verify_password()         │
│ 3. If invalid → 401 Error           │
│ 4. If valid:                        │
│    - Create JWT Token               │
│    - Include: sub=email, role=role  │
│    - Return token + role            │
│                                     │
│ Response:                           │
│ {                                   │
│   "access_token": "eyJ0ex...",      │
│   "token_type": "bearer",           │
│   "role": "Analyst"                 │
│ }                                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Frontend:                           │
│ 1. Store token in localStorage      │
│ 2. Set useAuth state                │
│ 3. Redirect to /executive           │
└─────────────────────────────────────┘
```

### 🛡️ Protected Route Access

```
User Requests Protected Page (/executive)
         │
         ▼
┌─────────────────────────────────────┐
│ Layout.tsx checks useAuth()         │
├─────────────────────────────────────┤
│ If !isLoading:                      │
│   If !user → Redirect to /login     │
│   If user → Show Page               │
│     Show sidebar (check role)       │
│     If role === 'Admin':            │
│       Show /settings link           │
│     End If                          │
└─────────────────────────────────────┘
```

### 🔀 Axios Interceptor

```
Every API Request
         │
         ▼
┌─────────────────────────────────────┐
│ Axios Request Interceptor           │
├─────────────────────────────────────┤
│ 1. Get token from localStorage      │
│ 2. Add to header:                   │
│    Authorization: Bearer <token>    │
│ 3. Send request with header         │
└─────────────────────────────────────┘
         │
         ▼
    API Response
         │
         ├─ Status: 200-299 ✅
         │  └─ Pass to component
         │
         └─ Status: 401 ❌
            ├─ Remove token
            ├─ Redirect to /login
            └─ Show error

```

---

## 🎨 6. Frontend State Management

### Zustand Assessment Store Flow

```
Risk Assessment Form
         │
         ▼
┌─────────────────────────────────────┐
│ useAssessmentStore()                │
├─────────────────────────────────────┤
│ State:                              │
│ - step: 1 (Form Step)               │
│ - smeData: {} (Form Values)         │
│ - isProcessing: false (Loading)     │
│                                     │
│ Actions:                            │
│ - setStep(2)                        │
│ - updateSmeData({...})              │
│ - setProcessing(true)               │
│ - resetForm()                       │
└─────────────────────────────────────┘
         │
         ▼
Step 1 Form
  ├─ User enters: legal_name, industry, sme_id
  ├─ updateSmeData() called
  ├─ Store updated (Step 1 data saved)
  ├─ setStep(2)
  │
  ▼
Step 2 Form
  ├─ User enters: credit_amount, income, deposits
  ├─ updateSmeData() called
  ├─ Store updated (Step 2 data added)
  ├─ setProcessing(true)
  ├─ POST /api/v1/assessment/single
  ├─ setProcessing(false)
  ├─ Response saved: updateSmeData({assessmentResult: ...})
  ├─ setStep(3)
  │
  ▼
Step 3 Results
  ├─ Display assessmentResult data
  ├─ Show risk score, category, AI insights
  ├─ User clicks "New Assessment"
  ├─ resetForm() clears state
  ├─ setStep(1)
  └─ Back to Step 1
```

---

## 🗂️ 7. Error Handling Flow

### API Error Response

```
Request to API
         │
         ▼
┌─────────────────────────────────────┐
│ Backend Error Handling              │
├─────────────────────────────────────┤
│ Try:                                │
│   - Process request                 │
│   - Execute business logic          │
│ Catch:                              │
│   - Log error                       │
│   - Return HTTPException            │
│   - Status: 400/401/404/500         │
│   - Detail: Error message           │
│                                     │
│ Response:                           │
│ {                                   │
│   "detail": "Invalid credentials"   │
│ }                                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Frontend Error Handling             │
├─────────────────────────────────────┤
│ Try:                                │
│   - Make API call                   │
│ Catch:                              │
│   - Show error to user              │
│   - Log to console                  │
│   - Update loading state            │
│                                     │
│ Display:                            │
│ Error Banner: Red alert with msg    │
└─────────────────────────────────────┘
```

---

## 📋 Summary of Data Flows

| Flow | Source → Destination | Method |
|------|--------|--------|
| Auth | Frontend → Backend | POST /login, POST /register |
| User | Frontend → Backend | GET /auth/me |
| Stats | Frontend → Backend | GET /analytics/dashboard-stats |
| Trends | Frontend → Backend | GET /analytics/risk-trend |
| Assessment | Frontend → Backend | POST /assessment/single |
| Reports | Frontend → Backend | GET /reports/history |
| Generate Report | Frontend → Backend | POST /reports/generate/{id} |
| Download | Frontend → Backend | GET /reports/download/{id} |

---

**Last Updated**: 2026-07-09 | **Version**: 1.0.0
