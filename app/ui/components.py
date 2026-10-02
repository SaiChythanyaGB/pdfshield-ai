
import streamlit as st

def section_heading(kicker, title, description=None):
    html = f"""
    <div class="section-kicker">{kicker}</div>
    <div class="section-title">{title}</div>
    """
    if description:
        html += f'<div style="color:#94a3b8;margin-top:-.65rem;margin-bottom:1rem;font-size:.88rem;">{description}</div>'
    st.markdown(html, unsafe_allow_html=True)

def glass_card(icon, title, text):
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-icon">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def hero():
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">AI Security Analysis Platform</div>
        <h1>🛡️ PDFShield AI</h1>
        <p>
            AI-powered static PDF malware detection and adversarial robustness
            analysis — designed for defensive cybersecurity research.
        </p>
        <div class="status-pill">
            <span class="status-dot"></span>
            Defensive analysis mode active
        </div>
    </div>
    """, unsafe_allow_html=True)

def verdict_card(prediction, probability):
    malicious = prediction == 1
    css = "verdict-malicious" if malicious else "verdict-benign"
    icon = "🚨" if malicious else "✓"
    label = "MALICIOUS PDF DETECTED" if malicious else "PDF CLASSIFIED AS BENIGN"
    note = "Model-estimated malicious risk" if malicious else "No malicious classification from the current model"
    st.markdown(f"""
    <div class="verdict {css}">
        <div class="verdict-icon">{icon}</div>
        <div class="verdict-label">{label}</div>
        <div class="verdict-note">{note}: {probability * 100:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

def pipeline():
    steps = [
        ("01", "PDF Upload"),
        ("02", "Static Analysis"),
        ("03", "31 Features"),
        ("04", "Preprocessing"),
        ("05", "Random Forest"),
        ("06", "Verdict"),
        ("07", "Robustness"),
    ]
    html = '<div class="pipeline">'
    for n, title in steps:
        html += f"""
        <div class="pipeline-step">
            <div class="step-no">{n}</div>
            <div class="step-title">{title}</div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
