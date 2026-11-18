import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette Constants (Modern AI/ML Dark Theme)
# -----------------------------------------------------------------------------
BG_COLOR = RGBColor(15, 23, 42)        # Slate 900 #0F172A
CARD_BG = RGBColor(30, 41, 59)        # Slate 800 #1E293B
CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700 #334155
CARD_BG_LIGHT = RGBColor(22, 32, 50)  # Darker container

COLOR_CYAN = RGBColor(56, 189, 248)    # Sky 400 #38BDF8
COLOR_BLUE = RGBColor(59, 130, 246)    # Blue 500 #3B82F6
COLOR_PURPLE = RGBColor(168, 85, 247)  # Purple 500 #A855F7
COLOR_EMERALD = RGBColor(52, 211, 153) # Emerald 400 #34D399
COLOR_AMBER = RGBColor(251, 191, 36)   # Amber 400 #FBBF24
COLOR_ROSE = RGBColor(248, 113, 113)   # Rose 400 #F87171

TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_LIGHT = RGBColor(241, 245, 249)   # Slate 100
TEXT_MUTED = RGBColor(148, 163, 184)   # Slate 400
TEXT_DIM = RGBColor(100, 116, 139)     # Slate 500

FONT_MAIN = "Calibri"
FONT_HEADING = "Segoe UI"

ASSETS_DIR = Path("generated_assets")

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background() # no line

    def add_header(slide, title, subtitle, slide_num, badge_text="TECHNICAL EVALUATION"):
        # Header category badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.5), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(14, 116, 144) # cyan-dark
        badge.line.color.rgb = COLOR_CYAN
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(8.5)
        p_b.font.bold = True
        p_b.font.color.rgb = TEXT_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        # Slide number badge (top right)
        num_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.35), Inches(1.8), Inches(0.35))
        tf_n = num_box.text_frame
        tf_n.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_n = tf_n.paragraphs[0]
        p_n.text = f"Slide {slide_num} of 20"
        p_n.font.name = FONT_MAIN
        p_n.font.size = Pt(10)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_CYAN
        p_n.alignment = PP_ALIGN.RIGHT

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.8), Inches(0.6))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Subtitle
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.8), Inches(0.4))
        tf_s = tb_sub.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = FONT_MAIN
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = COLOR_CYAN

        # Header accent separator line
        sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.72), Inches(11.733), Inches(0.02))
        sep.fill.solid()
        sep.fill.fore_color.rgb = CARD_BORDER
        sep.line.fill.background()

    def add_card(slide, left, top, width, height, title=None, title_color=COLOR_CYAN, border_color=CARD_BORDER, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.12), Inches(width - 0.3), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_HEADING
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Decorative header tag
    tag = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(4.2), Inches(0.38))
    tag.fill.solid()
    tag.fill.fore_color.rgb = RGBColor(14, 116, 144)
    tag.line.color.rgb = COLOR_CYAN
    tag.line.width = Pt(1.2)
    tf_tag = tag.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "B.TECH CSE MAJOR PROJECT EVALUATION"
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = TEXT_WHITE
    p_tag.alignment = PP_ALIGN.CENTER

    # Project Title
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(1.5))
    tf_main = t_box.text_frame
    tf_main.word_wrap = True
    p1 = tf_main.paragraphs[0]
    p1.text = "Real-Time Multimodal Stress Detection and Analysis System"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    # Subtitle
    s_box = slide1.shapes.add_textbox(Inches(0.8), Inches(2.85), Inches(11.7), Inches(0.8))
    tf_sub = s_box.text_frame
    tf_sub.word_wrap = True
    p2 = tf_sub.paragraphs[0]
    p2.text = "An AI-powered system integrating facial analysis and behavioural assessment for stress detection."
    p2.font.name = FONT_MAIN
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_CYAN

    # Team Box (Prominently featured)
    add_card(slide1, 0.8, 3.8, 6.6, 2.9, title="PROJECT TEAM MEMBERS", title_color=COLOR_CYAN)
    team_members = [
        ("Tarandeep Kaur", "23052441", "B.Tech Computer Science & Engineering"),
        ("Sakshi Agarwal", "23051776", "B.Tech Computer Science & Engineering"),
        ("Shatakshi Dasgupta", "23052425", "B.Tech Computer Science & Engineering"),
        ("Swasti Suman", "23051552", "B.Tech Computer Science & Engineering"),
        ("Swastika Chatterjee", "23053315", "B.Tech Computer Science & Engineering"),
    ]
    tb_team = slide1.shapes.add_textbox(Inches(0.95), Inches(4.3), Inches(6.3), Inches(2.3))
    tf_t = tb_team.text_frame
    tf_t.word_wrap = True
    for i, (name, reg, dept) in enumerate(team_members):
        p = tf_t.add_paragraph() if i > 0 else tf_t.paragraphs[0]
        p.text = f"•  {name}  —  Reg. No: {reg}  ({dept})"
        p.font.name = FONT_MAIN
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(4)

    # Project Highlights / Tech Pillars Box (Right)
    add_card(slide1, 7.6, 3.8, 4.9, 2.9, title="CORE ARCHITECTURAL PILLARS", title_color=COLOR_PURPLE)
    tb_pil = slide1.shapes.add_textbox(Inches(7.8), Inches(4.3), Inches(4.5), Inches(2.3))
    tf_p = tb_pil.text_frame
    tf_p.word_wrap = True
    pillars = [
        ("Dual-Stream Sensing", "Computer vision (webcam) + 8-factor lifestyle survey"),
        ("Ocular Fatigue Tracking", "Eye Aspect Ratio (EAR) for eyelid drooping detection"),
        ("Deep Vision CNN", "PyTorch 3-block CNN classifying 7 emotion probabilities"),
        ("Supervised ML Classifier", "Calibrated SVM achieving 83.67% accuracy & 83.01% F1"),
        ("Explainable AI (XAI)", "SHAP TreeExplainer attributions + Grad-CAM heatmaps"),
        ("Adaptive Fusion Engine", "Confidence weighting + Dissonance / Masked-stress override"),
    ]
    for i, (head, desc) in enumerate(pillars):
        p = tf_p.add_paragraph() if i > 0 else tf_p.paragraphs[0]
        p.text = f"✔  {head}: {desc}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(3)

    # -------------------------------------------------------------------------
    # SLIDE 2: Problem Statement and Motivation
    # -------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Problem Statement and Motivation",
               "Why Multimodal Stress Detection Overcomes the Fatal Flaws of Unimodal Systems", 2, "PROBLEM CONTEXT")

    # Card 1: The Context & Importance
    add_card(slide2, 0.8, 1.9, 3.7, 4.9, title="1. Student & Workplace Stress Crisis", title_color=COLOR_CYAN)
    tb2_1 = slide2.shapes.add_textbox(Inches(0.95), Inches(2.4), Inches(3.4), Inches(4.2))
    tf2_1 = tb2_1.text_frame
    tf2_1.word_wrap = True
    c1_pts = [
        "High Cognitive Burden: Academic pressure, tight deadlines, and extended screen exposure lead to chronic stress, executive dysfunction, and burnout.",
        "Health & Mental Well-being: Unmanaged stress causes sleep disorders, anxiety, memory consolidation deficits, and somatic illnesses.",
        "Need for Early Screening: Identifying early physiological and behavioural stress markers enables timely, non-invasive wellness interventions before escalation."
    ]
    for i, pt in enumerate(c1_pts):
        p = tf2_1.add_paragraph() if i > 0 else tf2_1.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Card 2: Pitfalls of Unimodal Solutions
    add_card(slide2, 4.8, 1.9, 3.8, 4.9, title="2. Vulnerability of Unimodal Systems", title_color=COLOR_ROSE)
    tb2_2 = slide2.shapes.add_textbox(Inches(4.95), Inches(2.4), Inches(3.5), Inches(4.2))
    tf2_2 = tb2_2.text_frame
    tf2_2.word_wrap = True
    c2_pts = [
        "Self-Reporting Pitfalls: Questionnaires suffer from acute recall bias, subjective minimization/denial, social desirability bias, and lack real-time physiological grounding.",
        "Facial Vision Blindspots ('Smiling Depression'): Socially compliant or professional smiling masks acute internal cognitive strain. Transient expressions do not reflect chronic fatigue.",
        "Wearable Hardware Drawbacks: PPG, ECG, EEG, and GSR sensors require physical skin contact, causing user discomfort, skin irritation, and workflow disruption."
    ]
    for i, pt in enumerate(c2_pts):
        p = tf2_2.add_paragraph() if i > 0 else tf2_2.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(10)

    # Card 3: Our Multimodal Solution
    add_card(slide2, 8.9, 1.9, 3.6, 4.9, title="3. The Proposed Multimodal Paradigm", title_color=COLOR_EMERALD)
    tb2_3 = slide2.shapes.add_textbox(Inches(9.05), Inches(2.4), Inches(3.3), Inches(4.2))
    tf2_3 = tb2_3.text_frame
    tf2_3.word_wrap = True
    c3_pts = [
        "Cross-Modal Validation: Fusing real-time visual biomarkers (eyelid fatigue + emotion valence) with contextual lifestyle data (sleep, workload, screen time).",
        "Dissonance Resolution: Specifically engineered to detect conflicts—such as a smiling face under 3 hours of sleep and high academic pressure.",
        "Privacy-Preserving & Zero Hardware: Operates using existing commodity webcams; video frames are processed strictly in RAM and discarded immediately.",
        "Explainable AI: Integrates SHAP and Grad-CAM so users and clinicians understand the rationale behind every assessment."
    ]
    for i, pt in enumerate(c3_pts):
        p = tf2_3.add_paragraph() if i > 0 else tf2_3.paragraphs[0]
        p.text = f"✔ {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 3: Proposed Solution and System Overview
    # -------------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Proposed Solution and System Overview",
               "Dual-Stream Non-Invasive Stress Screening with Decision-Level Fusion & XAI", 3, "SYSTEM CONCEPT")

    # 3 High-level concept cards
    add_card(slide3, 0.8, 1.9, 3.7, 2.5, title="MODALITY 1: FACIAL & OCULAR STREAM", title_color=COLOR_CYAN)
    tb3_1 = slide3.shapes.add_textbox(Inches(0.95), Inches(2.35), Inches(3.4), Inches(1.9))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True
    m1_pts = [
        "Webcam Ingestion: Non-invasive, standard laptop camera snapshot.",
        "OpenCV Haar Cascades: Face ROI & ocular region isolation.",
        "Eye Aspect Ratio (EAR): Real-time eyelid fatigue & squint detection.",
        "EmotionCNN (PyTorch): 7-class emotion probabilities (<28ms CPU latency)."
    ]
    for i, pt in enumerate(m1_pts):
        p = tf3_1.add_paragraph() if i > 0 else tf3_1.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(3)

    add_card(slide3, 4.8, 1.9, 3.8, 2.5, title="MODALITY 2: BEHAVIOURAL LIFESTYLE", title_color=COLOR_PURPLE)
    tb3_2 = slide3.shapes.add_textbox(Inches(4.95), Inches(2.35), Inches(3.5), Inches(1.9))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True
    m2_pts = [
        "8 Validated Factors: Sleep, screen time, study duration, pressure, activity, breaks, mood, perceived stress.",
        "Pydantic Validation: Strict boundary & schema integrity checks.",
        "StandardScaler: Normalizes input distribution against training baseline.",
        "Supervised ML (SVM): Optimal multi-class calibrated probability output."
    ]
    for i, pt in enumerate(m2_pts):
        p = tf3_2.add_paragraph() if i > 0 else tf3_2.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(3)

    add_card(slide3, 8.9, 1.9, 3.6, 2.5, title="SYNTHESIS & EXPLAINABILITY", title_color=COLOR_EMERALD)
    tb3_3 = slide3.shapes.add_textbox(Inches(9.05), Inches(2.35), Inches(3.3), Inches(1.9))
    tf3_3 = tb3_3.text_frame
    tf3_3.word_wrap = True
    m3_pts = [
        "Decision Fusion: Confidence-weighted soft voting + Dissonance override.",
        "Categorization: Low (<0.38), Moderate (0.38-0.52), High (>0.52).",
        "Dual XAI: SHAP feature bars + Grad-CAM attention heatmaps.",
        "Targeted Interventions: Actionable wellness protocols mapped to root causes."
    ]
    for i, pt in enumerate(m3_pts):
        p = tf3_3.add_paragraph() if i > 0 else tf3_3.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(3)

    # Bottom Full-width High-Level Workflow diagram box
    add_card(slide3, 0.8, 4.6, 11.7, 2.3, title="HIGH-LEVEL SYSTEM WORKFLOW DIAGRAM", title_color=COLOR_AMBER)
    # Draw flowchart steps horizontally inside card
    flow_steps = [
        ("1. User Input", "Webcam Frame &\n8-Item Survey", COLOR_CYAN),
        ("2. Feature Extraction", "Face ROI + EAR &\nScaled Survey Vector", COLOR_BLUE),
        ("3. Model Inference", "EmotionCNN (PyTorch)\n& SVM (Scikit-Learn)", COLOR_PURPLE),
        ("4. Decision Fusion", "Confidence Weighting\n& Dissonance Check", COLOR_EMERALD),
        ("5. Output & XAI", "Stress Tier, SHAP,\nGrad-CAM & Advice", COLOR_AMBER)
    ]
    for i, (stitle, sdesc, col) in enumerate(flow_steps):
        x_pos = 1.05 + i * 2.3
        s_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_pos), Inches(5.1), Inches(2.05), Inches(1.55))
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = CARD_BG_LIGHT
        s_box.line.color.rgb = col
        s_box.line.width = Pt(1.2)
        tf_s = s_box.text_frame
        tf_s.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_st = tf_s.paragraphs[0]
        p_st.text = stitle
        p_st.font.name = FONT_HEADING
        p_st.font.size = Pt(9.5)
        p_st.font.bold = True
        p_st.font.color.rgb = col
        p_st.alignment = PP_ALIGN.CENTER
        p_sd = tf_s.add_paragraph()
        p_sd.text = sdesc
        p_sd.font.name = FONT_MAIN
        p_sd.font.size = Pt(8.5)
        p_sd.font.color.rgb = TEXT_LIGHT
        p_sd.alignment = PP_ALIGN.CENTER

        if i < len(flow_steps) - 1:
            arr = slide3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x_pos + 2.08), Inches(5.75), Inches(0.18), Inches(0.2))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_CYAN
            arr.line.fill.background()

    # -------------------------------------------------------------------------
    # SLIDE 4: Technology Stack and Development Environment
    # -------------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Technology Stack and Development Environment",
               "Architectural Allocation Across Frontend, Backend, Machine Learning & Security Layers", 4, "TECH STACK")

    # 4 Columns for Tech Stack
    tech_cols = [
        ("FRONTEND LAYER", COLOR_CYAN, [
            ("React 19", "Single-Page Application (SPA) architecture with concurrent rendering and declarative UI components."),
            ("Vite (Port 5555)", "Next-generation build tool providing sub-second Hot Module Replacement (HMR)."),
            ("Tailwind CSS v4", "Utility-first design token styling delivering a responsive, dark-mode medical interface."),
            ("Recharts", "SVG-based hardware-accelerated time-series visualization for longitudinal stress tracking."),
            ("Axios Client", "Promise-based HTTP client with Bearer token request/response interceptors.")
        ]),
        ("BACKEND ENGINE", COLOR_BLUE, [
            ("Python 3.13 / 3.14", "Modern high-performance asynchronous runtime for mathematical computation."),
            ("FastAPI", "High-throughput asynchronous ASGI web framework with automatic OpenAPI documentation."),
            ("Uvicorn (Port 8000)", "Lightning-fast ASGI server execution handling concurrent client streams."),
            ("Pydantic v2", "Strict schema validation enforcing runtime type safety and input boundary constraints."),
            ("REST Architecture", "Stateless, decoupled endpoints for modular facial, survey, and fusion evaluation.")
        ]),
        ("ML & COMPUTER VISION", COLOR_PURPLE, [
            ("PyTorch 2.15", "Deep learning framework executing EmotionCNN inference & backward autograd hooks."),
            ("Scikit-Learn 1.9", "Supervised classification (SVM, RF, LogReg), StandardScaler, and StratifiedKFold."),
            ("OpenCV 5.0", "Haar Cascades for face and ocular bounding box detection; in-memory frame decoding."),
            ("SHAP 0.54", "TreeExplainer calculating exact game-theoretic feature attribution on survey factors."),
            ("Grad-CAM", "Targeted gradient activation mapping on final conv layer visualizing attention.")
        ]),
        ("DATABASE & SECURITY", COLOR_EMERALD, [
            ("SQLite Database", "Serverless, zero-configuration ACID transactional persistence (stress_system.db)."),
            ("SQLAlchemy ORM", "Declarative schema modeling with JSON feature support for historical assessments."),
            ("JWT (JSON Web Tokens)", "Stateless authentication with cryptographically signed Bearer tokens."),
            ("Passlib & Bcrypt", "Salted, irreversible password hashing protecting user account credentials."),
            ("Pytest (12 Suites)", "Automated testing covering BOLA defense, fallbacks, and boundary assertions.")
        ])
    ]

    for i, (col_title, col_color, items) in enumerate(tech_cols):
        left_pos = 0.8 + i * 2.98
        add_card(slide4, left_pos, 1.9, 2.85, 4.9, title=col_title, title_color=col_color)
        tb = slide4.shapes.add_textbox(Inches(left_pos + 0.12), Inches(2.4), Inches(2.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, (tech, desc) in enumerate(items):
            p1 = tf.add_paragraph() if j > 0 else tf.paragraphs[0]
            p1.text = f"▪ {tech}"
            p1.font.name = FONT_HEADING
            p1.font.size = Pt(9.5)
            p1.font.bold = True
            p1.font.color.rgb = col_color
            p2 = tf.add_paragraph()
            p2.text = desc
            p2.font.name = FONT_MAIN
            p2.font.size = Pt(8.5)
            p2.font.color.rgb = TEXT_LIGHT
            p2.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 5: Complete System Architecture (CRITICAL SLIDE)
    # -------------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Complete System Architecture",
               "Comprehensive End-to-End Pipeline: Ingestion, ML Processing, Fusion, and Persistence", 5, "CORE ARCHITECTURE")

    # Insert Architecture Chart Image
    arch_chart_path = ASSETS_DIR / "chart_system_architecture.png"
    if arch_chart_path.exists():
        slide5.shapes.add_picture(str(arch_chart_path), Inches(0.8), Inches(1.85), Inches(11.733), Inches(5.1))
    else:
        # Fallback card if chart missing
        add_card(slide5, 0.8, 1.85, 11.733, 5.1, title="SYSTEM ARCHITECTURE DIAGRAM", title_color=COLOR_CYAN)

    # -------------------------------------------------------------------------
    # SLIDE 6: Frontend Implementation and User Interaction
    # -------------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Frontend Implementation and User Interaction",
               "Single-Page Application (SPA) with Real-Time Sensory Feedback and Interactive Analytics", 6, "FRONTEND ARCHITECTURE")

    # 4 Feature Cards
    f_cards = [
        ("1. Authentication & Security Guard", COLOR_CYAN, [
            "Stateless Session: JWT Bearer tokens persisted in React Context with Axios authorization interceptors.",
            "Protected Route Wrapper: Unauthenticated attempts to access /dashboard or /assessment redirect to /login.",
            "Evaluation Auto-Fill: 1-click credential auto-fill (demo@stressguard.edu / Demo@123) for seamless faculty viva demonstration."
        ]),
        ("2. Interactive Assessment Wizard", COLOR_BLUE, [
            "Live Camera Stream: HTML5 video element with real-time ambient lighting quality detection (<80 lux alert).",
            "Ocular Feedback: Client-side Eye Aspect Ratio (EAR) indicator tracking blink frequency and eye openness.",
            "3-Step Survey: Ergonomic slider questionnaire collecting 8 validated lifestyle parameters with boundary validation."
        ]),
        ("3. Explainable Results Dashboard", COLOR_PURPLE, [
            "Speedometer Gauge: Dynamic SVG stress gauge visualizing Low (<0.38), Moderate (0.38-0.52), and High (>0.52).",
            "Emotion Probabilities: Horizontal bar chart displaying all 7 facial emotion distribution percentages.",
            "Dual XAI Displays: Interactive SHAP horizontal bar chart and Grad-CAM facial activation overlay."
        ]),
        ("4. Longitudinal History & Reporting", COLOR_EMERALD, [
            "14-Day Timeline (Recharts): Interactive area/line charts showing historical stress trends and modality balance.",
            "Detailed Assessment History: Audit log of past assessments with modality breakdown and user notes.",
            "Institutional Report View: Printable assessment report with clinical disclaimers ready for academic review."
        ])
    ]

    for i, (title, color, bullets) in enumerate(f_cards):
        row = i // 2
        col = i % 2
        left = 0.8 + col * 5.95
        top = 1.9 + row * 2.55
        add_card(slide6, left, top, 5.75, 2.4, title=title, title_color=color)
        tb = slide6.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.45), Inches(5.45), Inches(1.85))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, b in enumerate(bullets):
            p = tf.add_paragraph() if j > 0 else tf.paragraphs[0]
            p.text = f"• {b}"
            p.font.name = FONT_MAIN
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 7: Facial Analysis – Implementation Workflow
    # -------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Facial Analysis – Implementation Workflow",
               "Sub-30ms Computer Vision Pipeline: Acquisition, ROI Detection, Emotion Inference & Grad-CAM", 7, "FACIAL PIPELINE")

    # 8-step process flowchart displayed as cards across 2 rows of 4
    stages = [
        ("Stage 1: Frame Capture", "HTML5 Video element captures 640x480 webcam frame; encoded as Base64 JPEG data URI.", COLOR_CYAN),
        ("Stage 2: Safe Ingestion", "In-memory decoding via OpenCV; size ceiling (<5MB) and dimension ceiling (1920px) enforced.", COLOR_BLUE),
        ("Stage 3: Face Detection", "OpenCV Haar Cascade (haarcascade_frontalface_default.xml) detects face ROI (scale=1.1, minNeighbors=5).", COLOR_PURPLE),
        ("Stage 4: Fallback Handler", "If face undetected due to low lighting, central crop fallback is utilized with -0.10 confidence penalty.", COLOR_AMBER),
        ("Stage 5: EAR Calculation", "Haar eye cascade detects ocular regions in upper face half; computes bounding aspect ratio scaled by 0.55.", COLOR_ROSE),
        ("Stage 6: CNN Preprocessing", "Face ROI resized to 112x112 RGB, normalized with ImageNet mean/std; tensor fed to EmotionCNN.", COLOR_CYAN),
        ("Stage 7: Emotion Inference", "Forward pass executes in 24-28ms; Softmax layer generates probabilities across 7 emotion classes.", COLOR_BLUE),
        ("Stage 8: Stress Score & XAI", "Computes S_face = 0.75*Emotions + 0.25*EAR; hooks on conv4 generate Grad-CAM visual attention map.", COLOR_EMERALD)
    ]

    for i, (stitle, sdesc, scol) in enumerate(stages):
        row = i // 4
        col = i % 4
        left = 0.8 + col * 2.98
        top = 1.9 + row * 2.5
        add_card(slide7, left, top, 2.85, 2.35, title=stitle, title_color=scol)
        tb = slide7.shapes.add_textbox(Inches(left + 0.12), Inches(top + 0.45), Inches(2.6), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = sdesc
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT

    # Bottom summary ribbon
    ribbon = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.4))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = CARD_BG_LIGHT
    ribbon.line.color.rgb = COLOR_CYAN
    ribbon.line.width = Pt(1)
    tf_r = ribbon.text_frame
    tf_r.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_r = tf_r.paragraphs[0]
    p_r.text = "OUTPUT CONTRACT: { face_detected: bool, dominant_emotion: str, emotion_probabilities: dict, ear: float, facial_stress_score: float, gradcam_base64: str }"
    p_r.font.name = FONT_MAIN
    p_r.font.size = Pt(8.5)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_CYAN
    p_r.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------------------
    # SLIDE 8: Eye Aspect Ratio (EAR) and Facial Feature Analysis
    # -------------------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Eye Aspect Ratio (EAR) and Facial Feature Analysis",
               "Quantifying Ocular Fatigue and Eyelid Dynamic Tracking Without Specialized Sensors", 8, "OCULAR METRICS")

    # Left: Explanation Card
    add_card(slide8, 0.8, 1.9, 5.0, 5.1, title="EAR FORMULATION & COGNITIVE LOGIC", title_color=COLOR_CYAN)
    tb8 = slide8.shapes.add_textbox(Inches(0.95), Inches(2.4), Inches(4.7), Inches(4.4))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    ear_pts = [
        ("Theoretical Foundation", "Adapted from Soukupová & Čech (2016). Measures the ratio of vertical eyelid aperture relative to horizontal ocular fissure width."),
        ("Implemented Formula", "EAR = (height / width) * 0.55 derived from detected Haar ocular bounding boxes in the upper facial region."),
        ("Nominal Relaxed Baseline", "EAR in range [0.28, 0.35] represents normal alert, non-fatigued cognitive baseline (strain contribution: 0.00)."),
        ("Fatigue / Drooping Eyelids (EAR < 0.22)", "Indicates drowsiness, blink lag, or severe eye strain. Triggers strain penalty:\nStrain = min(0.35, (0.22 - EAR) * 2.5)."),
        ("Hyper-Vigilance / Squinting (EAR > 0.38)", "Wide-eyed cognitive tension or intense squinting triggers elevated strain:\nStrain = min(0.20, (EAR - 0.38) * 1.5)."),
        ("Multimodal Contribution", "EAR modulates the facial stress score by 25%, preventing false negatives when users display a neutral expression despite heavy ocular fatigue.")
    ]
    for i, (hd, text) in enumerate(ear_pts):
        p1 = tf8.add_paragraph() if i > 0 else tf8.paragraphs[0]
        p1.text = f"▪ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_CYAN
        p2 = tf8.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(3)

    # Right: Chart Image
    ear_chart_path = ASSETS_DIR / "chart_ear_analysis.png"
    if ear_chart_path.exists():
        slide8.shapes.add_picture(str(ear_chart_path), Inches(6.0), Inches(1.9), Inches(6.533), Inches(5.1))

    # -------------------------------------------------------------------------
    # SLIDE 9: EmotionCNN – Model Implementation
    # -------------------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "EmotionCNN – Model Implementation",
               "Lightweight 3-Block PyTorch CNN Delivering Sub-30ms CPU Inference for 7 Emotion Classes", 9, "DEEP LEARNING")

    # Top: Chart Image
    cnn_chart_path = ASSETS_DIR / "chart_cnn_architecture.png"
    if cnn_chart_path.exists():
        slide9.shapes.add_picture(str(cnn_chart_path), Inches(0.8), Inches(1.85), Inches(11.733), Inches(3.2))

    # Bottom: 3 Cards Explaining Architecture, Weights, and Decoupling
    add_card(slide9, 0.8, 5.15, 3.8, 1.9, title="1. ARCHITECTURAL SPECIFICATIONS", title_color=COLOR_CYAN)
    tb9_1 = slide9.shapes.add_textbox(Inches(0.95), Inches(5.55), Inches(3.5), Inches(1.4))
    tf9_1 = tb9_1.text_frame
    tf9_1.word_wrap = True
    c_pts1 = [
        "Input: 112x112 RGB normalized with ImageNet mean/std.",
        "3 Conv Blocks: (32->64), (128), (256 filters) with BatchNorm2d, MaxPool2d(2x2), and Dropout (0.2-0.3).",
        "Target Layer: conv4 (256 channels) is hooked for Grad-CAM.",
        "Classifier Head: AdaptiveAvgPool2d -> FC(256->128) -> Dropout(0.4) -> FC(128->7) -> Softmax."
    ]
    for i, pt in enumerate(c_pts1):
        p = tf9_1.add_paragraph() if i > 0 else tf9_1.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT

    add_card(slide9, 4.8, 5.15, 3.8, 1.9, title="2. VALENCE-AROUSAL WEIGHTS", title_color=COLOR_PURPLE)
    tb9_2 = slide9.shapes.add_textbox(Inches(4.95), Inches(5.55), Inches(3.5), Inches(1.4))
    tf9_2 = tb9_2.text_frame
    tf9_2.word_wrap = True
    c_pts2 = [
        "Anger (0.95) & Fear (0.90): High-arousal negative valence.",
        "Disgust (0.75) & Sadness (0.70): Negative emotional state.",
        "Surprise (0.30): Moderate arousal, context-dependent.",
        "Neutral (0.15) & Happy (0.02): Low/protective stress weights.",
        "Formula: S_emotion = sum(Weight_i * Prob_i)."
    ]
    for i, pt in enumerate(c_pts2):
        p = tf9_2.add_paragraph() if i > 0 else tf9_2.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT

    add_card(slide9, 8.8, 5.15, 3.733, 1.9, title="3. EMOTION-STRESS DECOUPLING", title_color=COLOR_EMERALD)
    tb9_3 = slide9.shapes.add_textbox(Inches(8.95), Inches(5.55), Inches(3.4), Inches(1.4))
    tf9_3 = tb9_3.text_frame
    tf9_3.word_wrap = True
    c_pts3 = [
        "Key Engineering Insight: Emotions alone do not equate to medical stress. Negative expressions indicate acute tension.",
        "Ocular Blending: Raw Score = (0.75 * S_emotion) + (0.25 * EAR_strain).",
        "Confidence Metric: Scaled dynamically based on the winning emotion certainty: Conf = min(0.98, max(0.60, P_max + 0.15))."
    ]
    for i, pt in enumerate(c_pts3):
        p = tf9_3.add_paragraph() if i > 0 else tf9_3.paragraphs[0]
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT

    # -------------------------------------------------------------------------
    # SLIDE 10: Behavioural Analysis – Questionnaire and Feature Engineering
    # -------------------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Behavioural Analysis – Questionnaire and Feature Engineering",
               "Quantifying Academic & Lifestyle Stressors via 8 Validated Dimensional Parameters", 10, "BEHAVIOURAL PIPELINE")

    # 8 Feature Definitions Grid (2 rows of 4 cards)
    features_info = [
        ("sleep_hours", "Range: 0.0 – 14.0 hrs", "Biological neural recovery. Deficits (<6.5h) heavily elevate biological stress vulnerability.", COLOR_CYAN),
        ("screen_time_hours", "Range: 0.0 – 18.0 hrs", "Digital visual exposure. Correlates with sensory fatigue and sleep cycle disruption.", COLOR_BLUE),
        ("work_study_hours", "Range: 0.0 – 16.0 hrs", "Academic & professional commitment duration; high volumes exhaust cognitive reserves.", COLOR_PURPLE),
        ("academic_work_pressure", "Likert: 1 – 5", "Subjective external urgency, exam deadlines, and performance expectations.", COLOR_ROSE),
        ("physical_activity_mins", "Range: 0 – 180 mins", "Aerobic exercise & movement. Acts as an endogenous buffer against cortisol elevation.", COLOR_EMERALD),
        ("break_frequency", "Scale: 1 – 6", "Regularity of cognitive detachment intervals during intense study or screen sessions.", COLOR_AMBER),
        ("self_reported_mood", "Scale: 1 – 5", "Subjective affective baseline from depressed/anxious (1) to highly positive (5).", COLOR_CYAN),
        ("perceived_stress_level", "Scale: 1 – 5", "Direct psychological self-assessment reflecting subjective perceived overload.", COLOR_ROSE)
    ]

    for i, (fname, frange, fdesc, fcol) in enumerate(features_info):
        row = i // 4
        col = i % 4
        left = 0.8 + col * 2.98
        top = 1.9 + row * 2.05
        add_card(slide10, left, top, 2.85, 1.95, title=fname, title_color=fcol)
        tb = slide10.shapes.add_textbox(Inches(left + 0.12), Inches(top + 0.45), Inches(2.6), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_r = tf.paragraphs[0]
        p_r.text = frange
        p_r.font.name = FONT_MAIN
        p_r.font.size = Pt(8.5)
        p_r.font.bold = True
        p_r.font.color.rgb = fcol
        p_d = tf.add_paragraph()
        p_d.text = fdesc
        p_d.font.name = FONT_MAIN
        p_d.font.size = Pt(8)
        p_d.font.color.rgb = TEXT_LIGHT

    # Bottom Pipeline Ribbon
    add_card(slide10, 0.8, 6.05, 11.733, 1.1, title="FEATURE VECTOR PREPROCESSING & INFERENCE PIPELINE", title_color=COLOR_AMBER)
    tb10_b = slide10.shapes.add_textbox(Inches(0.95), Inches(6.4), Inches(11.4), Inches(0.65))
    tf10_b = tb10_b.text_frame
    tf10_b.word_wrap = True
    p_b = tf10_b.paragraphs[0]
    p_b.text = "1. Pydantic v2 Schema Validation  ➜  2. Canonical Order Vectorization (8 Floats)  ➜  3. StandardScaler (scaler.joblib, μ=0, σ=1)  ➜  4. SupportVectorMachine Inference  ➜  5. Continuous Score: S_beh = (0.05*P_low) + (0.50*P_mod) + (0.95*P_high)"
    p_b.font.name = FONT_MAIN
    p_b.font.size = Pt(9)
    p_b.font.bold = True
    p_b.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------------------
    # SLIDE 11: Machine Learning Model Selection and Implementation
    # -------------------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Machine Learning Model Selection and Implementation",
               "Systematic Evaluation of 4 Supervised Classifiers on 3,000 Balanced Academic Lifestyle Samples", 11, "MODEL BENCHMARKING")

    # Left: Model Comparison Chart
    comp_chart_path = ASSETS_DIR / "chart_model_comparison.png"
    if comp_chart_path.exists():
        slide11.shapes.add_picture(str(comp_chart_path), Inches(0.8), Inches(1.9), Inches(7.0), Inches(5.1))

    # Right: Methodology & Results Table Card
    add_card(slide11, 8.0, 1.9, 4.533, 5.1, title="MODEL SELECTION PROTOCOL", title_color=COLOR_CYAN)
    tb11 = slide11.shapes.add_textbox(Inches(8.15), Inches(2.4), Inches(4.2), Inches(4.4))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    m_pts = [
        ("Experimental Setup", "3,000 balanced samples partitioned via 80:20 stratified split (2,400 training / 600 holdout test)."),
        ("5-Fold Cross-Validation", "5-fold StratifiedKFold executed on training data to verify generalization stability and prevent fold overfitting."),
        ("Selection Criterion: Macro F1", "Macro F1 was chosen as the primary selection metric because it penalizes models that sacrifice minority classes."),
        ("Why SVM Outperformed", "SVM with RBF kernel (C=1.5) effectively maps non-linear lifestyle interactions (e.g. sleep vs workload) in scaled hyperspace."),
        ("Actual Documented Results", "• SVM: Test Acc 83.67%, Macro F1 83.01%, ROC-AUC 95.62%\n• XGBoost: Test Acc 83.17%, Macro F1 82.42%, ROC-AUC 95.14%\n• LogReg: Test Acc 82.33%, Macro F1 81.40%, ROC-AUC 95.70%\n• Random Forest: Test Acc 80.83%, Macro F1 80.25%, ROC-AUC 94.82%")
    ]
    for i, (hd, text) in enumerate(m_pts):
        p1 = tf11.add_paragraph() if i > 0 else tf11.paragraphs[0]
        p1.text = f"▪ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_CYAN
        p2 = tf11.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(3)

    # -------------------------------------------------------------------------
    # SLIDE 12: Model Evaluation – Graphs and Performance Analysis
    # -------------------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "Model Evaluation – Graphs and Performance Analysis",
               "In-Depth Performance Verification of Selected Support Vector Machine (Holdout Test Partition: n=600)", 12, "EVALUATION METRICS")

    # Left: SVM Performance Metrics Chart
    svm_chart_path = ASSETS_DIR / "chart_svm_metrics.png"
    if svm_chart_path.exists():
        slide12.shapes.add_picture(str(svm_chart_path), Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.5))

    # Right: Confusion Matrix Heatmap
    cm_chart_path = ASSETS_DIR / "chart_svm_confusion_matrix.png"
    if cm_chart_path.exists():
        slide12.shapes.add_picture(str(cm_chart_path), Inches(6.6), Inches(1.9), Inches(5.933), Inches(4.5))

    # Bottom Clarification Callout
    callout = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.65))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_BG_LIGHT
    callout.line.color.rgb = COLOR_EMERALD
    callout.line.width = Pt(1.2)
    tf_c = callout.text_frame
    tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "CRITICAL RESULT INTERPRETATION: Zero extreme boundary errors (Low ↔ High misclassifications = 0). Errors occur strictly between adjacent Moderate classes. Note: These metrics evaluate the standalone behavioural SVM model on holdout test data, not the complete multimodal system."
    p_c1.font.name = FONT_MAIN
    p_c1.font.size = Pt(9)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_EMERALD
    p_c1.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------------------
    # SLIDE 13: Explainable AI – SHAP and Grad-CAM
    # -------------------------------------------------------------------------
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "Explainable AI – SHAP and Grad-CAM",
               "Eliminating Black-Box Opacity Across Both Behavioural Tabular Features and Visual Activations", 13, "EXPLAINABLE AI")

    # Left: SHAP Chart
    shap_chart_path = ASSETS_DIR / "chart_shap_importance.png"
    if shap_chart_path.exists():
        slide13.shapes.add_picture(str(shap_chart_path), Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.55))

    # Right: Grad-CAM Chart
    gradcam_chart_path = ASSETS_DIR / "chart_gradcam_visual.png"
    if gradcam_chart_path.exists():
        slide13.shapes.add_picture(str(gradcam_chart_path), Inches(6.7), Inches(1.85), Inches(5.833), Inches(4.55))

    # Bottom Callout Card
    xai_callout = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.65))
    xai_callout.fill.solid()
    xai_callout.fill.fore_color.rgb = CARD_BG_LIGHT
    xai_callout.line.color.rgb = COLOR_CYAN
    xai_callout.line.width = Pt(1.2)
    tf_xc = xai_callout.text_frame
    tf_xc.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_xc = tf_xc.paragraphs[0]
    p_xc.text = "WHY EXPLAINABILITY MATTERS: Healthcare and wellness AI cannot function as a black-box. SHAP provides feature-level rationale for targeted habit modification; Grad-CAM verifies facial attention focuses on muscular tension (corrugator/eyebrows) rather than extraneous background noise."
    p_xc.font.name = FONT_MAIN
    p_xc.font.size = Pt(8.5)
    p_xc.font.bold = True
    p_xc.font.color.rgb = COLOR_CYAN
    p_xc.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------------------
    # SLIDE 14: Multimodal Fusion Engine – Core Logic (CRITICAL SLIDE)
    # -------------------------------------------------------------------------
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14)
    add_header(slide14, "Multimodal Fusion Engine – Core Logic",
               "Decision-Level Soft Voting with Confidence Weighting, Dissonance Override, and Fallbacks", 14, "FUSION ENGINE")

    # Left: Fusion Flowchart
    fus_chart_path = ASSETS_DIR / "chart_fusion_flowchart.png"
    if fus_chart_path.exists():
        slide14.shapes.add_picture(str(fus_chart_path), Inches(0.8), Inches(1.9), Inches(6.8), Inches(5.1))

    # Right: Core Logic & Practical Scenarios Card
    add_card(slide14, 7.8, 1.9, 4.733, 5.1, title="FUSION MECHANISM & SCENARIOS", title_color=COLOR_EMERALD)
    tb14 = slide14.shapes.add_textbox(Inches(7.95), Inches(2.4), Inches(4.4), Inches(4.4))
    tf14 = tb14.text_frame
    tf14.word_wrap = True
    fus_pts = [
        ("1. Confidence-Weighted Soft Voting", "Modality weights are proportional to model prediction confidence:\nw_face = C_face / (C_face + C_beh), w_beh = C_beh / (C_face + C_beh).\nFinal Score: S_fused = (w_face * S_face) + (w_beh * S_beh)."),
        ("2. Dissonance Override (Masked Stress)", "Condition: S_beh > 0.70 AND S_face < 0.25.\nAction: Forces w_beh = 0.75, w_face = 0.25.\nRationale: 'Smiling Depression'—severe chronic strain (sleep < 4h, work > 12h, pressure = 5) cannot be nullified by a polite social smile."),
        ("3. Missing Modality Fallback Handler", "• Webcam Covered / No Face: Automatically shifts to behavioural_only mode (w_beh = 1.0, w_face = 0.0).\n• Survey Skipped: Automatically shifts to facial_only mode (w_face = 1.0, w_beh = 0.0). System never crashes on missing inputs."),
        ("4. Acute Stress Reaction Scenario", "High facial tension (anger/fear = 0.85, EAR < 0.20) + low lifestyle stress: Soft voting balances acute momentary anxiety with chronic baseline.")
    ]
    for i, (hd, text) in enumerate(fus_pts):
        p1 = tf14.add_paragraph() if i > 0 else tf14.paragraphs[0]
        p1.text = f"▪ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_EMERALD
        p2 = tf14.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(3)

    # -------------------------------------------------------------------------
    # SLIDE 15: Final Stress Classification and Recommendation Logic
    # -------------------------------------------------------------------------
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15)
    add_header(slide15, "Final Stress Classification and Recommendation Logic",
               "Translating Fused Stress Scores into Actionable Non-Diagnostic Wellness Recommendations", 15, "CLASSIFICATION & ACTION")

    # Left: Decision Tree Chart Image
    tree_chart_path = ASSETS_DIR / "chart_classification_decision_tree.png"
    if tree_chart_path.exists():
        slide15.shapes.add_picture(str(tree_chart_path), Inches(0.8), Inches(1.9), Inches(6.8), Inches(4.5))

    # Right: Targeted Recommender Engine Card
    add_card(slide15, 7.8, 1.9, 4.733, 4.5, title="RECOMMENDATION ENGINE RULES", title_color=COLOR_AMBER)
    tb15 = slide15.shapes.add_textbox(Inches(7.95), Inches(2.4), Inches(4.4), Inches(3.8))
    tf15 = tb15.text_frame
    tf15.word_wrap = True
    rec_rules = [
        ("Sleep Deficit (<6.5 hrs)", "Action: Power Nap Protocol & Circadian Reset.\nGuidance: 20-min midday nap; terminate screen use 45 mins prior to sleep."),
        ("Prolonged Screen Time (>8 hrs) + EAR < 0.22", "Action: 20-20-20 Ocular Decompression.\nGuidance: Every 20 mins, look at an object 20 feet away for 20 seconds."),
        ("High Pressure (4-5) + Low Mood (1-2)", "Action: 4-4-4-4 Box Breathing & Task Matrix.\nGuidance: Inhale 4s, hold 4s, exhale 4s, hold 4s; triage urgent vs important tasks."),
        ("Sedentary Study (>4 hrs) + Low Activity", "Action: Postural Micro-Breaks.\nGuidance: 5-min walk and thoracic extension stretching every 60 mins.")
    ]
    for i, (hd, text) in enumerate(rec_rules):
        p1 = tf15.add_paragraph() if i > 0 else tf15.paragraphs[0]
        p1.text = f"✔ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_AMBER
        p2 = tf15.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(2)

    # Bottom Academic Disclaimer Callout
    disc = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.65))
    disc.fill.solid()
    disc.fill.fore_color.rgb = CARD_BG_LIGHT
    disc.line.color.rgb = COLOR_ROSE
    disc.line.width = Pt(1.2)
    tf_d = disc.text_frame
    tf_d.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_d = tf_d.paragraphs[0]
    p_d.text = "ACADEMIC DISCLAIMER: The thresholds (Low < 0.38, Moderate 0.38-0.52, High > 0.52) are project-calibrated engineering benchmarks. This software is an educational prototype and wellness screening tool, not a certified clinical or psychiatric diagnostic instrument."
    p_d.font.name = FONT_MAIN
    p_d.font.size = Pt(8.5)
    p_d.font.bold = True
    p_d.font.color.rgb = COLOR_ROSE
    p_d.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------------------
    # SLIDE 16: Backend Implementation and API Integration
    # -------------------------------------------------------------------------
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16)
    add_header(slide16, "Backend Implementation and API Integration",
               "High-Throughput Asynchronous FastAPI Architecture, Pydantic v2 Validation & REST Routing", 16, "BACKEND ARCHITECTURE")

    # 4 Architecture Columns / Cards
    b_cards = [
        ("1. Application Structure", COLOR_CYAN, [
            "main.py: FastAPI entry point with CORS middleware, security headers, and router mounting.",
            "config.py: Centralized settings managing JWT secret, database paths, and model directory pointers.",
            "database.py: SQLAlchemy session factory with autocommit=False, autoflush=False engine bindings."
        ]),
        ("2. REST API Routers", COLOR_BLUE, [
            "POST /api/auth: User registration, login verification, and profile retrieval.",
            "POST /api/facial/analyze: Decodes Base64 frame, detects face ROI, evaluates EmotionCNN & Grad-CAM.",
            "POST /api/behavioural/analyze: Validates survey, applies StandardScaler, evaluates SVM & SHAP.",
            "POST /api/fusion/evaluate: Executes multimodal fusion, dissonance check, and recommendation engine.",
            "GET /api/history/trends: Returns time-series data formatted for Recharts longitudinal timeline."
        ]),
        ("3. Validation & Schemas", COLOR_PURPLE, [
            "Pydantic v2 Models: Strict input typing preventing injection or malformed data packets.",
            "Boundary Enforcement: Clamps sleep (0-14), screen (0-18), pressure (1-5), and image base64 length.",
            "Serialization: Automatic JSON serialization of complex ML outputs (SHAP dictionaries, confidence scores)."
        ]),
        ("4. Request-Response Lifecycle", COLOR_EMERALD, [
            "1. Client Axios sends Bearer JWT token in Authorization header.",
            "2. Security middleware enforces nosniff, DENY clickjack, and strict CORS whitelist.",
            "3. Route handler invokes ML engines asynchronously on worker thread pool.",
            "4. SQLAlchemy writes assessment record to SQLite; returns JSON payload (<35ms total roundtrip)."
        ])
    ]

    for i, (title, color, bullets) in enumerate(b_cards):
        left = 0.8 + i * 2.98
        add_card(slide16, left, 1.9, 2.85, 4.9, title=title, title_color=color)
        tb = slide16.shapes.add_textbox(Inches(left + 0.12), Inches(2.4), Inches(2.6), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, b in enumerate(bullets):
            p = tf.add_paragraph() if j > 0 else tf.paragraphs[0]
            p.text = f"• {b}"
            p.font.name = FONT_MAIN
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(5)

    # -------------------------------------------------------------------------
    # SLIDE 17: Database, Authentication and Security
    # -------------------------------------------------------------------------
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17)
    add_header(slide17, "Database, Authentication and Security",
               "Relational Data Persistence, BOLA Defense, Ephemeral Media Processing & OWASP Hardening", 17, "SECURITY & DATABASE")

    # 3 Large Cards
    add_card(slide17, 0.8, 1.9, 3.7, 4.9, title="1. RELATIONAL DATABASE (SQLITE)", title_color=COLOR_CYAN)
    tb17_1 = slide17.shapes.add_textbox(Inches(0.95), Inches(2.4), Inches(3.4), Inches(4.2))
    tf17_1 = tb17_1.text_frame
    tf17_1.word_wrap = True
    db_pts = [
        ("SQLAlchemy ORM", "Declarative entity definitions mapped to SQLite (stress_system.db). Enables zero-maintenance ACID compliance."),
        ("User Entity (users)", "id (PK), email (unique index), full_name, hashed_password (bcrypt), is_active, created_at, updated_at."),
        ("Assessment Entity (assessments)", "id (PK), user_id (FK to users.id), timestamp, modality_mode ('multimodal', 'facial_only', 'behavioural_only')."),
        ("Score & Metric Columns", "facial_stress_score, behavioural_stress_score, fused_stress_score, stress_category, confidence."),
        ("JSON Payloads", "Native JSON columns persist raw feature dicts, SHAP contribution arrays, and generated recommendation lists.")
    ]
    for i, (hd, text) in enumerate(db_pts):
        p1 = tf17_1.add_paragraph() if i > 0 else tf17_1.paragraphs[0]
        p1.text = f"▪ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_CYAN
        p2 = tf17_1.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(3)

    add_card(slide17, 4.8, 1.9, 3.8, 4.9, title="2. AUTHENTICATION & ACCESS CONTROL", title_color=COLOR_PURPLE)
    tb17_2 = slide17.shapes.add_textbox(Inches(4.95), Inches(2.4), Inches(3.5), Inches(4.2))
    tf17_2 = tb17_2.text_frame
    tf17_2.word_wrap = True
    auth_pts = [
        ("Stateless JWT Tokens", "Authentication issues cryptographically signed JWTs using HS256 algorithm with configured expiration window."),
        ("Bcrypt Password Hashing", "Passwords hashed with salted bcrypt rounds; plain text passwords never touch database logs."),
        ("Broken Object-Level Auth (BOLA)", "Strict tenant isolation: all /api/history queries predicate on Assessment.user_id == current_user.id. Adversaries cannot query other users' assessments (HTTP 404/403)."),
        ("Protected Route Guards", "FastAPI Depends(get_current_user) blocks unauthenticated requests with HTTP 401 Unauthorized.")
    ]
    for i, (hd, text) in enumerate(auth_pts):
        p1 = tf17_2.add_paragraph() if i > 0 else tf17_2.paragraphs[0]
        p1.text = f"▪ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PURPLE
        p2 = tf17_2.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(4)

    add_card(slide17, 8.9, 1.9, 3.6, 4.9, title="3. PRIVACY & SECURITY HARDENING", title_color=COLOR_EMERALD)
    tb17_3 = slide17.shapes.add_textbox(Inches(9.05), Inches(2.4), Inches(3.3), Inches(4.2))
    tf17_3 = tb17_3.text_frame
    tf17_3.word_wrap = True
    sec_pts = [
        ("Ephemeral Media Processing", "Webcam frames are decoded directly in RAM, processed for facial metrics, and immediately destroyed. Zero video or raw faces are stored."),
        ("Decompression Bomb Defense", "Base64 payload capped at 6MB string length and 5MB decoded bytes; image dimensions capped at 1920px with downscaling to stop DoS."),
        ("OWASP Security Headers", "Enforces X-Content-Type-Options: nosniff, X-Frame-Options: DENY, X-XSS-Protection: 1, and Permissions-Policy: camera=(self)."),
        ("CORS Sanitization", "Whitelist restricted to localhost:5555 and authorized production domains; eliminates cross-site scripting risks.")
    ]
    for i, (hd, text) in enumerate(sec_pts):
        p1 = tf17_3.add_paragraph() if i > 0 else tf17_3.paragraphs[0]
        p1.text = f"✔ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_EMERALD
        p2 = tf17_3.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 18: Testing, Validation and Practical Execution
    # -------------------------------------------------------------------------
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18)
    add_header(slide18, "Testing, Validation and Practical Execution",
               "12 Automated Test Suites, 19 Formal Verification Scenarios, and Adversarial Pen-Testing", 18, "TESTING & QA")

    # Left: Test Suite Coverage Chart
    test_chart_path = ASSETS_DIR / "chart_testing_coverage.png"
    if test_chart_path.exists():
        slide18.shapes.add_picture(str(test_chart_path), Inches(0.8), Inches(1.9), Inches(6.6), Inches(4.5))

    # Right: Testing Verification Summary Card
    add_card(slide18, 7.6, 1.9, 4.933, 4.5, title="FORMAL VERIFICATION SUITES (19/19 PASSED)", title_color=COLOR_CYAN)
    tb18 = slide18.shapes.add_textbox(Inches(7.75), Inches(2.4), Inches(4.6), Inches(3.8))
    tf18 = tb18.text_frame
    tf18.word_wrap = True
    test_suites = [
        ("Authentication & Access (TC-AUTH)", "Verifies valid JWT token issuance, 401 unauthorized rejection on bad password, and duplicate email prevention."),
        ("ML Inference & XAI (TC-BEH, TC-FACE)", "Tests 8-feature SVM scoring, SHAP TreeExplainer attribution calculation, Haar face detection, and Grad-CAM generation."),
        ("Multimodal Fusion & Fallback (TC-FUS)", "Evaluates dual-stream fusion, covered-camera 1x1 blank pixel fallback, and survey omission handling."),
        ("Database Persistence (TC-HIST)", "Validates assessment history retrieval, user isolation, and Recharts trend aggregation."),
        ("Adversarial Security (Shannon Audit)", "Validates BOLA cross-tenant isolation (User B accessing User A gets 404), 7MB DoS decompression bomb defense, and security headers."),
        ("Environmental Robustness (ENV)", "Verified under dim lighting (<80 lux), overexposure (>800 lux), head yaw (±20°), and eyeglass occlusion.")
    ]
    for i, (hd, text) in enumerate(test_suites):
        p1 = tf18.add_paragraph() if i > 0 else tf18.paragraphs[0]
        p1.text = f"✔ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_CYAN
        p2 = tf18.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(2)

    # Bottom Stat Bar
    s_bar = slide18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.65))
    s_bar.fill.solid()
    s_bar.fill.fore_color.rgb = CARD_BG_LIGHT
    s_bar.line.color.rgb = COLOR_EMERALD
    s_bar.line.width = Pt(1.2)
    tf_sb = s_bar.text_frame
    tf_sb.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_sb = tf_sb.paragraphs[0]
    p_sb.text = "AUTOMATED TEST EXECUTION SUMMARY: 12 Test Suites | 19 Test Cases Executed | 19 Passed (100%) | 0 Failed | Total Suite Runtime: 8.62s | Zero Deprecation Warnings"
    p_sb.font.name = FONT_MAIN
    p_sb.font.size = Pt(9)
    p_sb.font.bold = True
    p_sb.font.color.rgb = COLOR_EMERALD
    p_sb.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------------------
    # SLIDE 19: Limitations, Challenges and Future Enhancements
    # -------------------------------------------------------------------------
    slide19 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide19)
    add_header(slide19, "Limitations, Challenges and Future Enhancements",
               "Candid Appraisal of Current Engineering Constraints and Strategic Research Roadmap", 19, "LIMITATIONS & ROADMAP")

    # Left: Current Limitations Card
    add_card(slide19, 0.8, 1.9, 5.75, 5.1, title="CURRENT PROJECT LIMITATIONS", title_color=COLOR_ROSE)
    tb19_l = slide19.shapes.add_textbox(Inches(0.95), Inches(2.4), Inches(5.45), Inches(4.4))
    tf19_l = tb19_l.text_frame
    tf19_l.word_wrap = True
    limits = [
        ("Webcam Quality & Illumination Sensitivity", "Commodity laptop webcams suffer from sensor noise, motion blur, and poor dynamic range under dim (<80 lux) or backlit (>800 lux) conditions."),
        ("Non-Verbal Emotional Ambiguity", "Facial expressions alone do not monotonically map to stress. Social smiling, cultural display rules, and emotional masking introduce ambiguity."),
        ("Self-Reporting Subjectivity", "Lifestyle questionnaire inputs rely on user recollection, which is subject to estimation inaccuracies, social desirability bias, and cognitive delay."),
        ("Absence of Clinical Ground Truth", "Models are trained on synthesized and academic benchmark distributions; the system is not yet paired with physiological gold standards (cortisol, EEG, HRV)."),
        ("Heuristic Boundary Calibration", "The classification thresholds (0.38, 0.52) are project-calibrated engineering boundaries rather than clinically standardized diagnostic thresholds.")
    ]
    for i, (hd, text) in enumerate(limits):
        p1 = tf19_l.add_paragraph() if i > 0 else tf19_l.paragraphs[0]
        p1.text = f"⚠ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_ROSE
        p2 = tf19_l.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(3)

    # Right: Future Enhancements Roadmap Card
    add_card(slide19, 6.8, 1.9, 5.733, 5.1, title="STRATEGIC FUTURE ROADMAP", title_color=COLOR_EMERALD)
    tb19_r = slide19.shapes.add_textbox(Inches(6.95), Inches(2.4), Inches(5.4), Inches(4.4))
    tf19_r = tb19_r.text_frame
    tf19_r.word_wrap = True
    future = [
        ("Clinical Gold-Standard Validation", "Partner with academic medical centers to evaluate multimodal predictions against salivary cortisol markers and continuous EEG recordings."),
        ("Non-Invasive Wearable Integration", "Incorporate optional consumer smartwatch data (Photoplethysmography / PPG) for continuous Heart Rate Variability (HRV) and skin temperature."),
        ("Temporal Sequence Modeling", "Transition from single-frame snapshots to continuous temporal video analysis using 3D-CNNs or Video Vision Transformers with LSTM sequence tracking."),
        ("Demographic Fairness & Calibration", "Expand training datasets across diverse age groups, skin tones, and cultures with rigorous adversarial fairness auditing to prevent demographic bias."),
        ("Edge WebAssembly Deployment", "Compile EmotionCNN to ONNX Web / WebAssembly for 100% client-side offline execution, achieving true zero-transmission privacy.")
    ]
    for i, (hd, text) in enumerate(future):
        p1 = tf19_r.add_paragraph() if i > 0 else tf19_r.paragraphs[0]
        p1.text = f"✔ {hd}:"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_EMERALD
        p2 = tf19_r.add_paragraph()
        p2.text = text
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_after = Pt(3)

    # -------------------------------------------------------------------------
    # SLIDE 20: Conclusion and Live Demonstration Workflow
    # -------------------------------------------------------------------------
    slide20 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide20)
    add_header(slide20, "Conclusion and Live Demonstration Workflow",
               "Summary of Project Accomplishments and End-to-End Practical Execution Protocol", 20, "CONCLUSION & DEMO")

    # Top: 10-Step Live Demonstration Walkthrough Card
    add_card(slide20, 0.8, 1.9, 11.733, 2.5, title="LIVE DEMONSTRATION WORKFLOW (EXACT PRACTICAL SEQUENCE)", title_color=COLOR_CYAN)
    demo_steps = [
        ("Step 1", "User Login (Auto-Fill demo@stressguard.edu)"),
        ("Step 2", "Open Dashboard & review 14-day trends"),
        ("Step 3", "Click 'New Assessment' (Launch Wizard)"),
        ("Step 4", "Enable webcam & verify lighting quality"),
        ("Step 5", "Capture frame & calculate live EAR"),
        ("Step 6", "Complete 8-factor lifestyle survey"),
        ("Step 7", "FastAPI executes dual ML inference"),
        ("Step 8", "Fusion engine evaluates dissonance"),
        ("Step 9", "Results display gauge, SHAP & Grad-CAM"),
        ("Step 10", "Review recommendations & export report")
    ]
    for i, (st, desc) in enumerate(demo_steps):
        row = i // 5
        col = i % 5
        x = 0.95 + col * 2.3
        y = 2.4 + row * 0.95
        box = slide20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(2.2), Inches(0.85))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG_LIGHT
        box.line.color.rgb = COLOR_CYAN if row == 0 else COLOR_EMERALD
        box.line.width = Pt(1)
        tf_b = box.text_frame
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = tf_b.paragraphs[0]
        p1.text = st
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_CYAN if row == 0 else COLOR_EMERALD
        p2 = tf_b.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = TEXT_WHITE

    # Bottom Left: Project Achievements
    add_card(slide20, 0.8, 4.6, 5.75, 2.4, title="KEY SYSTEM ACHIEVEMENTS", title_color=COLOR_PURPLE)
    tb20_ach = slide20.shapes.add_textbox(Inches(0.95), Inches(5.05), Inches(5.45), Inches(1.85))
    tf20_ach = tb20_ach.text_frame
    tf20_ach.word_wrap = True
    achs = [
        "Multimodal Synergy: Resolved unimodal blindspots via confidence-weighted fusion & dissonance override.",
        "High Performance: Sub-30ms CPU inference with zero invasive wearable hardware requirements.",
        "Explainability Built-in: Transparent SHAP attribution and Grad-CAM visual heatmaps.",
        "Production-Grade Engineering: Complete full-stack integration (FastAPI, React 19, SQLite, Recharts)."
    ]
    for i, a in enumerate(achs):
        p = tf20_ach.add_paragraph() if i > 0 else tf20_ach.paragraphs[0]
        p.text = f"✔ {a}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(2)

    # Bottom Right: Final Viva / Team Sign-off
    add_card(slide20, 6.8, 4.6, 5.733, 2.4, title="THANK YOU — QUESTIONS & DISCUSSION", title_color=COLOR_AMBER)
    tb20_so = slide20.shapes.add_textbox(Inches(6.95), Inches(5.05), Inches(5.4), Inches(1.85))
    tf20_so = tb20_so.text_frame
    tf20_so.word_wrap = True
    p_so1 = tf20_so.paragraphs[0]
    p_so1.text = "Major Project Viva Presentation Completed"
    p_so1.font.name = FONT_HEADING
    p_so1.font.size = Pt(11)
    p_so1.font.bold = True
    p_so1.font.color.rgb = COLOR_AMBER

    p_so2 = tf20_so.add_paragraph()
    p_so2.text = "Team Members:"
    p_so2.font.name = FONT_MAIN
    p_so2.font.size = Pt(9)
    p_so2.font.bold = True
    p_so2.font.color.rgb = TEXT_WHITE
    p_so2.space_before = Pt(3)

    p_so3 = tf20_so.add_paragraph()
    p_so3.text = "• Tarandeep Kaur (23052441)   • Sakshi Agarwal (23051776)\n• Shatakshi Dasgupta (23052425) • Swasti Suman (23051552)\n• Swastika Chatterjee (23053315)"
    p_so3.font.name = FONT_MAIN
    p_so3.font.size = Pt(8.5)
    p_so3.font.color.rgb = TEXT_LIGHT

    p_so4 = tf20_so.add_paragraph()
    p_so4.text = "Department of Computer Science & Engineering | 2026"
    p_so4.font.name = FONT_MAIN
    p_so4.font.size = Pt(8.5)
    p_so4.font.italic = True
    p_so4.font.color.rgb = COLOR_CYAN
    p_so4.space_before = Pt(3)

    # Save presentation
    output_path = Path("Real_Time_Multimodal_Stress_Detection_and_Analysis_System_Presentation.pptx")
    prs.save(str(output_path))
    print(f"Presentation saved successfully to: {output_path.resolve()}")
    print(f"Total slides generated: {len(prs.slides)}")

if __name__ == "__main__":
    create_deck()
