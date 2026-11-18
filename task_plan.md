# Task Plan: Real-Time Multimodal Stress Detection and Analysis System

## Roadmap & Status

### Phase 1: Environment & Architecture Setup
- [x] Create project directory structure (`backend`, `frontend`, `docs`).
- [x] Create Python virtual environment (`py -3.13 -m venv venv`).
- [x] Install backend dependencies (`fastapi`, `uvicorn`, `torch`, `torchvision`, `scikit-learn`, `xgboost`, `shap`, `opencv-python`, `mediapipe`, `email-validator`).
- [x] Initialize Vite React 19 frontend and configure to port 5174 (preserving port 5173).
- [x] Install frontend dependencies (`tailwindcss`, `@tailwindcss/vite`, `lucide-react`, `recharts`, `axios`, `react-router-dom`).

### Phase 2: Data Pipeline & Model Training
- [x] Develop `generate_datasets.py` modeling the SWELL-KW and student stress protocols.
- [x] Generate balanced 3000-sample dataset (`stress_behavioural_data.csv`) across Low, Moderate, High classes.
- [x] Implement and train 4 algorithms: Random Forest, XGBoost, Support Vector Machine (RBF), and Logistic Regression.
- [x] Execute 5-fold stratified cross-validation and compute multi-class ROC-AUC and confusion matrices.
- [x] Fit and serialize SHAP `TreeExplainer` on the trained model.
- [x] Implement `train_facial.py` with deep `EmotionCNN` (PyTorch) with Grad-CAM gradient hooks on terminal layer `conv4`.
- [x] Download official OpenCV Haar cascades (`haarcascade_frontalface_default.xml`, `haarcascade_eye.xml`) to `backend/app/ml/cascades/`.

### Phase 3: Multimodal Decision Fusion & XAI Engine
- [x] Build `fusion_model.py` supporting dynamic soft-voting with quality-weighted confidences.
- [x] Formulate missing modality fallback (`facial_only` or `behavioural_only`).
- [x] Implement masked-stress dissonance detector (reweighting when a user smiles during acute chronic lifestyle strain).
- [x] Implement context-driven wellness recommendations in `recommender.py`.
- [x] Implement Grad-CAM heatmap generation with Jet colormap overlay.

### Phase 4: Backend API & Database
- [x] Configure SQLAlchemy engine and SQLite database (`stress_system.db`).
- [x] Define `User` and `Assessment` database models.
- [x] Define Pydantic v2 schemas (`auth.py`, `assessment.py`) with `model_config = ConfigDict(from_attributes=True)`.
- [x] Implement REST endpoints:
  - `POST /api/auth/register` & `POST /api/auth/login` (JWT + bcrypt).
  - `POST /api/facial/analyze` (Webcam frame + Grad-CAM + EAR).
  - `POST /api/behavioural/analyze` (8 lifestyle features + SHAP).
  - `POST /api/fusion/evaluate` (Multimodal fusion + persistence + recommendations).
  - `GET /api/history` & `GET /api/history/trends` (Recharts series).
  - `GET /api/history/benchmarks` (Empirical model comparison metrics).
- [x] Seed demo account (`demo@stressguard.edu` / `Demo@123`) with 8 multi-date historical assessments.

### Phase 5: Frontend Interface & Anti-Convergence Design
- [x] Bespoke typography pairing: Space Grotesk (headings), Plus Jakarta Sans (body), JetBrains Mono (metrics).
- [x] Implement fluid transitions with weighted editorial cubic-bezier easing (`cubic-bezier(0.16, 1, 0.3, 1)`).
- [x] Implement JWT authentication context (`AuthContext.jsx`) and protected route guards.
- [x] Implement responsive navigation header (`Navbar.jsx`) and non-diagnostic disclaimer footer (`Footer.jsx`).
- [x] Build webcam capture component (`WebcamCapture.jsx`) with live preview, exposure meter, and landmark guide.
- [x] Build 3-step questionnaire wizard (`QuestionnaireWizard.jsx`).
- [x] Build circular stress gauge (`StressGauge.jsx`) with dynamic color tokens (emerald, amber, rose).
- [x] Build SHAP horizontal diverging bar chart (`ShapChart.jsx`).
- [x] Build Grad-CAM saliency map viewer (`GradCamViewer.jsx`) with overlay and split modes.
- [x] Build categorized recommendation cards (`RecommendationCard.jsx`).
- [x] Implement all pages with responsive asymmetric layouts.

### Phase 6: Mobile-First & Vercel Production Optimization
- [x] Enforce mobile 360px viewport baseline, `100dvh` container sizing, and `overflow-x: hidden`.
- [x] Ensure minimum 44px tap targets for mobile usability (WCAG 2.5.5 / 2.5.8).
- [x] Enforce 16px minimum form inputs to prevent iOS automatic zoom on focus.
- [x] Implement dynamic route-level code-splitting with `React.lazy()` and `<Suspense>` across all pages.
- [x] Implement Rolldown functional `manualChunks` in `vite.config.js` isolating vendor-charts and vendor-icons.
- [x] Create `frontend/vercel.json` with SPA routing rewrites and immutable cache headers.
- [x] Create root `vercel.json` for smooth repository-level Vercel builds.
- [x] Create `frontend/.env.example` and `backend/.env.example` for environment variable configuration.
- [x] Add dynamic CORS support and `https://.*\.vercel\.app` regex in FastAPI backend.
- [x] Containerize backend with `backend/Dockerfile` and `docker-compose.yml`.

### Phase 7: Verification & Documentation
- [x] Run pytest test suite (6/6 tests passing in 9.00s).
- [x] Run Vite production bundle build (`npm run build` passing in 962ms with 0 warnings).
- [x] Write formal 12-chapter B.Tech major project report (`docs/BTech_Major_Project_Report.md`).
- [x] Write formal test cases matrix (`docs/testing_matrix.md`).
- [x] Update root `README.md` with Vercel deployment guide and mobile UX instructions.
- [x] Create one-click execution runner scripts (`run_backend.bat`, `run_frontend.bat`, `run_all.bat`).

### Phase 8: Systematic Bug Hunting, A11y Audit & LLM Council Review
- [x] Convened 4-member LLM advisory council (Architect, UI/UX Designer, Tech Lead, Security Auditor).
- [x] Resolved face-detection absence in multimodal fusion (blank frames now gracefully fall back to 100% behavioural).
- [x] Resolved unhandled client exception in `Assessment.jsx` when multimodal evaluation was triggered without taking a photo.
- [x] Added dedicated `GET /api/history/latest` endpoint preventing 422 errors on `/history/latest`.
- [x] Enforced WCAG 1.3.1 / 4.1.2 input label associations (`htmlFor`, `id`, `autoComplete`) across `Login.jsx` and `Register.jsx`.
- [x] Added `role="radiogroup"`, `role="radio"`, and `aria-checked` to Likert rating scales in `QuestionnaireWizard.jsx`.
- [x] Upgraded interactive table actions and auth submit buttons to minimum 44px tap targets (WCAG 2.5.5 / 2.5.8).
- [x] Added dialog modal semantics and Escape key listeners in `DisclaimerModal.jsx`.
- [x] Expanded automated test suite from 6 to 8 tests (100% passing in 8.70s).
- [x] Verified AI prose sanitization via `unslop 0.7.0`.

### Phase 9: Secure-Skill Hardening & Shannon Adversarial Penetration Testing
- [x] Multi-pass security audit conducted across Secrets, Database, Auth, Server Validation, Supply Chain, and Headers.
- [x] Created root `.gitignore` isolating `.env`, `*.db`, `venv/`, and `node_modules/`.
- [x] Injected security headers middleware into FastAPI (`nosniff`, `DENY`, `strict-origin-when-cross-origin`, `camera=(self)`).
- [x] Configured static security headers in `vercel.json` (root and `frontend/`).
- [x] Neutralized DoS decompression bomb risks in `decode_base64_image` with 6MB string limit and 1920px image dimension bounds.
- [x] Enforced `is_active` validation in `get_current_user` auth dependency.
- [x] Verified Broken Object-Level Authorization (BOLA/IDOR) tenant isolation via test suite.
- [x] Disabled production source maps in `frontend/vite.config.js`.
- [x] Verified zero npm vulnerabilities via `npm audit`.
- [x] Expanded automated test suite to 12 tests (100% passing in 10.32s).
- [x] Reconfigured and launched live frontend on port 5555 (`http://localhost:5555`) with backend on port 8000.

### Phase 10: Standalone Zero-npm Support & Clean Packaging
- [x] Created `serve_frontend.py` using Python standard library `http.server` with SPA rewrite to `frontend/dist/index.html`.
- [x] Verified zero-npm static serving on `http://localhost:5555` with successful 200 responses on both `/` and subroutes (`/dashboard`).
- [x] Built resilient `run_without_npm.bat` supporting auto-detection of `venv`, first-time dependency setup from root `requirements.txt`, concurrent server startup, and automated browser launch.
- [x] Generated root `requirements.txt` containing all runtime and ML dependencies.
- [x] Verified and executed full 12/12 automated pytest regression and security suite.
- [x] Packaged clean standalone ZIP archive: `Real_Time_Multimodal_Stress_Detection_System.zip` (4.49 MB, 113 files).
- [x] Verified ZIP excludes `venv/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`, and `.pyc` files while preserving all trained models, cascades, and compiled `frontend/dist`.

---

## Issues & Resolutions Log

1. **Issue**: OpenCV 5.0 preview wheel didn't bundle legacy Haar cascades in `cv2/data`.
   * **Root Cause**: `cv2.data.haarcascades` referenced an empty folder in this build.
   * **Resolution**: Downloaded official `haarcascade_frontalface_default.xml` and `haarcascade_eye.xml` directly into `backend/app/ml/cascades/` and referenced them locally.

2. **Issue**: Pytest failed on Pydantic `EmailStr` validation.
   * **Root Cause**: `email-validator` dependency was missing.
   * **Resolution**: Installed `email-validator>=2.3.0` into the virtual environment.

3. **Issue**: Python f-string syntax error in `recommender.py` (`{ear:.2f if ear else 'N/A'}`).
   * **Root Cause**: Inline ternary expression inside format specifier.
   * **Resolution**: Pre-formatted `ear_str = f"{ear:.2f}" if ear is not None else "N/A"`.

4. **Issue**: Class imbalance in initial synthetic dataset (High class was 2.1%).
   * **Root Cause**: High threshold was set at 0.68.
   * **Resolution**: Calibrated thresholds to Low (< 0.38), Moderate (0.38 - 0.52), High (> 0.52), yielding balanced distributions (46% Low, 33% Moderate, 21% High).

5. **Issue**: Vite 8 (Rolldown) build failed on object-based `manualChunks`.
   * **Root Cause**: Rolldown requires `manualChunks` to be a function `(id) => string | void`.
   * **Resolution**: Refactored `vite.config.js` to functional `manualChunks(id)` pattern.

6. **Issue**: Multimodal fusion incorporated false calm score when webcam frame had no face.
   * **Root Cause**: `facial_res` returned default calm emotion values when `face_detected` was false.
   * **Resolution**: Guarded `facial_score` and `facial_conf` in `fusion.py` to require `face_detected == True`; otherwise automatically triggers missing-modality fallback to behavioural-only.

7. **Issue**: Fast reload on `/results` or `/report/latest` showed empty screen when state was lost.
   * **Root Cause**: Client components relied strictly on in-memory React Router state.
   * **Resolution**: Created `GET /api/history/latest` endpoint and updated `Results.jsx` and `ReportView.jsx` to fetch the latest assessment if router state is absent.

8. **Issue**: Screen readers couldn't correlate labels with form inputs on auth pages.
   * **Root Cause**: Form `<label>` tags lacked `htmlFor` and `<input>` tags lacked `id`.
   * **Resolution**: Assigned matching identifiers and `autoComplete` attributes on all authentication and survey controls.

9. **Issue**: Missing root `.gitignore` risked accidental repository commit of virtual environment and database files.
   * **Root Cause**: `.gitignore` existed only inside `frontend/`.
   * **Resolution**: Created broad root `.gitignore` covering `venv/`, `*.db`, `.env`, and `node_modules/`.

10. **Issue**: Unchecked base64 frame input posed risk of memory exhaustion / decompression bomb attack.
    * **Root Cause**: `decode_base64_image` processed arbitrary string payloads without byte size boundaries.
    * **Resolution**: Enforced strict 6MB string length cap, 5MB decoded buffer limit, and automatic dimension downscaling for inputs exceeding 1920px.
   * **Resolution**: Refactored `vite.config.js` to functional `manualChunks(id)` pattern.
