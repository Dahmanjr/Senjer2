import os
import requests
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Senjer Fragrances – Fragrance Advisor",
    page_icon="🌸",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    background-color: #0d0a07 !important;
    color: #e8dfd4;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 760px; margin: 0 auto; }

.snj-header {
    text-align: center;
    padding: 48px 24px 20px;
    border-bottom: 1px solid rgba(185,155,105,0.25);
    margin-bottom: 8px;
}
.snj-wordmark {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    font-size: 11px;
    letter-spacing: 0.45em;
    color: #b99b69;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.snj-title {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    font-size: 38px;
    line-height: 1.15;
    color: #ede5d8;
    margin: 0 0 8px;
    font-style: italic;
}
.snj-subtitle {
    font-size: 13px;
    font-weight: 300;
    color: #8a7d6e;
    letter-spacing: 0.06em;
    margin: 0;
}
.snj-chat {
    padding: 24px 20px;
    min-height: 420px;
}
.snj-msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}
.snj-msg-user .bubble {
    background: #b99b69;
    color: #0d0a07;
    border-radius: 18px 18px 4px 18px;
    padding: 11px 16px;
    font-size: 14px;
    font-weight: 400;
    max-width: 72%;
    line-height: 1.55;
}
.snj-msg-bot {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
    align-items: flex-end;
    gap: 10px;
}
.snj-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #b99b69 0%, #7a5c30 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
}
.snj-msg-bot .bubble {
    background: #1c1610;
    border: 1px solid rgba(185,155,105,0.18);
    color: #e8dfd4;
    border-radius: 18px 18px 18px 4px;
    padding: 11px 16px;
    font-size: 14px;
    line-height: 1.65;
    max-width: 75%;
}
.snj-divider {
    border: none;
    border-top: 1px solid rgba(185,155,105,0.15);
    margin: 4px 20px 0;
}
.snj-input-area {
    padding: 16px 20px 28px;
    background: #0d0a07;
}
div[data-testid="stTextInput"] input {
    background: #1c1610 !important;
    border: 1px solid rgba(185,155,105,0.3) !important;
    border-radius: 30px !important;
    color: #e8dfd4 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 20px !important;
    caret-color: #b99b69;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #b99b69 !important;
    box-shadow: 0 0 0 2px rgba(185,155,105,0.15) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #4a4035 !important; }
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #b99b69 0%, #8a6e40 100%) !important;
    color: #0d0a07 !important;
    border: none !important;
    border-radius: 30px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 12px 28px !important;
    cursor: pointer !important;
    width: 100% !important;
}
div[data-testid="stButton"] button:hover { opacity: 0.88 !important; }
.snj-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 0 20px 16px;
}
.snj-chip {
    background: transparent;
    border: 1px solid rgba(185,155,105,0.3);
    color: #b99b69;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-family: 'Jost', sans-serif;
    font-weight: 300;
    letter-spacing: 0.04em;
}
.snj-error {
    background: rgba(180,60,60,0.15);
    border: 1px solid rgba(180,60,60,0.4);
    color: #e8a0a0;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 13px;
    margin: 8px 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Catalog / System Prompt ───────────────────────────────────────────────────
CATALOG = """You are Senjer, the luxury fragrance advisor for Senjer Fragrances — a premium Egyptian perfume brand.
Speak warmly, knowledgeably, and with understated elegance. Keep replies concise (2–4 short paragraphs max) unless the customer asks for detail. You support both English and Arabic — respond in whichever language the customer uses.

PRODUCT CATALOG:

=== EXTRAIT DE PARFUM — 50ml ===
| Name           | Gender   | Inspired by                           | Price   |
|----------------|----------|---------------------------------------|---------|
| Nomad          | For Him  | Paradigm – Prada                      | 699 EGP |
| Ashes          | For Him  | Terroni – Orto Parisi                 | 799 EGP |
| Frostbite      | Unisex   | Torino 21 – Xerjoff                   | 850 EGP |
| Sweet Venom    | For Him  | The Most Wanted – Azzaro              | 799 EGP |
| Crimson Dust   | Unisex   | Monkey Special – Tony Iommi/Xerjoff   | 750 EGP |
| Iron Coast     | For Him  | Megamare – Orto Parisi                | 799 EGP |
| Lost Eden      | For Him  | Hacivat – Nishane                     | 850 EGP |
| Mirage         | For Her  | Valaya Exclusive – Parfums de Marly   | 699 EGP |
| Freya          | For Her  | Libre Le Parfum – YSL                 | 750 EGP |
| Ember Cherry   | Unisex   | Cherry Smoke – Tom Ford               | 699 EGP |
| Eternal Bloom  | For Her  | Fleur Narcotique – Ex Nihilo          | 750 EGP |
| Nightfall      | For Her  | Senjer Signature Creation (original)  | 699 EGP |
| Last Chord     | Unisex   | Symphony – Louis Vuitton              | 899 EGP |

=== DISCOVERY SET ===
Senjer 5ml Samples Set — Box of 5 sample vials — 399 EGP

=== BODY SPLASH — 150ml, 250 EGP each ===
| Name           | Gender | Inspired by                          |
|----------------|--------|--------------------------------------|
| Prestige       | Him    | #3 Green – Miller et Bertaux         |
| Vision         | Him    | Imagination – Louis Vuitton          |
| Dark Pulse     | Him    | The One – Dolce & Gabbana            |
| Eclipse        | Her    | Into The Night – Bath & Body Works   |
| Sparkling Hour | Her    | Champagne Toast – Bath & Body Works  |
| Lady Berry     | Her    | Gingham Vibrant – Bath & Body Works  |
| Starlet        | Her    | In The Stars – Bath & Body Works     |
| Morning Breeze | Her    | Gingham – Bath & Body Works          |
| Silk Bloom     | Her    | Pink Chiffon – Bath & Body Works     |

GUIDELINES:
- When recommending, ask about gender preference and scent character if not stated.
- Always mention the inspiration fragrance so customers can relate.
- For ordering/availability, direct customers to WhatsApp or Instagram.
- Never invent products outside this catalog.
- Be warm, not pushy."""

# ── Gemini API call (pure requests, no SDK) ───────────────────────────────────
def call_gemini(history: list) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "⚠️ GOOGLE_API_KEY is not set. Please set it as an environment variable."

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )

    # Build contents list from history
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    payload = {
        "system_instruction": {"parts": [{"text": CATALOG}]},
        "contents": contents,
        "generationConfig": {
            "maxOutputTokens": 600,
            "temperature": 0.7,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.HTTPError as e:
        try:
            err_msg = resp.json().get("error", {}).get("message", str(e))
        except Exception:
            err_msg = str(e)
        return f"⚠️ API error: {err_msg}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="snj-header">
  <p class="snj-wordmark">Senjer Fragrances</p>
  <h1 class="snj-title">Fragrance Advisor</h1>
  <p class="snj-subtitle">Tell me your scent story — I'll find your perfect match.</p>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
chat_html = '<div class="snj-chat">'

if not st.session_state.messages:
    chat_html += """
    <div class="snj-msg-bot">
      <div class="snj-avatar">✦</div>
      <div class="bubble">
        Welcome to Senjer Fragrances. I'm here to help you discover your signature scent.<br><br>
        Whether you're searching for an extrait de parfum, a body splash, or a gift — just tell me what you're looking for.
      </div>
    </div>"""

for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += f'<div class="snj-msg-user"><div class="bubble">{msg["content"]}</div></div>'
    else:
        content = msg["content"].replace("\n", "<br>")
        chat_html += f'<div class="snj-msg-bot"><div class="snj-avatar">✦</div><div class="bubble">{content}</div></div>'

chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# ── Quick chips ───────────────────────────────────────────────────────────────
CHIPS = [
    "Recommend a perfume for him 🌿",
    "Best floral for her 🌸",
    "Show me unisex options",
    "What's in the sample set?",
    "Body splashes under 300 EGP",
]
if not st.session_state.messages:
    chips_html = '<div class="snj-chips">' + "".join(
        f'<span class="snj-chip">{c}</span>' for c in CHIPS
    ) + "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<hr class="snj-divider">', unsafe_allow_html=True)
st.markdown('<div class="snj-input-area">', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        label="",
        placeholder="Ask about a fragrance, or describe your mood…",
        key="chat_input",
        label_visibility="collapsed",
    )
with col2:
    send = st.button("Send →", key="send_btn")

st.markdown("</div>", unsafe_allow_html=True)

# ── Send & reply ──────────────────────────────────────────────────────────────
if (send or user_input) and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner("✦  Finding your perfect scent…"):
        reply = call_gemini(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
