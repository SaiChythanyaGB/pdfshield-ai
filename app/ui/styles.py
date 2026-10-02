
import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --ps-bg: #070b14;
        --ps-panel: rgba(15, 23, 42, 0.72);
        --ps-border: rgba(148, 163, 184, 0.16);
        --ps-text: #e5eefc;
        --ps-muted: #94a3b8;
        --ps-cyan: #22d3ee;
        --ps-blue: #60a5fa;
        --ps-green: #34d399;
        --ps-red: #fb7185;
        --ps-yellow: #fbbf24;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(34,211,238,.10), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(96,165,250,.10), transparent 28%),
            linear-gradient(135deg, #050812 0%, #09111f 48%, #050812 100%);
        color: var(--ps-text);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: .18;
        background-image:
            linear-gradient(rgba(148,163,184,.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,.07) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: linear-gradient(to bottom, black, transparent 88%);
        animation: gridDrift 18s linear infinite;
    }

    @keyframes gridDrift {
        from { transform: translate3d(0,0,0); }
        to { transform: translate3d(42px,42px,0); }
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(7,11,20,.96), rgba(8,15,28,.94));
        border-right: 1px solid var(--ps-border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
    }

    .brand {
        display:flex;
        align-items:center;
        gap:.75rem;
        margin-bottom:1.4rem;
    }

    .brand-icon {
        width:44px;
        height:44px;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:1.35rem;
        background: linear-gradient(135deg, rgba(34,211,238,.22), rgba(96,165,250,.12));
        border:1px solid rgba(34,211,238,.30);
        box-shadow: 0 0 28px rgba(34,211,238,.12);
    }

    .brand-name {
        font-weight:800;
        letter-spacing:-.03em;
        font-size:1.15rem;
    }

    .brand-sub {
        color:var(--ps-muted);
        font-size:.72rem;
        margin-top:.1rem;
    }

    .hero {
        position:relative;
        overflow:hidden;
        padding:2.5rem;
        border:1px solid rgba(34,211,238,.20);
        border-radius:28px;
        background:
            radial-gradient(circle at 82% 18%, rgba(34,211,238,.16), transparent 24%),
            radial-gradient(circle at 65% 75%, rgba(96,165,250,.12), transparent 28%),
            linear-gradient(135deg, rgba(15,23,42,.88), rgba(7,11,20,.72));
        box-shadow: 0 20px 70px rgba(0,0,0,.30);
    }

    .hero::after {
        content:"";
        position:absolute;
        width:260px;
        height:260px;
        right:-80px;
        top:-100px;
        border-radius:50%;
        border:1px solid rgba(34,211,238,.18);
        box-shadow:0 0 70px rgba(34,211,238,.08);
        animation:pulseRing 4s ease-in-out infinite;
    }

    @keyframes pulseRing {
        0%,100% { transform:scale(.92); opacity:.45; }
        50% { transform:scale(1.08); opacity:.9; }
    }

    .eyebrow {
        color:var(--ps-cyan);
        font-size:.78rem;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:.16em;
        margin-bottom:.75rem;
    }

    .hero h1 {
        font-size:clamp(2.2rem, 5vw, 4rem);
        line-height:1;
        letter-spacing:-.055em;
        margin:0;
    }

    .hero p {
        color:#aab8cc;
        font-size:1.05rem;
        max-width:720px;
        line-height:1.7;
        margin-top:1rem;
    }

    .status-pill {
        display:inline-flex;
        align-items:center;
        gap:.45rem;
        margin-top:1.25rem;
        padding:.45rem .75rem;
        border-radius:999px;
        color:#b9f6df;
        background:rgba(52,211,153,.08);
        border:1px solid rgba(52,211,153,.20);
        font-size:.78rem;
        font-weight:600;
    }

    .status-dot {
        width:7px;
        height:7px;
        border-radius:50%;
        background:var(--ps-green);
        box-shadow:0 0 12px rgba(52,211,153,.8);
        animation:blink 1.8s infinite;
    }

    @keyframes blink {
        0%,100% { opacity:.45; }
        50% { opacity:1; }
    }

    .glass-card {
        padding:1.2rem;
        border-radius:20px;
        border:1px solid var(--ps-border);
        background:linear-gradient(145deg, rgba(15,23,42,.76), rgba(9,15,27,.62));
        box-shadow:0 14px 45px rgba(0,0,0,.18);
        transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease;
        height:100%;
    }

    .glass-card:hover {
        transform:translateY(-3px);
        border-color:rgba(34,211,238,.28);
        box-shadow:0 18px 55px rgba(0,0,0,.28);
    }

    .card-icon {
        font-size:1.35rem;
        margin-bottom:.6rem;
    }

    .card-title {
        font-weight:700;
        font-size:1rem;
        margin-bottom:.35rem;
    }

    .card-text {
        color:var(--ps-muted);
        line-height:1.55;
        font-size:.88rem;
    }

    .metric-card {
        padding:1.25rem;
        border-radius:20px;
        border:1px solid var(--ps-border);
        background:linear-gradient(145deg, rgba(15,23,42,.80), rgba(9,15,27,.60));
        position:relative;
        overflow:hidden;
    }

    .metric-card::before {
        content:"";
        position:absolute;
        left:0;
        top:0;
        width:100%;
        height:2px;
        background:linear-gradient(90deg, transparent, var(--ps-cyan), transparent);
        opacity:.7;
    }

    .metric-label {
        color:var(--ps-muted);
        font-size:.78rem;
        text-transform:uppercase;
        letter-spacing:.08em;
    }

    .metric-value {
        font-size:1.8rem;
        font-weight:800;
        margin-top:.35rem;
        letter-spacing:-.04em;
    }

    .section-kicker {
        color:var(--ps-cyan);
        font-size:.75rem;
        text-transform:uppercase;
        letter-spacing:.14em;
        font-weight:700;
        margin-bottom:.35rem;
    }

    .section-title {
        font-size:1.45rem;
        font-weight:750;
        letter-spacing:-.035em;
        margin-bottom:1rem;
    }

    .pipeline {
        display:flex;
        align-items:stretch;
        gap:.6rem;
        overflow-x:auto;
        padding:.25rem 0 .8rem;
    }

    .pipeline-step {
        min-width:145px;
        padding:1rem;
        border-radius:16px;
        border:1px solid var(--ps-border);
        background:rgba(15,23,42,.62);
        position:relative;
    }

    .pipeline-step:not(:last-child)::after {
        content:"→";
        position:absolute;
        right:-.65rem;
        top:50%;
        transform:translateY(-50%);
        color:var(--ps-cyan);
        font-weight:800;
        z-index:2;
    }

    .step-no {
        color:var(--ps-cyan);
        font-size:.7rem;
        font-weight:800;
    }

    .step-title {
        font-size:.82rem;
        font-weight:700;
        margin-top:.4rem;
    }

    .scanner-drop {
        padding:2.4rem;
        border-radius:24px;
        border:1px dashed rgba(34,211,238,.35);
        background:radial-gradient(circle at center, rgba(34,211,238,.08), rgba(15,23,42,.55));
        text-align:center;
        margin-bottom:1rem;
    }

    .scanner-icon {
        font-size:2.5rem;
        margin-bottom:.5rem;
    }

    .scanner-title {
        font-size:1.2rem;
        font-weight:750;
    }

    .scanner-sub {
        color:var(--ps-muted);
        font-size:.86rem;
        margin-top:.35rem;
    }

    .verdict {
        padding:1.8rem;
        border-radius:24px;
        text-align:center;
        border:1px solid var(--ps-border);
        background:linear-gradient(145deg, rgba(15,23,42,.85), rgba(9,15,27,.68));
        margin:1rem 0;
    }

    .verdict-benign {
        border-color:rgba(52,211,153,.28);
        box-shadow:0 0 45px rgba(52,211,153,.07);
    }

    .verdict-malicious {
        border-color:rgba(251,113,133,.30);
        box-shadow:0 0 45px rgba(251,113,133,.08);
    }

    .verdict-icon { font-size:2.4rem; }
    .verdict-label {
        font-size:1.65rem;
        font-weight:850;
        letter-spacing:-.04em;
        margin-top:.45rem;
    }

    .verdict-note {
        color:var(--ps-muted);
        font-size:.82rem;
        margin-top:.35rem;
    }

    .indicator {
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:.8rem .9rem;
        margin-bottom:.5rem;
        border-radius:13px;
        background:rgba(15,23,42,.58);
        border:1px solid rgba(148,163,184,.10);
    }

    .indicator-name { font-size:.84rem; font-weight:600; }
    .indicator-state { font-size:.75rem; font-weight:700; }
    .state-on { color:var(--ps-red); }
    .state-off { color:var(--ps-green); }

    .lab-banner {
        padding:1rem 1.2rem;
        border-radius:18px;
        border:1px solid rgba(251,191,36,.20);
        background:rgba(251,191,36,.055);
        color:#f8d98c;
    }

    .footer-note {
        color:#64748b;
        font-size:.75rem;
        text-align:center;
        padding-top:2rem;
    }

    div[data-testid="stMetric"] {
        background:transparent;
    }

    .stButton > button {
        border-radius:12px;
        border:1px solid rgba(34,211,238,.24);
        background:linear-gradient(135deg, rgba(34,211,238,.14), rgba(96,165,250,.08));
        transition:all .2s ease;
    }

    .stButton > button:hover {
        border-color:rgba(34,211,238,.50);
        box-shadow:0 0 25px rgba(34,211,238,.10);
        transform:translateY(-1px);
    }

    [data-testid="stFileUploader"] {
        border-radius:18px;
    }

    </style>
    """, unsafe_allow_html=True)
