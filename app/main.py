from __future__ import annotations

import io
import sys
from pathlib import Path

# Add the project root to Python's import path
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from app.pdf_features import extract_features
from ml.adversarial_lab import adversarial_sweep

MODEL_PATH = ROOT / "models" / "pdf_malware_rf.joblib"

st.set_page_config(page_title="PDFShield AI", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 2rem;}
.metric-card {padding: 1rem; border: 1px solid rgba(128,128,128,.25); border-radius: 14px;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

st.title("🛡️ PDFShield AI")
st.caption("Defensive static PDF malware detection + feature-space adversarial robustness lab")

if model is None:
    st.warning("Model not found. Train it first using the command in README.md. The interface can still be explored, but predictions require a trained model.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
    "Navigation",
    [
        "Dashboard",
        "PDF Scanner",
        "Adversarial Lab",
        "Model Information",
        "About"
    ],
    label_visibility="collapsed",
)

if page == "Dashboard":

    # ==================================================
    # HERO SECTION
    # ==================================================

    st.markdown(
    """
<div style="padding:2rem;border-radius:20px;border:1px solid rgba(255,255,255,0.12);background:linear-gradient(135deg,rgba(80,80,120,0.20),rgba(20,20,30,0.45));margin-bottom:1.5rem;">
<h1 style="margin:0 0 0.5rem 0;">🛡️ PDFShield AI</h1>
<div style="font-size:1.15rem;opacity:0.8;">
AI-Powered PDF Malware Detection &amp; Adversarial Robustness Analysis
</div>
</div>
""",
    unsafe_allow_html=True
)

    st.markdown(
        """
        **PDFShield AI** is a defensive cybersecurity system that
        analyzes PDF files using static features and machine learning
        without executing the uploaded document.
        """
    )

    st.divider()

    # ==================================================
    # KEY PERFORMANCE METRICS
    # ==================================================

    st.subheader("📊 System Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Dataset",
        "10,023 PDFs"
    )

    col2.metric(
        "Accuracy",
        "98.85%"
    )

    col3.metric(
        "F1 Score",
        "98.97%"
    )

    col4.metric(
        "ROC-AUC",
        "0.9991"
    )

    st.divider()

    # ==================================================
    # SYSTEM WORKFLOW
    # ==================================================

    st.subheader("⚙️ Detection Workflow")

    st.code(
        """
PDF Upload
     ↓
Safe Static Analysis
     ↓
31 PDF Feature Extraction
     ↓
Preprocessing
     ↓
Random Forest Classifier
     ↓
Benign / Malicious Classification
     ↓
Risk Estimation
     ↓
Adversarial Robustness Analysis
        """,
        language="text"
    )

    st.divider()

    # ==================================================
    # PROJECT COMPONENTS
    # ==================================================

    st.subheader("🔐 Security Analysis Components")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🔎 Static PDF Analysis")

        st.write(
            "Extracts structural, metadata, content and "
            "security-relevant PDF features without executing "
            "JavaScript or embedded files."
        )

        st.markdown("### 🤖 Machine Learning Detection")

        st.write(
            "A Random Forest classifier analyzes the extracted "
            "feature vector to classify PDFs as benign or malicious."
        )

    with col2:

        st.markdown("### 🧪 Adversarial Robustness")

        st.write(
            "Controlled feature-space perturbations are used to "
            "study how the model's estimated malicious probability "
            "changes under simulated input variations."
        )

        st.markdown("### 📈 Model Evaluation")

        st.write(
            "Performance is evaluated using accuracy, precision, "
            "recall, F1-score, ROC-AUC and a confusion matrix."
        )

    st.divider()

    # ==================================================
    # DATASET SUMMARY
    # ==================================================

    st.subheader("📚 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Samples",
        "10,023"
    )

    col2.metric(
        "Malicious",
        "5,555"
    )

    col3.metric(
        "Benign",
        "4,468"
    )

    st.caption(
        "PDFMalware2022 feature dataset used for training and evaluation."
    )

    st.divider()

    # ==================================================
    # SAFETY DESIGN
    # ==================================================

    st.subheader("🛡️ Defensive Security Design")

    st.success(
        "✓ PDFs are analyzed as data and are never executed."
    )

    st.info(
        "✓ Embedded JavaScript, macros, commands and extracted "
        "files are not executed by the application."
    )

    st.info(
        "✓ Adversarial experiments operate in feature space "
        "rather than creating or modifying malicious PDFs."
    )

    st.warning(
        "⚠️ This is an academic research classifier. Model "
        "probabilities are estimates and should not be treated "
        "as definitive malware verdicts."
    )
elif page == "PDF Scanner":
    st.subheader("🔎 Static PDF Scanner")

    st.info(
        "Upload a PDF for non-executing static analysis. "
        "PDF JavaScript and embedded files are never executed."
    )

    uploaded = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
    )

    if uploaded:

        if uploaded.size > 20 * 1024 * 1024:
            st.error("File is larger than the 20 MB demo limit.")
            st.stop()

        temp_dir = ROOT / "data" / "runtime"
        temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        temp = temp_dir / "uploaded.pdf"
        temp.write_bytes(uploaded.getvalue())

        try:

            # ==================================================
            # FEATURE EXTRACTION
            # ==================================================

            with st.spinner("Performing safe static analysis..."):

                features = extract_features(temp)

            st.success(
                f"Successfully extracted {len(features)} static features."
            )
            st.session_state["pdf_features"] = features
            st.session_state["pdf_name"] = uploaded.name

            # ==================================================
            # MODEL PREDICTION
            # ==================================================

            if model is None:

                st.warning(
                    "Trained model not found. "
                    "Run `python ml/train.py` first."
                )

            else:

                X = pd.DataFrame([features])

                prediction = int(
                    model.predict(X)[0]
                )

                probability = float(
                    model.predict_proba(X)[0, 1]
                )

                benign_probability = 1.0 - probability

                st.divider()

                # ==================================================
                # RESULT
                # ==================================================

                if prediction == 1:

                    st.error(
                        "🚨 MALICIOUS PDF DETECTED"
                    )

                else:

                    st.success(
                        "✅ PDF CLASSIFIED AS BENIGN"
                    )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Classification",
                    "MALICIOUS"
                    if prediction == 1
                    else "BENIGN",
                )

                col2.metric(
                    "Malicious probability",
                    f"{probability * 100:.2f}%",
                )

                col3.metric(
                    "Benign probability",
                    f"{benign_probability * 100:.2f}%",
                )

                # ==================================================
                # RISK INTERPRETATION
                # ==================================================

                st.subheader("Risk interpretation")

                if probability >= 0.80:

                    st.error(
                        "High model-estimated malicious risk"
                    )

                elif probability >= 0.50:

                    st.warning(
                        "Elevated model-estimated malicious risk"
                    )

                else:

                    st.success(
                        "Low model-estimated malicious risk"
                    )

                st.caption(
                    "Risk is based on the Random Forest model's "
                    "estimated probability and should not be treated "
                    "as a definitive malware verdict."
                )

                # ==================================================
                # SECURITY INDICATORS
                # ==================================================

                st.divider()

                st.subheader(
                    "🔐 Security-relevant indicators"
                )

                indicators = {

                    "JavaScript": features.get(
                        "Javascript",
                        "0",
                    ),

                    "JS": features.get(
                        "JS",
                        "0",
                    ),

                    "OpenAction": features.get(
                        "OpenAction",
                        "0",
                    ),

                    "AA": features.get(
                        "AA",
                        "0",
                    ),

                    "Launch": features.get(
                        "Launch",
                        "0",
                    ),

                    "EmbeddedFile": features.get(
                        "EmbeddedFile",
                        "0",
                    ),

                    "XFA": features.get(
                        "XFA",
                        "0",
                    ),

                    "JBIG2Decode": features.get(
                        "JBIG2Decode",
                        "0",
                    ),

                    "RichMedia": features.get(
                        "RichMedia",
                        "0",
                    ),

                    "Acroform": features.get(
                        "Acroform",
                        "0",
                    ),

                }

                indicator_values = []

                for name, value in indicators.items():

                    if isinstance(value, str):
                        value_clean = value.strip().lower()

                        if value_clean in ["yes", "true", "1"]:
                            numeric_value = 1
                        elif value_clean in ["no", "false", "0"]:
                            numeric_value = 0
                        else:
                            try:
                                numeric_value = float(value)
                            except (ValueError, TypeError):
                                numeric_value = 0

                    else:
                        try:
                            numeric_value = float(value)
                        except (ValueError, TypeError):
                            numeric_value = 0

                    indicator_values.append(numeric_value)

                chart_df = pd.DataFrame(
                    {
                        "Indicator": list(
                            indicators.keys()
                        ),
                        "Count": indicator_values,
                    }
                )

                fig = px.bar(
                    chart_df,
                    x="Indicator",
                    y="Count",
                    title="PDF security-relevant indicators",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                # ==================================================
                # ALL FEATURES
                # ==================================================

                with st.expander(
                    "View all 31 extracted features"
                ):

                    feature_table = (
                        pd.DataFrame(
                            [features]
                        )
                        .T
                        .rename(
                            columns={
                                0: "Value"
                            }
                        )
                    )

                    st.dataframe(
                        feature_table,
                        use_container_width=True,
                    )

        except Exception as exc:

            st.error(
                f"Could not analyze this PDF safely: {exc}"
            )

elif page == "Adversarial Lab":

    st.subheader("🧪 Adversarial Robustness Lab")

    st.warning(
        "This lab operates in feature space for safe experimentation. "
        "It does not create or modify malicious files."
    )

    st.write(
        "The lab reuses the PDF analyzed in the PDF Scanner. "
        "No second upload is required."
    )

    if "pdf_features" not in st.session_state:

        st.info(
            "📄 No PDF has been analyzed yet. "
            "Go to PDF Scanner and upload a PDF first."
        )

    else:

        features = st.session_state["pdf_features"]

        pdf_name = st.session_state.get(
            "pdf_name",
            "Previously scanned PDF"
        )

        st.success(
            f"📄 Using scanned PDF: {pdf_name}"
        )

        X = pd.DataFrame([features])

        if model is None:

            st.error(
                "Trained model not found. "
                "Run `python ml/train.py` first."
            )

        else:

            base_prob = float(
                model.predict_proba(X)[0, 1]
            )

            base_prediction = int(
                model.predict(X)[0]
            )

            st.metric(
                "Baseline malicious probability",
                f"{base_prob * 100:.2f}%"
            )

            st.caption(
                "Baseline classification: "
                + (
                    "MALICIOUS"
                    if base_prediction == 1
                    else "BENIGN"
                )
            )

            st.divider()

            strength = st.slider(
                "Feature-space perturbation strength",
                0.0,
                0.50,
                0.20,
                0.01
            )

            if st.button("Run robustness sweep"):

                results = adversarial_sweep(
                    model,
                    X,
                    y_true=base_prediction,
                    strength=strength
                )

                st.subheader(
                    "📊 Robustness Experiment Results"
                )

                st.dataframe(
                    results,
                    use_container_width=True
                )

                fig = px.line(
                    results,
                    x="perturbation",
                    y="malicious_probability",
                    markers=True,
                    title="Model response to controlled perturbation"
                )

                fig.add_hline(
                    y=0.5,
                    line_dash="dash",
                    annotation_text="Decision threshold"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                if (
                    results["prediction"]
                    != results.iloc[0]["prediction"]
                ).any():

                    st.warning(
                        "⚠️ The model changed its decision "
                        "during the simulated feature-space "
                        "perturbation."
                    )

                else:

                    st.success(
                        "✅ The model kept the same decision "
                        "across this simulated sweep."
                    )

            st.divider()

            if st.button("Clear scanned PDF"):

                st.session_state.pop(
                    "pdf_features",
                    None
                )

                st.session_state.pop(
                    "pdf_name",
                    None
                )

                st.rerun()

elif page == "Model Information":

    st.subheader("📊 Model Information")

    if MODEL_PATH.exists():

        # ==================================================
        # MODEL DETAILS
        # ==================================================

        st.success("✅ Trained model loaded successfully")

        st.markdown("### 🤖 Model Configuration")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Algorithm",
            "Random Forest"
        )

        col2.metric(
            "Number of Trees",
            "350"
        )

        col3.metric(
            "Task",
            "Benign vs Malicious"
        )

        st.divider()

        # ==================================================
        # DATASET INFORMATION
        # ==================================================

        st.markdown("### 📚 Dataset Information")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total PDFs",
            "10,023"
        )

        col2.metric(
            "Malicious PDFs",
            "5,555"
        )

        col3.metric(
            "Benign PDFs",
            "4,468"
        )

        st.caption(
            "The displayed values correspond to the PDFMalware2022 dataset "
            "used for this project."
        )

        st.divider()

        # ==================================================
        # TRAIN / TEST SPLIT
        # ==================================================

        st.markdown("### 🔀 Training Configuration")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Training Samples",
            "8,018"
        )

        col2.metric(
            "Test Samples",
            "2,005"
        )

        col3.metric(
            "Split",
            "80% / 20%"
        )

        st.divider()

        # ==================================================
        # MODEL PERFORMANCE
        # ==================================================

        st.markdown("### 📈 Model Performance")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Accuracy",
            "98.85%"
        )

        col2.metric(
            "Precision",
            "98.57%"
        )

        col3.metric(
            "Recall",
            "99.37%"
        )

        col4.metric(
            "F1 Score",
            "98.97%"
        )

        col5.metric(
            "ROC-AUC",
            "0.9991"
        )

        st.caption(
            "Metrics are calculated on the held-out test split."
        )

        st.divider()

        # ==================================================
        # CONFUSION MATRIX
        # ==================================================

        st.markdown("### 🧩 Confusion Matrix")

        confusion_matrix = pd.DataFrame(
            [
                [878, 16],
                [7, 1104]
            ],
            index=["Actual Benign", "Actual Malicious"],
            columns=["Predicted Benign", "Predicted Malicious"]
        )

        st.dataframe(
            confusion_matrix,
            use_container_width=True
        )

        st.caption(
            "Rows represent the actual class and columns represent "
            "the predicted class."
        )

        st.divider()

        # ==================================================
        # FEATURES
        # ==================================================

        st.markdown("### 🔢 Feature Engineering")

        st.write(
            "The classifier uses 31 static PDF features extracted "
            "without executing the PDF."
        )

        feature_groups = {
            "File / document properties": [
                "PdfSize",
                "MetadataSize",
                "Pages",
                "XrefLength",
                "TitleCharacters",
                "isEncrypted",
                "PageNo"
            ],

            "PDF structural features": [
                "Header",
                "Obj",
                "Endobj",
                "Stream",
                "Endstream",
                "Xref",
                "Trailer",
                "StartXref",
                "Encrypt",
                "ObjStm"
            ],

            "Security-relevant features": [
                "JS",
                "Javascript",
                "AA",
                "OpenAction",
                "Acroform",
                "JBIG2Decode",
                "RichMedia",
                "Launch",
                "EmbeddedFile",
                "XFA"
            ],

            "Content features": [
                "EmbeddedFiles",
                "Images",
                "Text",
                "Colors"
            ]
        }

        for group_name, feature_list in feature_groups.items():

            with st.expander(group_name):

                st.write(
                    ", ".join(feature_list)
                )

        st.divider()

        # ==================================================
        # LIMITATIONS
        # ==================================================

        st.markdown("### ⚠️ Important Limitations")

        st.info(
            "This is an academic research classifier for defensive "
            "PDF malware analysis. The reported probabilities are "
            "model estimates and should not be treated as definitive "
            "malware verdicts. Static analysis can produce false "
            "positives and false negatives."
        )

    else:

        st.warning(
            "Trained model not found. "
            "Run `python ml/train.py` before using the model."
        )

else:
    st.subheader("About the project")
    st.markdown("""
**PDFShield AI** is an academic defensive-security project for the Data Science for Security course.

**Core concepts:** static PDF feature engineering, supervised machine learning, evaluation metrics, and adversarial robustness analysis.

**Important limitation:** the detector is a research/academic classifier, not an antivirus product. Static ML can produce false positives and false negatives.
""")
