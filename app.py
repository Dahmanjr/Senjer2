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

# ─── LOGO ──────────────────────────────────────────────────────────────────────

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

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    background-color: #080808 !important;
    color: #e8dcc8;
    font-family: 'Montserrat', sans-serif;
    font-weight: 300;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Page ── */
.page {
    max-width: 700px;
    margin: 0 auto;
    padding: 0 20px;
}

/* ── Header ── */
.brand-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 28px;
    border-bottom: 1px solid rgba(212,175,110,0.15);
    margin-bottom: 32px;
}
.brand-logo {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 16px;
    border: 1px solid rgba(212,175,110,0.25);
    box-shadow: 0 0 40px rgba(212,175,110,0.07);
}
.brand-logo-placeholder {
    width: 100px; height: 100px;
    border-radius: 50%;
    background: #111;
    border: 1px solid rgba(212,175,110,0.25);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem; color: #d4af6e;
    margin-bottom: 16px;
}
.brand-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.9rem;
    font-weight: 400;
    letter-spacing: 0.38em;
    color: #d4af6e;
    text-transform: uppercase;
    line-height: 1;
}
.brand-rule {
    width: 36px; height: 1px;
    background: rgba(212,175,110,0.35);
    margin: 10px auto;
}
.brand-sub {
    font-size: 0.6rem;
    letter-spacing: 0.45em;
    color: rgba(212,175,110,0.4);
    text-transform: uppercase;
}

/* ── Messages area ── */
.messages-wrap {
    padding-bottom: 140px;
}

/* ── Single message row ── */
.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    margin-bottom: 24px;
}
.msg-row.user-row { flex-direction: row-reverse; }

/* ── Avatar ── */
.av {
    width: 32px; height: 32px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px;
    letter-spacing: 0.05em;
}
.av.bot-av {
    background: #131313;
    border: 1px solid rgba(212,175,110,0.22);
    color: #d4af6e;
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px;
}
.av.user-av {
    background: #131313;
    border: 1px solid rgba(212,175,110,0.15);
    color: rgba(212,175,110,0.5);
    font-size: 13px;
}

/* ── Bubble ── */
.bubble {
    max-width: 75%;
    padding: 15px 20px;
    font-size: 0.9rem;
    line-height: 1.75;
    font-family: 'Montserrat', sans-serif;
    font-weight: 300;
    word-break: break-word;
}

/* Bot bubble */
.bot-bubble {
    background: #111111;
    border: 1px solid rgba(212,175,110,0.18);
    border-radius: 2px 18px 18px 18px;
    color: #f0e6d2;
    box-shadow: inset 0 0 0 1px rgba(212,175,110,0.04),
                0 4px 24px rgba(0,0,0,0.35);
}

/* Gold left accent bar on bot bubble */
.bot-bubble-wrap {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    gap: 0;
    max-width: 75%;
}
.bot-accent {
    width: 2px;
    border-radius: 2px;
    background: linear-gradient(to bottom, #d4af6e, rgba(212,175,110,0.2));
    flex-shrink: 0;
    margin-right: 10px;
    min-height: 100%;
}

/* User bubble */
.user-bubble {
    background: #131313;
    border: 1px solid rgba(212,175,110,0.22);
    border-radius: 18px 2px 18px 18px;
    color: #f5eddc;
    text-align: right;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* sender label */
.sender-label {
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 5px;
    font-family: 'Montserrat', sans-serif;
    font-weight: 400;
}
.bot-label  { color: rgba(212,175,110,0.45); }
.user-label { color: rgba(212,175,110,0.3); text-align: right; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 50px 20px 40px;
}
.empty-diamond {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    color: rgba(212,175,110,0.25);
    margin-bottom: 24px;
    display: block;
    letter-spacing: 0.4em;
}
.empty-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.45rem;
    font-weight: 400;
    color: #d4af6e;
    letter-spacing: 0.06em;
    margin-bottom: 14px;
}
.empty-desc {
    font-size: 0.78rem;
    color: rgba(212,175,110,0.38);
    line-height: 1.9;
    letter-spacing: 0.04em;
    max-width: 320px;
    margin: 0 auto;
}

/* ── Luxury Chat Input Styling ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(700px, 100%) !important;
    padding: 20px 24px 30px !important;
    background: linear-gradient(to top, #080808 85%, rgba(8,8,8,0)) !important;
    z-index: 999 !important;
}

[data-testid="stChatInput"] > div {
    border: 1px solid rgba(212, 175, 110, 0.3) !important;
    border-radius: 28px !important;
    background: #0d0d0d !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(212, 175, 110, 0.05) !important;
    transition: all 0.3s ease-in-out !important;
    padding: 4px 8px !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: rgba(212, 175, 110, 0.75) !important;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(212, 175, 110, 0.18) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #f0e6d2 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 300 !important;
    caret-color: #d4af6e !important;
    resize: none !important;
    letter-spacing: 0.03em !important;
    padding: 12px 16px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(212, 175, 110, 0.35) !important;
    letter-spacing: 0.04em !important;
    font-style: italic !important;
}

button[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, rgba(212, 175, 110, 0.25), rgba(212, 175, 110, 0.05)) !important;
    border: 1px solid rgba(212, 175, 110, 0.4) !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s ease !important;
    margin-right: 4px !important;
}

button[data-testid="stChatInputSubmitButton"]:hover {
    background: #d4af6e !important;
    border-color: #d4af6e !important;
    box-shadow: 0 0 15px rgba(212, 175, 110, 0.5) !important;
    transform: scale(1.05);
}

button[data-testid="stChatInputSubmitButton"] svg {
    fill: #d4af6e !important;
    transition: fill 0.3s ease !important;
}

button[data-testid="stChatInputSubmitButton"]:hover svg {
    fill: #080808 !important;
}

/* ── Mobile ── */
@media (max-width: 480px) {
    .brand-logo  { width: 80px; height: 80px; }
    .brand-name  { font-size: 1.45rem; letter-spacing: 0.3em; }
    .bubble      { font-size: 0.85rem; padding: 13px 16px; }
    .page        { padding: 0 12px; }
    .bot-bubble-wrap, .bubble { max-width: 86%; }
    [data-testid="stChatInput"] { padding: 12px 14px 20px !important; }
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
    except Exception:
        return "عذراً، حدث خطأ مؤقت. حاول مرة ثانية بعد لحظة 🙏"


# ─── SESSION ───────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user-{int(time.time())}"


# ─── RENDER ────────────────────────────────────────────────────────────────────

st.markdown('<div class="page">', unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="brand-header">
    {logo_html}
    <div class="brand-name">Senjer</div>
    <div class="brand-rule"></div>
    <div class="brand-sub">Fragrances</div>
</div>
""", unsafe_allow_html=True)

# Messages
st.markdown('<div class="messages-wrap">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-diamond">✦ ✦ ✦</span>
        <div class="empty-title">كيف يمكنني مساعدتك؟</div>
        <div class="empty-desc">
            اسألني عن عطورنا، أسعارنا، أو المجموعات المتاحة<br><br>
            Ask me anything about our fragrances, prices, or collections
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user-row">
                <div class="av user-av">↑</div>
                <div style="max-width:75%">
                    <div class="sender-label user-label">You</div>
                    <div class="bubble user-bubble">{msg["content"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
                <div class="av bot-av">✦</div>
                <div style="max-width:75%; display:flex; flex-direction:column;">
                    <div class="sender-label bot-label">Senjer</div>
                    <div style="display:flex; flex-direction:row; align-items:stretch;">
                        <div class="bot-accent"></div>
                        <div class="bubble bot-bubble">{msg["content"]}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Input
if prompt := st.chat_input("اكتب رسالتك هنا... / Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(""):
        reply = ask_flowise(prompt, st.session_state.session_id)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
