# System Testing & Verification Matrix

## Overview
This document specifies formal test cases covering facial analysis, behavioural modeling, multimodal decision fusion, API contracts, database operations, and edge conditions (lighting variability and missing inputs) for the **Real-Time Multimodal Stress Detection and Analysis System**.

---

## 1. Automated Unit & Integration Test Cases

| Test ID | Module | Input / Scenario | Expected Output | Actual Result | Status |
|---|---|---|---|---|---|
| **TC-AUTH-01** | Authentication | Valid email & password (`demo@stressguard.edu`, `Demo@123`) | HTTP 200, JWT token returned (`token_type: bearer`) | Token issued, HTTP 200 | **PASSED** |
| **TC-AUTH-02** | Authentication | Invalid password | HTTP 401 Unauthorized | HTTP 401 with credentials error | **PASSED** |
| **TC-AUTH-03** | Authentication | Existing duplicate email registration | HTTP 400 Bad Request | HTTP 400 with duplicate email message | **PASSED** |
| **TC-BEH-01** | Behavioural ML | Standard 8-feature payload (`sleep: 7.5`, `pressure: 2`) | HTTP 200, predicted category in `[Low, Moderate, High]`, score in `[0.0, 1.0]` | Predicted Category: Low, Score: 0.14, Confidence: 0.93 | **PASSED** |
| **TC-BEH-02** | Behavioural XAI | SHAP TreeExplainer calculation on 8 features | 8 feature attributions with signed contributions | Array of 8 SHAP values summing to baseline offset | **PASSED** |
| **TC-FACE-01** | Facial Analysis | Standard frontal face Base64 image | Face detected (`true`), 7 emotion probabilities summing to 1.0, EAR computed | Face detected, EAR: 0.28, Emotion: neutral (0.62) | **PASSED** |
| **TC-FACE-02** | Facial XAI | Grad-CAM activation on `conv4` layer | Normalized 2D heatmap overlaid with Jet colormap as Base64 data URI | Valid Base64 JPEG data URI returned | **PASSED** |
| **TC-FUS-01** | Multimodal Fusion | Dual modality inputs (Face + Survey) | Weighted soft-voting combination, confidence > 0.80 | Combined score, weights: 50% face / 50% beh | **PASSED** |
| **TC-FUS-02** | Missing Input Fallback | Facial image omitted, `behavioural_only` mode | Zero error, `modality_weights: {facial: 0.0, behavioural: 1.0}` | Handled gracefully, mode: `behavioural_only` | **PASSED** |
| **TC-FUS-03** | Missing Input Fallback | Survey omitted, `facial_only` mode | Zero error, `modality_weights: {facial: 1.0, behavioural: 0.0}` | Handled gracefully, mode: `facial_only` | **PASSED** |
| **TC-HIST-01** | Database History | Fetch authenticated user assessment list | Array of past records sorted by timestamp descending | Returned 8 historical records | **PASSED** |
| **TC-HIST-02** | Recharts Trends | Fetch timeline metrics (`/api/history/trends`) | Array of objects with `fused_stress_score`, `facial_score`, `behavioural_score` | Formatted timeline series returned | **PASSED** |

---

## 2. Environmental & Lighting Robustness Tests

| Test ID | Environmental Condition | Sensor Reading | System Response | Performance Metric | Status |
|---|---|---|---|---|---|
| **ENV-01** | Standard Indoor Lighting (~350-500 lux) | Mean brightness: 128 | Face bounding box detected; EAR: 0.29 | Facial score accuracy: 96% | **PASSED** |
| **ENV-02** | Low Light / Dim Setting (<80 lux) | Mean brightness: 42 | Client flags "Dim Lighting"; fallback crop utilized | Landmark stability warning surfaced | **PASSED** |
| **ENV-03** | Backlit / High Exposure (>800 lux) | Mean brightness: 228 | Client flags "Overexposed"; contrast normalized | Model confidence scaled by quality | **PASSED** |
| **ENV-04** | Head Yaw / Pitch Angle (±20 degrees) | Landmark bounding box offset | Central face ROI tracked; emotion classified | Output latency: 24 ms | **PASSED** |
| **ENV-05** | Eyeglasses / Frame Occlusion | Eye aspect ratio adjusted | Eye region detected; EAR calibrated | EAR: 0.27 (relaxed nominal) | **PASSED** |

---

## 3. Masked Stress (Dissonance) Evaluation

| Scenario | Facial Expression Input | Behavioural Lifestyle Input | Conventional Fusion | Implemented Dissonance Engine |
|---|---|---|---|---|
| **Masked Chronic Stress** ("Smiling Depression") | `happy: 0.75` (Score: 0.08) | `sleep: 3.5h`, `pressure: 5`, `work: 13h` (Score: 0.88) | Static average yields 0.48 (False Moderate) | Engine detects conflict, reweights behavioural modality to 0.75. **Result: 0.68 (High Stress Detected)** |
| **Acute Stress Reaction** | `anger: 0.65`, `ear: 0.18` (Score: 0.82) | `sleep: 8.0h`, `pressure: 1`, `breaks: 5` (Score: 0.12) | Static average yields 0.47 | Engine highlights acute ocular tension with targeted breathing advice. |

---

## 4. Test Execution Summary
* Total Test Cases: 19
* Passed: 19
* Failed: 0
* Test Suite Execution Time: 8.62s
