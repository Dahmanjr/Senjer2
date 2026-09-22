"""
Senjer Fragrances – AI Chat Assistant
Streamlit app — deploy to Streamlit Cloud (streamlit.io)

Requirements (requirements.txt):
    streamlit
    requests
"""

import time
import requests
import streamlit as st

# ─── CONFIG ────────────────────────────────────────────────────────────────────

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/199a8171-8790-49dc-badc-56a6ee067874"

# ─── PAGE SETUP ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Senjer Fragrances",
    page_icon="🌸",
    layout="centered",
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Jost:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    background-color: #0e0b08;
    color: #e8e0d4;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Layout wrapper ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 720px;
    margin: 0 auto;
    padding: 0 16px;
}

/* ── Header ── */
.brand-header {
    text-align: center;
    padding: 36px 0 20px;
    border-bottom: 1px solid rgba(200,180,140,0.15);
    margin-bottom: 24px;
}
.brand-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    letter-spacing: 0.18em;
    color: #c8b48c;
    margin: 0;
    text-transform: uppercase;
}
.brand-tagline {
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    color: rgba(200,180,140,0.5);
    margin-top: 6px;
    text-transform: uppercase;
}

/* ── Chat messages ── */
.msg-row {
    display: flex;
    margin-bottom: 18px;
    gap: 12px;
    align-items: flex-end;
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.avatar.bot  { background: rgba(200,180,140,0.12); border: 1px solid rgba(200,180,140,0.2); }
.avatar.user { background: rgba(200,180,140,0.08); border: 1px solid rgba(200,180,140,0.12); }

.bubble {
    max-width: 78%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 0.92rem;
    line-height: 1.65;
    font-weight: 300;
}
.bubble.bot {
    background: rgba(200,180,140,0.07);
    border: 1px solid rgba(200,180,140,0.12);
    border-bottom-left-radius: 4px;
    color: #e8e0d4;
}
.bubble.user {
    background: rgba(200,180,140,0.13);
    border: 1px solid rgba(200,180,140,0.2);
    border-bottom-right-radius: 4px;
    color: #f0e8da;
    text-align: right;
}

/* ── Typing indicator ── */
.typing {
    display: flex;
    gap: 5px;
    padding: 4px 2px;
    align-items: center;
}
.typing span {
    width: 6px; height: 6px;
    background: #c8b48c;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
    opacity: 0.6;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40%            { transform: translateY(-6px); opacity: 1; }
}

/* ── Input area ── */
.stChatInput {
    position: fixed !important;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: min(720px, 100%);
    padding: 16px;
    background: linear-gradient(to top, #0e0b08 70%, transparent);
    z-index: 100;
}
.stChatInput textarea {
    background: rgba(200,180,140,0.06) !important;
    border: 1px solid rgba(200,180,140,0.25) !important;
    border-radius: 12px !important;
    color: #e8e0d4 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 300 !important;
}
.stChatInput textarea::placeholder { color: rgba(200,180,140,0.35) !important; }
.stChatInput textarea:focus {
    border-color: rgba(200,180,140,0.5) !important;
    box-shadow: 0 0 0 2px rgba(200,180,140,0.08) !important;
}
button[data-testid="stChatInputSubmitButton"] {
    background: rgba(200,180,140,0.15) !important;
    border: 1px solid rgba(200,180,140,0.3) !important;
    border-radius: 8px !important;
}
button[data-testid="stChatInputSubmitButton"]:hover {
    background: rgba(200,180,140,0.25) !important;
}

/* ── Scrollable messages area ── */
.messages-area {
    flex: 1;
    overflow-y: auto;
    padding-bottom: 100px;
}

/* ── Welcome card ── */
.welcome-card {
    text-align: center;
    padding: 48px 24px;
    margin: 40px 0;
}
.welcome-icon {
    font-size: 3rem;
    margin-bottom: 20px;
}
.welcome-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 300;
    color: #c8b48c;
    margin-bottom: 10px;
    letter-spacing: 0.05em;
}
.welcome-sub {
    font-size: 0.85rem;
    color: rgba(200,180,140,0.5);
    font-weight: 300;
    line-height: 1.7;
    max-width: 360px;
    margin: 0 auto 28px;
}

/* ── Suggestion chips ── */
.chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 8px;
}
.chip {
    padding: 7px 14px;
    border: 1px solid rgba(200,180,140,0.25);
    border-radius: 20px;
    font-size: 0.78rem;
    color: rgba(200,180,140,0.7);
    cursor: pointer;
    transition: all 0.2s;
    background: rgba(200,180,140,0.04);
    font-family: 'Jost', sans-serif;
    letter-spacing: 0.03em;
}
.chip:hover {
    background: rgba(200,180,140,0.1);
    color: #c8b48c;
    border-color: rgba(200,180,140,0.4);
}
</style>
""", unsafe_allow_html=True)


# ─── FLOWISE ───────────────────────────────────────────────────────────────────

def ask_flowise(question: str, session_id: str = "streamlit-user") -> str:
    payload = {
        "question": question,
        "overrideConfig": {"sessionId": session_id},
    }
    try:
        resp = requests.post(FLOWISE_URL, json=payload, timeout=60)
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
        return f"عذراً، حدث خطأ مؤقت. حاول مرة ثانية 🙏\n\n_{e}_"


# ─── SESSION STATE ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"user-{int(time.time())}"


# ─── HEADER ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="brand-header">
    <p class="brand-name">Senjer</p>
    <p class="brand-tagline">Fragrances · مساعدك الشخصي للعطور</p>
</div>
""", unsafe_allow_html=True)


# ─── MESSAGES ──────────────────────────────────────────────────────────────────

if not st.session_state.messages:
    # Welcome screen
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-icon">🌸</div>
        <p class="welcome-title">أهلاً بيك في Senjer</p>
        <p class="welcome-sub">
            اسألني عن أي عطر، سعر، أو مجموعة.<br>
            Ask me anything about our fragrances.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips
    suggestions = [
        "شوفلي عطر حلو للصيف 🌞",
        "ايه أسعارك؟",
        "عندك sample sets؟",
        "What's your best seller?",
    ]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        if cols[i % 2].button(s, key=f"chip_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": s})
            with st.spinner(""):
                reply = ask_flowise(s, st.session_state.session_id)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

else:
    # Render conversation
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar user">👤</div>
                <div class="bubble user">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
                <div class="avatar bot">🌸</div>
                <div class="bubble bot">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)


# ─── INPUT ─────────────────────────────────────────────────────────────────────

placeholder = "اكتب سؤالك هنا... / Type your question..."
if prompt := st.chat_input(placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show typing indicator
    with st.spinner("🌸 جاري الرد..."):
        reply = ask_flowise(prompt, st.session_state.session_id)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
