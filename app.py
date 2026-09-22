"""
Senjer Fragrances – AI Chat Assistant
Streamlit app — deploy to Streamlit Cloud

Requirements (requirements.txt):
    streamlit
    requests
"""

import base64
import time
import requests
import streamlit as st
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────────

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/199a8171-8790-49dc-badc-56a6ee067874"

# ─── PAGE SETUP ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Senjer Fragrances",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── LOGO AS BASE64 ────────────────────────────────────────────────────────────

def get_logo_b64():
    logo_path = Path(__file__).parent / "logo.jpeg"
    if logo_path.exists():
        return base64.b64encode(logo_path.read_bytes()).decode()
    return None

logo_b64 = get_logo_b64()
logo_html = (
    f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo" alt="Senjer Fragrances"/>'
    if logo_b64
    else '<div class="brand-logo-placeholder">SJ</div>'
)

# ─── CSS ───────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Montserrat:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    background-color: #0a0a0a !important;
    color: #d4af6e;
    font-family: 'Montserrat', sans-serif;
    font-weight: 300;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* Remove default padding */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Page shell ── */
.page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    max-width: 680px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
}

/* ── Header ── */
.brand-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 28px;
    border-bottom: 1px solid rgba(212,175,110,0.18);
    margin-bottom: 28px;
}
.brand-logo {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 18px;
    border: 1px solid rgba(212,175,110,0.3);
    box-shadow: 0 0 28px rgba(212,175,110,0.08);
}
.brand-logo-placeholder {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: #111;
    border: 1px solid rgba(212,175,110,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    color: #d4af6e;
    margin-bottom: 18px;
}
.brand-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: 0.35em;
    color: #d4af6e;
    text-transform: uppercase;
    line-height: 1;
}
.brand-line {
    width: 40px;
    height: 1px;
    background: rgba(212,175,110,0.4);
    margin: 10px auto;
}
.brand-sub {
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    color: rgba(212,175,110,0.45);
    text-transform: uppercase;
}

/* ── Messages ── */
.messages-wrap {
    padding-bottom: 110px;
}

.msg-block {
    display: flex;
    margin-bottom: 20px;
    gap: 10px;
    align-items: flex-end;
}
.msg-block.user-block { flex-direction: row-reverse; }

.avatar-dot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
}
.avatar-dot.bot-av {
    background: rgba(212,175,110,0.08);
    border: 1px solid rgba(212,175,110,0.2);
    color: #d4af6e;
}
.avatar-dot.user-av {
    background: rgba(212,175,110,0.05);
    border: 1px solid rgba(212,175,110,0.15);
    color: rgba(212,175,110,0.6);
}

.bubble {
    max-width: 80%;
    padding: 13px 17px;
    font-size: 0.88rem;
    line-height: 1.7;
    font-weight: 300;
    font-family: 'Montserrat', sans-serif;
}
.bot-bubble {
    background: rgba(212,175,110,0.05);
    border: 1px solid rgba(212,175,110,0.13);
    border-radius: 0 16px 16px 16px;
    color: #e8dcc8;
}
.user-bubble {
    background: rgba(212,175,110,0.1);
    border: 1px solid rgba(212,175,110,0.22);
    border-radius: 16px 0 16px 16px;
    color: #f0e6d0;
    text-align: right;
    margin-left: auto;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px 40px;
}
.empty-icon {
    font-size: 2.4rem;
    margin-bottom: 20px;
    opacity: 0.7;
}
.empty-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: #d4af6e;
    letter-spacing: 0.05em;
    margin-bottom: 10px;
}
.empty-desc {
    font-size: 0.8rem;
    color: rgba(212,175,110,0.4);
    line-height: 1.8;
    letter-spacing: 0.03em;
    max-width: 300px;
    margin: 0 auto;
}

/* ── Input box ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(680px, 100%) !important;
    padding: 16px 20px 20px !important;
    background: linear-gradient(to top, #0a0a0a 75%, transparent) !important;
    z-index: 999 !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(212,175,110,0.05) !important;
    border: 1px solid rgba(212,175,110,0.25) !important;
    border-radius: 14px !important;
    color: #e8dcc8 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 300 !important;
    caret-color: #d4af6e !important;
    resize: none !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(212,175,110,0.3) !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(212,175,110,0.45) !important;
    box-shadow: 0 0 0 3px rgba(212,175,110,0.06) !important;
    outline: none !important;
}
button[data-testid="stChatInputSubmitButton"] {
    background: rgba(212,175,110,0.12) !important;
    border: 1px solid rgba(212,175,110,0.28) !important;
    border-radius: 10px !important;
    color: #d4af6e !important;
    transition: background 0.2s !important;
}
button[data-testid="stChatInputSubmitButton"]:hover {
    background: rgba(212,175,110,0.22) !important;
}
button[data-testid="stChatInputSubmitButton"] svg { fill: #d4af6e !important; }

/* ── Mobile tweaks ── */
@media (max-width: 480px) {
    .brand-logo { width: 85px; height: 85px; }
    .brand-name  { font-size: 1.5rem; letter-spacing: 0.28em; }
    .bubble      { font-size: 0.84rem; }
    .page        { padding: 0 14px; }
}
</style>
""", unsafe_allow_html=True)


# ─── FLOWISE ───────────────────────────────────────────────────────────────────

def ask_flowise(question: str, session_id: str) -> str:
    try:
        resp = requests.post(
            FLOWISE_URL,
            json={"question": question, "overrideConfig": {"sessionId": session_id}},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return (
            data.get("text")
            or data.get("answer")
            or data.get("output")
            or data.get("response")
            or "عذراً، لم أفهم. ممكن تعيد السؤال؟"
        )
    except Exception as e:
        return "عذراً، حدث خطأ مؤقت. حاول مرة ثانية بعد لحظة 🙏"


# ─── SESSION ───────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user-{int(time.time())}"


# ─── RENDER PAGE ───────────────────────────────────────────────────────────────

st.markdown('<div class="page">', unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="brand-header">
    {logo_html}
    <div class="brand-name">Senjer</div>
    <div class="brand-line"></div>
    <div class="brand-sub">Fragrances</div>
</div>
""", unsafe_allow_html=True)

# Messages
st.markdown('<div class="messages-wrap">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">✦</div>
        <div class="empty-title">كيف يمكنني مساعدتك؟</div>
        <div class="empty-desc">
            اسألني عن عطورنا، الأسعار، أو المجموعات المتاحة.<br><br>
            Ask me anything about our fragrances, prices, or collections.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-block user-block">
                <div class="avatar-dot user-av">↑</div>
                <div class="bubble user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-block">
                <div class="avatar-dot bot-av">✦</div>
                <div class="bubble bot-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── INPUT ─────────────────────────────────────────────────────────────────────

if prompt := st.chat_input("اكتب رسالتك... / Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(""):
        reply = ask_flowise(prompt, st.session_state.session_id)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
