# Architectural Discoveries & Technical Findings

## 1. Runtime Environment & Library Compatibility

* **Python Runtime**: Python 3.13.14 (Windows AMD64).
* **Deep Learning Framework**: PyTorch 2.15.0 with CPU execution.
  * Inference latency for `EmotionCNN`: **24 ms - 28 ms** per $112 \times 112$ RGB face crop.
  * Native PyTorch backward hook on `conv4` (256 channels) generates deterministic Grad-CAM heatmaps without Keras version conflicts.
* **Computer Vision**: OpenCV 5.0.0.93.
  * Haar cascades located at `backend/app/ml/cascades/haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`.
* **Tabular ML**: Scikit-Learn 1.9.1 and XGBoost 3.4.1.
  * Support Vector Machine with RBF kernel and calibrated probabilities achieved optimal F1-score (83.01%) and multi-class ROC-AUC (0.9562).
  * SHAP 0.54.1 `TreeExplainer` fitted on Random Forest delivers sub-5ms feature attribution vectors.

---

## 2. API Signatures & Schemas

### Facial Inference (`POST /api/facial/analyze`)
* **Request**:
  ```json
  {
    "image_base64": "data:image/jpeg;base64,...",
    "client_ear": 0.28,
    "client_blink_rate": 18.0
  }
  ```
* **Response**:
  ```json
  {
    "face_detected": true,
    "dominant_emotion": "neutral",
    "emotion_probabilities": {
      "neutral": 0.62,
      "happy": 0.15,
      "sad": 0.08,
      "surprise": 0.05,
      "fear": 0.04,
      "disgust": 0.03,
      "anger": 0.03
    },
    "eye_aspect_ratio": 0.28,
    "facial_stress_score": 0.22,
    "gradcam_base64": "data:image/jpeg;base64,...",
    "confidence": 0.88,
    "message": "Face analyzed successfully"
  }
  ```

### Behavioural Lifestyle Inference (`POST /api/behavioural/analyze`)
* **Request**:
  ```json
  {
    "sleep_hours": 7.5,
    "screen_time_hours": 6.0,
    "work_study_hours": 7.0,
    "academic_work_pressure": 2,
    "physical_activity_mins": 45,
    "break_frequency": 4,
    "self_reported_mood": 4,
    "perceived_stress_level": 2
  }
  ```
* **Response**:
  ```json
  {
    "predicted_category": "Low",
    "stress_score": 0.14,
    "probabilities": { "Low": 0.86, "Moderate": 0.11, "High": 0.03 },
    "shap_contributions": [
      { "feature": "academic_work_pressure", "display_name": "Academic/Work Pressure", "value": 2.0, "shap_value": -0.06 }
    ],
    "model_used": "RandomForest",
    "confidence": 0.86
  }
  ```

### Multimodal Fusion (`POST /api/fusion/evaluate`)
* Supports `modality_mode`: `"multimodal"`, `"facial_only"`, or `"behavioural_only"`.
* Employs soft voting: $S_{\text{fused}} = (w_{\text{face}} \cdot S_{\text{face}}) + (w_{\text{beh}} \cdot S_{\text{beh}})$.
* Enforces dissonance reweighting (75% behavioural) if chronic sleep/workload strain is masked by a smiling face.

---

## 3. Port & Host Constraints

* **Port 5173 Exclusivity**: Port 5173 is reserved exclusively for Daily Tracker.
* **Frontend**: Bound to **port 5555** in `frontend/vite.config.js`.
* **Backend**: Bound to **port 8000** (`127.0.0.1:8000`), with CORS whitelisting port 5555 and 5174.

---

## 4. Deployment and Hosting Architecture

* **Frontend on Vercel**:
  - `frontend/vercel.json` and root `vercel.json` configure client-side SPA routing (`/(.*) -> /index.html`) and static asset immutable caching.
  - Route-level lazy loading (`React.lazy()` with `<Suspense>`) splits all 8 pages into individual bundles (<27 kB each).
  - Rolldown `manualChunks` in `vite.config.js` extracts `vendor-charts` (Recharts) and `vendor-icons` (Lucide), preserving small initial bundle loads.
  - Environment variable `VITE_API_URL` dynamically points to the deployed FastAPI backend.

---

## 5. Standalone Zero-npm Serving & Distribution

* **Standard Library Static File Server (`serve_frontend.py`)**:
  - Uses standard library `http.server.SimpleHTTPRequestHandler` combined with `socketserver.TCPServer`.
  - Serves static assets from `frontend/dist/`.
  - Rewrites non-asset requests (e.g., `/dashboard`, `/results`, `/benchmarks`) to `/index.html` to enable React Router single-page application routing without Node.js, Vite, or npm.
  - Verifiable on port 5555 (`http://localhost:5555`).
* **Standalone Zip Distribution**:
  - Clean archive `Real_Time_Multimodal_Stress_Detection_System.zip` packaged at 4.49 MB (15.92 MB uncompressed, 113 files).
  - Contains fully compiled frontend build in `frontend/dist/`, complete backend codebase, SQLite database with seeded demo history, trained model weights (`.pt`, `.joblib`), OpenCV cascades, documentation, and automated startup batch files.
  - Excludes machine-dependent virtual environments (`venv/`), development cache folders (`.pytest_cache/`, `__pycache__/`), and unneeded node modules (`node_modules/`).

* **Backend Cloud Support**:
  - Dynamic CORS handling via `CORS_ORIGINS` environment variable and regex `https://.*\.vercel\.app` enables any Vercel preview or production deployment to connect without CORS errors.
  - `Dockerfile` containerizes the Python 3.11/FastAPI backend with OpenCV runtime dependencies (`libgl1-mesa-glx`, `libglib2.0-0`, `libgomp1`).
  - Pytest runs 12 automated integration and security tests with 0 deprecation warnings.

---

## 5. Security Posture & Adversarial Testing Results (Shannon & Secure-Skill)

* **Broken Object-Level Authorization (BOLA / IDOR)**:
  - Validated tenant isolation: User B querying User A's `assessment_id` receives HTTP 404.
  - Query filtering strictly predicates on `Assessment.user_id == current_user.id`.
* **Resource Exhaustion & Decompression Bomb Defense**:
  - Image base64 inputs capped at 6MB string length and 5MB decoded bytes.
  - Decompression dimension ceiling enforced at 1920px with automatic proportional downscaling.
* **Security Headers & Clickjacking Protection**:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy: camera=(self)`
* **Supply Chain & Source Maps**:
  - Production source maps disabled (`sourcemap: false`) in Vite build.
  - `npm audit` reports 0 vulnerabilities.
  - Secrets and local databases isolated via root `.gitignore`.
