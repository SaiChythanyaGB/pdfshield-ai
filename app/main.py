
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.pdf_features import extract_features
from ml.adversarial_lab import adversarial_sweep
from app.ui.styles import inject_styles
from app.ui.components import (
    hero, section_heading, glass_card, metric_card, pipeline, verdict_card
)

MODEL_PATH = ROOT / "models" / "pdf_malware_rf.joblib"

st.set_page_config(
    page_title="PDFShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">PDFShield AI</div>
            <div class="brand-sub">Defensive PDF Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Dashboard", "PDF Scanner", "Adversarial Lab", "Model Information", "About"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("SYSTEM")
    if model is not None:
        st.success("Model loaded")
    else:
        st.warning("Model not loaded")

    st.caption("Static analysis only • No document execution")

if page == "Dashboard":
    hero()

    st.write("")
    section_heading(
        "SYSTEM OVERVIEW",
        "Security intelligence at a glance",
        "A research-focused pipeline for static PDF malware analysis.",
    )

    cols = st.columns(4)
    metrics = [
        ("Dataset", "10,023 PDFs"),
        ("Accuracy", "98.85%"),
        ("F1 Score", "98.97%"),
        ("ROC-AUC", "0.9991"),
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            metric_card(label, value)

    st.write("")
    section_heading("DETECTION PIPELINE", "From document to security verdict")
    pipeline()

    st.write("")
    section_heading("CORE CAPABILITIES", "Four layers of defensive analysis")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        glass_card("🔎", "Static PDF Analysis",
                   "Extract structural, metadata, content and security-relevant features without executing the uploaded document.")
    with c2:
        glass_card("🤖", "ML Detection",
                   "A Random Forest classifier evaluates the extracted 31-feature representation for benign or malicious classification.")
    with c3:
        glass_card("🧪", "Adversarial Lab",
                   "Controlled feature-space perturbations study how the model responds to simulated input variation.")
    with c4:
        glass_card("📈", "Model Evaluation",
                   "Accuracy, precision, recall, F1, ROC-AUC and confusion-matrix analysis provide measurable evaluation.")

    st.write("")
    section_heading("DATASET", "PDFMalware2022 project dataset")

    d1, d2, d3 = st.columns(3)
    with d1:
        metric_card("Total samples", "10,023")
    with d2:
        metric_card("Malicious", "5,555")
    with d3:
        metric_card("Benign", "4,468")

    st.write("")
    section_heading("DEFENSIVE DESIGN", "Safety-first analysis")

    s1, s2, s3 = st.columns(3)
    with s1:
        glass_card("🛡️", "No execution", "PDFs are treated as data. JavaScript, embedded files and commands are not executed.")
    with s2:
        glass_card("🧬", "Feature-space research", "The adversarial experiment perturbs model features rather than creating or modifying malicious files.")
    with s3:
        glass_card("⚠️", "Academic scope", "Model probabilities are estimates and should not be treated as definitive malware verdicts.")

    st.markdown('<div class="footer-note">PDFShield AI • Data Science for Security • Defensive academic research project</div>',
                unsafe_allow_html=True)

elif page == "PDF Scanner":
    section_heading(
        "STATIC ANALYSIS",
        "PDF Security Scanner",
        "Upload a PDF for non-executing structural analysis.",
    )

    st.markdown("""
    <div class="scanner-drop">
        <div class="scanner-icon">📄</div>
        <div class="scanner-title">Drop a PDF into the scanner</div>
        <div class="scanner-sub">Maximum 20 MB • Static analysis • No JavaScript or embedded-file execution</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Choose PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded:
        if uploaded.size > 20 * 1024 * 1024:
            st.error("File is larger than the 20 MB demo limit.")
            st.stop()

        temp_dir = ROOT / "data" / "runtime"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp = temp_dir / "uploaded.pdf"
        temp.write_bytes(uploaded.getvalue())

        with st.spinner("Analyzing PDF structure safely..."):
            try:
                features = extract_features(temp)
            except Exception as exc:
                st.error(f"Could not analyze this PDF safely: {exc}")
                st.stop()

        st.session_state["pdf_features"] = features
        st.session_state["pdf_name"] = uploaded.name

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.markdown(f"**📄 {uploaded.name}**")
            st.caption(f"{uploaded.size / 1024:.1f} KB • {len(features)} static features extracted")
        with c2:
            st.metric("Features", len(features))
        with c3:
            st.metric("File size", f"{uploaded.size / 1024:.1f} KB")

        if model is None:
            st.warning("Trained model not found. Run `python ml/train.py` first.")
        else:
            X = pd.DataFrame([features])
            prediction = int(model.predict(X)[0])
            probability = float(model.predict_proba(X)[0, 1])
            benign_probability = 1.0 - probability

            verdict_card(prediction, probability)

            c1, c2 = st.columns(2)
            with c1:
                metric_card("Malicious probability", f"{probability * 100:.2f}%")
            with c2:
                metric_card("Benign probability", f"{benign_probability * 100:.2f}%")

            st.write("")
            section_heading("RISK ANALYSIS", "Model-estimated risk")

            if probability >= 0.80:
                st.error("High model-estimated malicious risk")
            elif probability >= 0.50:
                st.warning("Elevated model-estimated malicious risk")
            else:
                st.success("Low model-estimated malicious risk")

            st.caption(
                "The probability is a model estimate from the Random Forest classifier; "
                "it is not a calibrated confidence score or a definitive malware verdict."
            )

            st.write("")
            section_heading("SECURITY INDICATORS", "Potentially relevant PDF structures")

            indicators = {
                "JavaScript": features.get("Javascript", "0"),
                "JS": features.get("JS", "0"),
                "OpenAction": features.get("OpenAction", "0"),
                "AA": features.get("AA", "0"),
                "Launch": features.get("Launch", "0"),
                "EmbeddedFile": features.get("EmbeddedFile", "0"),
                "XFA": features.get("XFA", "0"),
                "JBIG2Decode": features.get("JBIG2Decode", "0"),
                "RichMedia": features.get("RichMedia", "0"),
                "Acroform": features.get("Acroform", "0"),
            }

            def as_flag(value):
                text = str(value).strip().lower()
                return text in {"yes", "true", "1"}

            left, right = st.columns(2)
            items = list(indicators.items())
            midpoint = (len(items) + 1) // 2

            for container, subset in [(left, items[:midpoint]), (right, items[midpoint:])]:
                with container:
                    for name, value in subset:
                        active = as_flag(value)
                        state = "DETECTED" if active else "NOT DETECTED"
                        css = "state-on" if active else "state-off"
                        icon = "●" if active else "○"
                        st.markdown(
                            f"""
                            <div class="indicator">
                                <span class="indicator-name">{name}</span>
                                <span class="indicator-state {css}">{icon} {state}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            chart_df = pd.DataFrame({
                "Indicator": list(indicators.keys()),
                "Detected": [1 if as_flag(v) else 0 for v in indicators.values()],
            })

            fig = px.bar(
                chart_df,
                x="Indicator",
                y="Detected",
                title="Security-relevant feature presence",
                range_y=[0, 1.15],
            )
            fig.update_layout(
                height=360,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=55, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.write("")
            with st.expander("🧬 Explore all 31 extracted features"):
                feature_table = pd.DataFrame([features]).T.rename(columns={0: "Value"})
                st.dataframe(feature_table, use_container_width=True)

elif page == "Adversarial Lab":
    section_heading(
        "ROBUSTNESS RESEARCH",
        "Adversarial Robustness Lab",
        "Study controlled feature-space perturbations without creating or modifying malicious PDFs.",
    )

    st.markdown("""
    <div class="lab-banner">
        🧪 <b>Safe research mode:</b> this experiment operates on extracted feature values
        and does not generate, execute, or modify malicious PDF files.
    </div>
    """, unsafe_allow_html=True)

    if "pdf_features" not in st.session_state:
        st.info("📄 Analyze a PDF in the PDF Scanner first. The lab will automatically reuse it.")
    elif model is None:
        st.error("Trained model not found. Run `python ml/train.py` first.")
    else:
        features = st.session_state["pdf_features"]
        pdf_name = st.session_state.get("pdf_name", "Previously scanned PDF")
        X = pd.DataFrame([features])

        base_prob = float(model.predict_proba(X)[0, 1])
        base_prediction = int(model.predict(X)[0])

        st.success(f"📄 Experiment target: {pdf_name}")

        c1, c2 = st.columns(2)
        with c1:
            metric_card("Baseline malicious probability", f"{base_prob * 100:.2f}%")
        with c2:
            metric_card("Baseline decision", "MALICIOUS" if base_prediction else "BENIGN")

        st.write("")
        strength = st.slider(
            "Feature-space perturbation strength",
            0.0, 0.50, 0.20, 0.01,
            help="Controls the magnitude of the simulated feature-space perturbation."
        )

        if st.button("🧪 Run robustness sweep", use_container_width=True):
            results = adversarial_sweep(
                model,
                X,
                y_true=base_prediction,
                strength=strength,
            )

            section_heading("EXPERIMENT OUTPUT", "Model response to controlled perturbation")

            fig = px.line(
                results,
                x="perturbation",
                y="malicious_probability",
                markers=True,
                title="Malicious probability across perturbation strength",
            )
            fig.add_hline(
                y=0.5,
                line_dash="dash",
                annotation_text="Decision threshold",
            )
            fig.update_layout(
                height=440,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

            changed = (results["prediction"] != results.iloc[0]["prediction"]).any()
            if changed:
                st.warning("⚠️ The model changed its classification during this simulated feature-space sweep.")
            else:
                st.success("✅ The model kept the same classification across this simulated sweep.")

            st.dataframe(results, use_container_width=True)

        st.caption(
            "Interpretation: this is a controlled academic robustness experiment. "
            "It does not demonstrate that a real-world PDF can be modified to evade the detector."
        )

        if st.button("Clear scanned PDF"):
            st.session_state.pop("pdf_features", None)
            st.session_state.pop("pdf_name", None)
            st.rerun()

elif page == "Model Information":
    section_heading(
        "MODEL INTELLIGENCE",
        "Random Forest Detection Model",
        "Training configuration and held-out evaluation results.",
    )

    if not MODEL_PATH.exists():
        st.warning("Trained model not found. Run `python ml/train.py` before using the model.")
    else:
        st.success("✅ Trained model loaded successfully")

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Algorithm", "Random Forest")
        with c2:
            metric_card("Trees", "350")
        with c3:
            metric_card("Task", "Benign vs Malicious")

        st.write("")
        section_heading("DATASET", "Training and evaluation configuration")

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Total PDFs", "10,023")
        with c2:
            metric_card("Malicious", "5,555")
        with c3:
            metric_card("Benign", "4,468")

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Training samples", "8,018")
        with c2:
            metric_card("Test samples", "2,005")
        with c3:
            metric_card("Split", "80 / 20")

        st.write("")
        section_heading("PERFORMANCE", "Held-out test-set metrics")

        cols = st.columns(5)
        for col, (label, value) in zip(cols, [
            ("Accuracy", "98.85%"),
            ("Precision", "98.57%"),
            ("Recall", "99.37%"),
            ("F1 Score", "98.97%"),
            ("ROC-AUC", "0.9991"),
        ]):
            with col:
                metric_card(label, value)

        st.caption("Metrics are calculated on the held-out test split.")

        st.write("")
        section_heading("CONFUSION MATRIX", "Classification outcomes")

        cm = [[878, 16], [7, 1104]]
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=["Predicted Benign", "Predicted Malicious"],
            y=["Actual Benign", "Actual Malicious"],
            text=cm,
            texttemplate="%{text}",
            hovertemplate="%{y}<br>%{x}<br>Count: %{z}<extra></extra>",
        ))
        fig.update_layout(
            height=390,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("")
        section_heading("FEATURE ENGINEERING", "31 static PDF features")

        feature_groups = {
            "File / document properties": [
                "PdfSize", "MetadataSize", "Pages", "XrefLength",
                "TitleCharacters", "isEncrypted", "PageNo"
            ],
            "PDF structural features": [
                "Header", "Obj", "Endobj", "Stream", "Endstream",
                "Xref", "Trailer", "StartXref", "Encrypt", "ObjStm"
            ],
            "Security-relevant features": [
                "JS", "Javascript", "AA", "OpenAction", "Acroform",
                "JBIG2Decode", "RichMedia", "Launch", "EmbeddedFile", "XFA"
            ],
            "Content features": [
                "EmbeddedFiles", "Images", "Text", "Colors"
            ],
        }

        for title, features in feature_groups.items():
            with st.expander(title):
                st.write(", ".join(features))

        st.info(
            "This is an academic research classifier for defensive PDF malware analysis. "
            "Static analysis can produce false positives and false negatives, and the "
            "reported probabilities are model estimates rather than definitive malware verdicts."
        )

elif page == "About":
    hero()
    st.write("")
    section_heading("ABOUT THE PROJECT", "Built for Data Science for Security")

    c1, c2 = st.columns(2)
    with c1:
        glass_card(
            "🎯", "Problem",
            "PDF documents can contain structural and active-content characteristics "
            "associated with malicious behavior. PDFShield AI studies whether static "
            "features can support automated classification."
        )
    with c2:
        glass_card(
            "🧠", "Approach",
            "A supervised Random Forest classifier is trained on static PDF features, "
            "followed by controlled feature-space robustness experiments."
        )

    st.write("")
    section_heading("TECHNOLOGY", "Project stack")

    tech = st.columns(5)
    for col, item in zip(tech, [
        ("🐍", "Python"),
        ("🎈", "Streamlit"),
        ("🌲", "Scikit-learn"),
        ("📄", "pypdf"),
        ("📊", "Plotly"),
    ]):
        with col:
            glass_card(item[0], item[1], "Core project technology")

    st.write("")
    section_heading("DEFENSIVE PRINCIPLES", "Designed for safe academic experimentation")

    st.info(
        "Uploaded PDFs are analyzed as data. The application does not execute PDF JavaScript, "
        "embedded programs, macros or extracted files. The adversarial component works in "
        "feature space rather than generating or modifying malicious documents."
    )

    st.markdown(
        '<div class="footer-note">PDFShield AI • AI-Powered PDF Malware Detection & Adversarial Robustness Analysis</div>',
        unsafe_allow_html=True,
    )
