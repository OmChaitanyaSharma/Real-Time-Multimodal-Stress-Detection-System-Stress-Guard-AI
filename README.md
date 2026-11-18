# Real-Time Multimodal Stress Detection and Analysis System

A B.Tech CSE major project that analyzes stress indicators using a combination of facial expression analysis and behavioural lifestyle metrics.

The system combines computer vision (face detection, Eye Aspect Ratio / EAR, and deep CNN emotion classification) with machine learning models (Random Forest, XGBoost, Support Vector Machine, and Logistic Regression) trained on lifestyle metrics. Explainable AI components include SHAP for feature attribution and Grad-CAM for facial attention heatmaps.

---

## System Architecture

```
[Webcam Stream] ──────> Face Detection & EAR ──> EmotionCNN + Grad-CAM ──┐
                                                                         ├──> [Multimodal Fusion] ──> [Stress Level] ──> [Recommendations]
[Lifestyle Survey] ───> Feature Normalizer ────> ML Models + SHAP ───────┘
```

The system classifies stress indicators into three categories:
- **Low Stress Indicators** (Index < 38%)
- **Moderate Stress Indicators** (Index 38% - 52%)
- **High Stress Indicators** (Index > 52%)

If one modality is unavailable (e.g., webcam disabled), the system falls back to the available modality rather than failing.

---

## Tech Stack

- **Frontend**: React 19, Tailwind CSS v4, Recharts, Lucide Icons, Vite (Running on port 5555)
- **Backend**: Python 3.13 / 3.14, FastAPI, Uvicorn, SQLAlchemy, SQLite (Running on port 8000)
- **Machine Learning**: PyTorch, Scikit-learn, XGBoost, SHAP, OpenCV
- **Testing**: Pytest, Vitest/React build

---

## Directory Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI route handlers (auth, facial, behavioural, fusion, history)
│   │   ├── ml/              # Inference models, fusion engine, and recommender
│   │   │   ├── saved_models/# Serialized model weights (.joblib, .pt)
│   │   │   └── cascades/    # OpenCV Haar cascade definitions
│   │   ├── models/          # SQLAlchemy database entities
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   ├── utils/           # Password hashing, JWT, image decoding, EAR
│   │   ├── config.py        # Environment settings and paths
│   │   ├── database.py      # Database session setup
│   │   └── main.py          # FastAPI application entry point
│   ├── data/                # Raw and processed datasets
│   ├── scripts/             # Dataset generation and model training scripts
│   ├── tests/               # Backend pytest suite
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # Webcam, questionnaire, gauge, SHAP and Grad-CAM viewers
│   │   ├── context/         # Authentication context (JWT)
│   │   ├── pages/           # Home, Login, Register, Assessment, Results, Dashboard, Benchmarks, Report
│   │   └── services/        # Axios API client
│   ├── package.json
│   └── vite.config.js       # Vite configuration (port 5555)
├── docs/
│   ├── BTech_Major_Project_Report.md # Formal 12-chapter academic report
│   └── testing_matrix.md             # Formal test cases and evaluation matrix
├── task_plan.md             # Active roadmap, tasks, issues and resolutions
├── findings.md              # Technical discoveries, API signatures, environment bounds
├── progress.md              # Session execution log and verification outputs
├── run_backend.bat          # One-click backend startup script (Port 8000)
├── run_frontend.bat         # One-click frontend startup script (Port 5555)
├── run_all.bat              # One-click concurrent system launcher
└── README.md
```

---

## Prerequisites

1. **Python 3.13 or 3.14**
2. **Node.js (v18+) and npm**
3. A functional laptop webcam or external USB camera

---

## Installation & Setup

### 1. Backend Setup

```powershell
# Navigate to the project root
cd "x:\projects\Real-Time Multimodal Stress Detection and Analysis System Using Machine Learning"

# Create a virtual environment (if not already created)
py -3.13 -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt
pip install email-validator
```

### 2. Dataset Generation & Model Training

Run the training pipeline to generate datasets and save trained models:

```powershell
# 1. Generate balanced behavioural dataset
.\venv\Scripts\python.exe backend/scripts/generate_datasets.py

# 2. Initialize and save the EmotionCNN weights
.\venv\Scripts\python.exe backend/scripts/train_facial.py

# 3. Train and benchmark the 4 ML models (RF, XGBoost, SVM, Logistic Regression) + SHAP
.\venv\Scripts\python.exe backend/scripts/train_behavioural.py

# 4. Seed the demo account and 8 historical assessments
.\venv\Scripts\python.exe backend/scripts/seed_demo_data.py
```

### 3. Frontend Setup

```powershell
cd frontend
npm install
```

---

## Running the Application

### Option A: Standalone Launcher (No Node.js / npm Required)

For systems without Node.js, npm, or Vite installed:

Double-click `run_without_npm.bat` or execute in PowerShell:

```powershell
.\run_without_npm.bat
```

This script:
1. Detects Python on your system (or activates `venv`).
2. Installs required Python libraries if not present.
3. Starts the FastAPI backend on port 8000.
4. Starts the Python static web server on port 5555 serving the pre-built frontend (`frontend/dist`).
5. Opens `http://localhost:5555` in your default browser.

### Option B: Concurrent Development Launch (Requires Node.js and npm)

If Node.js is installed and you want live frontend hot module reloading:

Double-click `run_all.bat` or execute:

```powershell
.\run_all.bat
```

This launches the FastAPI backend (port 8000) and the Vite development server (port 5555) in separate terminal windows.

### Option C: Manual Terminal Execution

#### 1. Start the Backend Server (Port 8000)

```powershell
cd backend
..\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The OpenAPI documentation is accessible at: `http://127.0.0.1:8000/docs`.

#### 2. Start the Frontend Server (Port 5555)

##### Without npm (Using Python standard library):
```powershell
python serve_frontend.py
```

##### With npm (Development mode):
```powershell
cd frontend
npm run dev
```

Open your browser at: `http://localhost:5555`

> Note: Port 5173 is reserved; the frontend is bound to **port 5555**.

---

## Pre-Seeded Demonstration Account

For examination, evaluation, and viva presentations:
- **Email**: `demo@stressguard.edu`
- **Password**: `Demo@123`

Clicking the **"Auto-Fill"** button on the sign-in page populates these credentials automatically. The account includes 8 historical assessments showing score trends over 14 days.

---

## Running Automated Tests

Run backend integration and unit tests:

```powershell
.\venv\Scripts\pytest -v
```

All 12 test suites cover authentication, input boundary validation, SHAP calculation, covered-camera fallbacks, single-modality evaluations, security headers, BOLA cross-tenant isolation, decompression bomb mitigation, and unauthenticated request rejection.

---

## Deployment & Hosting

### 1. Frontend Hosting on Vercel

The frontend includes production routing and caching rules configured in `frontend/vercel.json` and root `vercel.json`:
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Framework Preset**: Vite
- **Environment Variables**:
  - `VITE_API_URL`: URL of the deployed FastAPI backend (e.g. `https://your-backend.onrender.com/api`). When unset, it points to `http://localhost:8000/api`.

#### Deployment Steps:
1. Push the project repository to GitHub.
2. In the Vercel Dashboard, click **Add New Project** and select the repository.
3. Set **Root Directory** to `frontend` (or keep root; root `vercel.json` will route to `frontend`).
4. Add the `VITE_API_URL` environment variable pointing to the backend API.
5. Deploy. Vercel automatically deploys the single-page application with SPA rewrites (`/(.*) -> /index.html`) and asset caching.

### 2. Backend Cloud Deployment (Render / Railway / Docker)

The backend includes a `Dockerfile` and `docker-compose.yml`:

```powershell
# Build and run backend and frontend containers locally:
docker-compose up --build
```

For cloud platforms (such as Render or Railway):
1. Create a Web Service connected to the `backend/` directory.
2. Set build command: `pip install -r requirements.txt` (or use Dockerfile).
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables:
   - `SECRET_KEY`: A random secret key for JWT tokens.
   - `CORS_ORIGINS`: Frontend URL (e.g. `https://your-app.vercel.app`).
   - `DATABASE_URL`: SQLite URL or PostgreSQL connection string.

---

## Standalone Project Distribution Package

The project includes a pre-packaged distribution archive:
`Real_Time_Multimodal_Stress_Detection_System.zip` (4.49 MB).

### Contents Included:
- Complete backend codebase, database (`stress_system.db`), and cascade files.
- Serialized machine learning models (`.pt`, `.joblib`).
- Pre-compiled production frontend bundle in `frontend/dist/`.
- Zero-npm static server (`serve_frontend.py`) and launchers (`run_without_npm.bat`, `run_all.bat`).
- Automated test suite and documentation.
- All machine-dependent paths (`venv/`, `node_modules/`, cache directories) are excluded to ensure cross-system compatibility.

---

## Ethical and Medical Notice

This project is an engineering and academic screening prototype. It doesn't provide medical, psychological, or psychiatric diagnosis. Facial expressions alone don't establish clinical stress. Video frames are processed in-memory and discarded immediately without persistent storage.
