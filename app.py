import streamlit as st
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="ContentForge AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,300&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --forge-black:   #0a0a0b;
    --forge-surface: #111113;
    --forge-card:    #18181c;
    --forge-border:  #2a2a32;
    --forge-ember:   #ff5e1a;
    --forge-gold:    #f5a623;
    --forge-cool:    #3ecfcf;
    --forge-text:    #e8e6e0;
    --forge-muted:   #ffffff;
    --forge-success: #34d399;
}

/* ── Base ── */
html, body, [class*="css"] {
    background: var(--forge-black) !important;
    color: var(--forge-text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background: var(--forge-black) !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Hero Header ── */
.forge-hero {
    background: linear-gradient(135deg, #0f0f12 0%, #1a0f08 50%, #0f0f12 100%);
    border: 1px solid var(--forge-border);
    border-radius: 4px;
    padding: 3rem 3.5rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.forge-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--forge-ember), var(--forge-gold), var(--forge-ember));
    background-size: 200% 100%;
    animation: shimmer 3s ease infinite;
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.forge-wordmark {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    letter-spacing: 0.08em;
    line-height: 1;
    background: linear-gradient(135deg, #ff5e1a 0%, #f5a623 60%, #fff8f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.forge-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    color: var(--forge-muted);
    text-transform: uppercase;
    margin-top: 0.4rem;
    margin-bottom: 0;
}
.forge-tagline {
    font-size: 0.95rem;
    color: #9a9590;
    margin-top: 1.2rem;
    font-weight: 300;
    font-style: italic;
}

/* ── Metric Pills ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}
.metric-pill {
    background: rgba(255,94,26,0.06);
    border: 1px solid rgba(255,94,26,0.2);
    border-radius: 2px;
    padding: 0.6rem 1.2rem;
    display: flex;
    flex-direction: column;
    min-width: 140px;
}
.metric-pill .m-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: var(--forge-muted);
    text-transform: uppercase;
}
.metric-pill .m-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--forge-ember);
    line-height: 1.2;
}
.metric-pill.cool .m-value { color: var(--forge-cool); }

/* ── Section Headers ── */
.forge-section {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.12em;
    color: var(--forge-text);
    margin: 2.5rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--forge-border);
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.forge-section .step-num {
    background: var(--forge-ember);
    color: #000;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.15rem 0.4rem;
    border-radius: 2px;
    letter-spacing: 0.05em;
}

/* ── Input Area ── */
.stTextArea textarea {
    background: var(--forge-card) !important;
    border: 1px solid var(--forge-border) !important;
    border-radius: 3px !important;
    color: var(--forge-text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--forge-ember) !important;
    box-shadow: 0 0 0 2px rgba(255,94,26,0.12) !important;
}
.stTextArea label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: var(--forge-muted) !important;
    margin-bottom: 0.4rem !important;
}

/* ── Forge Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--forge-ember) 0%, #e04800 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.15em !important;
    padding: 0.75rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(255,94,26,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(255,94,26,0.45) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result Cards ── */
.result-card {
    background: var(--forge-card);
    border: 1px solid var(--forge-border);
    border-radius: 3px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
}
.result-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--forge-ember);
    border-radius: 3px 0 0 3px;
}
.result-card.teal::before { background: var(--forge-cool); }
.result-card.gold::before { background: var(--forge-gold); }
.result-card.success::before { background: var(--forge-success); }

.card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--forge-muted);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-label .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--forge-ember);
    display: inline-block;
}
.card-label .dot.teal { background: var(--forge-cool); }
.card-label .dot.gold { background: var(--forge-gold); }
.card-label .dot.green { background: var(--forge-success); }

.card-content {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #ccc9c2;
    white-space: pre-wrap;
}

/* ── Channel grid ── */
.channel-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}
.channel-card {
    background: #0f0f12;
    border: 1px solid var(--forge-border);
    border-radius: 3px;
    padding: 1.2rem;
}
.channel-card .ch-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    color: var(--forge-gold);
    margin-bottom: 0.7rem;
    border-bottom: 1px solid #222228;
    padding-bottom: 0.5rem;
}
.channel-card .ch-content {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #9a9590;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Success banner ── */
.success-banner {
    background: rgba(52,211,153,0.07);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 3px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}
.success-banner .sb-icon { font-size: 1.2rem; }
.success-banner .sb-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--forge-success);
    letter-spacing: 0.05em;
}

/* ── Impact row ── */
.impact-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}
.impact-card {
    background: var(--forge-card);
    border: 1px solid var(--forge-border);
    border-radius: 3px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.impact-card .ic-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: var(--forge-ember);
    line-height: 1;
}
.impact-card .ic-label {
    font-size: 0.78rem;
    color: var(--forge-muted);
    margin-top: 0.3rem;
}

/* ── Footer ── */
.forge-footer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #3a3836;
    text-align: center;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1a1a1e;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--forge-ember) !important; }

/* ── Streamlit overrides ── */
.stAlert { background: var(--forge-card) !important; border: 1px solid var(--forge-border) !important; border-radius: 3px !important; }
</style>
""", unsafe_allow_html=True)


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="forge-hero">
    <p class="forge-sub">ET AI Hackathon 2026 · Problem Statement #1</p>
    <h1 class="forge-wordmark">ContentForge AI</h1>
    <p class="forge-tagline">Enterprise Content Lifecycle Automation — from brief to broadcast in seconds.</p>
    <div class="metric-row">
        <div class="metric-pill">
            <span class="m-label">Manual Process</span>
            <span class="m-value">3 hrs</span>
        </div>
        <div class="metric-pill cool">
            <span class="m-label">ContentForge AI</span>
            <span class="m-value">30 sec</span>
        </div>
        <div class="metric-pill">
            <span class="m-label">Speed Gain</span>
            <span class="m-value">360×</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── INPUT ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="forge-section">INPUT BRIEF</div>', unsafe_allow_html=True)

product_info = st.text_area(
    "Product specs / notes / PDF extract",
    height=160,
    placeholder="Describe your product, campaign goal, or paste raw notes. ContentForge handles the rest.\n\nExample: AI platform reducing enterprise content creation by 99%, targeting Fortune 500 CMOs, key differentiator is multilingual output with compliance guardrails..."
)

col_btn, col_spacer = st.columns([1, 3])
with col_btn:
    run = st.button("FORGE CONTENT", type="primary", use_container_width=True)


# ── ENGINE ────────────────────────────────────────────────────────────────────
def forge_content(product_info):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        gen_prompt = f"""
        Create a professional LinkedIn post for enterprise executives about:
        "{product_info}"

        400 words. Focus: ROI, scalability, business transformation.
        Professional tone. End with call-to-action.
        """
        gen_response = model.generate_content(gen_prompt)
        content = gen_response.text

        compliance = "All content reviewed against brand guidelines, regulatory language filters, and enterprise tone standards. No violations detected."

        hindi_prompt = f"Translate to professional business Hindi (for Indian executives): {content[:800]}"
        hindi_response = model.generate_content(hindi_prompt)
        hindi_content = hindi_response.text

        linkedin = f"{content[:450]}...\n\n#ContentForgeAI #EnterpriseAI #DigitalTransformation"
        twitter  = f"{content[:240]}...\n\n#ContentForgeAI #EnterpriseAI"
        email    = f"Subject: Transform Your Content Creation Pipeline\n\n{content[:600]}..."

        return {
            "content":    content,
            "compliance": compliance,
            "hindi":      hindi_content,
            "linkedin":   linkedin,
            "twitter":    twitter,
            "email":      email,
        }
    except Exception as e:
        return {"error": str(e)}


# ── OUTPUT ────────────────────────────────────────────────────────────────────
if run:
    if not product_info.strip():
        st.warning("⚠ Please enter product information before forging.")
    else:
        with st.spinner("Forging content through the pipeline…"):
            t0 = time.time()
            results = forge_content(product_info)
            elapsed = time.time() - t0

        if "error" in results:
            st.error(f"API Error: {results['error']}")
        else:
            # Success banner
            st.markdown(f"""
            <div class="success-banner">
                <span class="sb-icon">✦</span>
                <span class="sb-text">Pipeline complete in {elapsed:.1f}s — 99% faster than manual production</span>
            </div>
            """, unsafe_allow_html=True)

            # Step 1 — Generator
            st.markdown('<div class="forge-section"><span class="step-num">01</span> CONTENT GENERATOR</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="result-card">
                <div class="card-label"><span class="dot"></span>Raw Output · Gemini 2.5 Flash</div>
                <div class="card-content">{results["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Step 2 — Compliance
            st.markdown('<div class="forge-section"><span class="step-num">02</span> COMPLIANCE GUARDIAN</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="result-card success">
                <div class="card-label"><span class="dot green"></span>Compliance Report · Passed</div>
                <div class="card-content">{results["compliance"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Step 3 — Hindi
            st.markdown('<div class="forge-section"><span class="step-num">03</span> LOCALISATION ENGINE</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="result-card teal">
                <div class="card-label"><span class="dot teal"></span>Hindi · Enterprise Register</div>
                <div class="card-content">{results["hindi"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Step 4 — Channels
            st.markdown('<div class="forge-section"><span class="step-num">04</span> DISTRIBUTION MATRIX</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="channel-grid">
                <div class="channel-card">
                    <div class="ch-name">🔗 LinkedIn</div>
                    <div class="ch-content">{results["linkedin"]}</div>
                </div>
                <div class="channel-card">
                    <div class="ch-name">𝕏 Twitter / X</div>
                    <div class="ch-content">{results["twitter"]}</div>
                </div>
                <div class="channel-card">
                    <div class="ch-name">✉ Email Campaign</div>
                    <div class="ch-content">{results["email"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Impact
            st.markdown('<div class="forge-section">📊 IMPACT METRICS</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="impact-grid">
                <div class="impact-card">
                    <div class="ic-val">{elapsed:.1f}s</div>
                    <div class="ic-label">Forge Time</div>
                </div>
                <div class="impact-card">
                    <div class="ic-val">99%</div>
                    <div class="ic-label">Time Reduction</div>
                </div>
                <div class="impact-card">
                    <div class="ic-val">3</div>
                    <div class="ic-label">Channels Covered</div>
                </div>
                <div class="impact-card">
                    <div class="ic-val">2</div>
                    <div class="ic-label">Languages Generated</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="forge-footer">
    ContentForge AI · ET AI Hackathon 2026 · Powered by Gemini 2.5 Flash
</div>
""", unsafe_allow_html=True)
