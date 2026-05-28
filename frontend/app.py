import streamlit as st
import requests
import os

# Fetch backend URL from Streamlit secrets (Cloud) or Environment (Local)
try:
    BASE_API_URL = st.secrets["API_URL"]
except Exception:
    BASE_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Clean the URL just in case there are accidental spaces or line breaks
BASE_API_URL = BASE_API_URL.strip().strip("/")

API_URL = f"{BASE_API_URL}/api/chat"
ESCALATE_URL = f"{BASE_API_URL}/api/escalate"

st.set_page_config(
    page_title="WebCraft Digital — AI Support",
    page_icon="💎",
    layout="centered"
)

# Custom CSS for purple branding
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #6D55E9 0%, #9b8af2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .main-header p {
        color: #888;
        font-size: 1rem;
    }

    /* Chat input accent */
    .stChatInput > div {
        border-color: #6D55E9 !important;
    }

    /* Badge styling */
    .intent-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6D55E9, #9b8af2);
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Escalation badge */
    .escalation-badge {
        display: inline-block;
        background: linear-gradient(135deg, #e94e4e, #f08a5d);
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1432 0%, #0e0b1a 100%);
    }
    [data-testid="stSidebar"] * {
        color: #d4ccf5 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 💎 WebCraft Digital")
    st.markdown("*AI-Powered Support Assistant*")
    st.divider()
    st.markdown("**Try asking about:**")
    st.markdown("🎨 Web Design & UI/UX")
    st.markdown("💻 Custom Development")
    st.markdown("📈 SEO & Digital Marketing")
    st.markdown("🛒 Shopify / eCommerce")
    st.markdown("💰 Pricing & Plans")
    st.markdown("📋 Project Process")
    st.divider()
    st.markdown("**Powered by**")
    st.markdown("🧠 LangChain + Groq (Llama 3.3)")
    st.markdown("🔍 FAISS Vector Database")
    st.markdown("📚 RAG Pipeline")
    st.markdown("📧 Human Escalation via Email")

# Main header
st.markdown("""
<div class="main-header">
    <h1>💎 WebCraft Digital</h1>
    <p>AI Customer Support Assistant — Ask me anything about our services, pricing, or project process!</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_escalation_form" not in st.session_state:
    st.session_state.show_escalation_form = False
if "escalation_sent" not in st.session_state:
    st.session_state.escalation_sent = False

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "intent" in message:
            is_escalation = "escalation" in message["intent"].lower()
            badge_class = "escalation-badge" if is_escalation else "intent-badge"
            icon = "🚨" if is_escalation else "🏷️"
            st.markdown(
                f'<span class="{badge_class}">{icon} {message["intent"]}</span>',
                unsafe_allow_html=True
            )

# --- Escalation Form ---
if st.session_state.show_escalation_form and not st.session_state.escalation_sent:
    st.divider()
    st.markdown("### 📧 Connect with a Human Agent")
    st.markdown("Please provide your email and our team will get back to you with a personalized solution.")

    with st.form("escalation_form", clear_on_submit=True):
        user_email = st.text_input("Your email address", placeholder="you@example.com")
        submitted = st.form_submit_button("📨 Send to Support Team", type="primary")

        if submitted and user_email:
            with st.spinner("Summarizing conversation and sending email..."):
                try:
                    resp = requests.post(ESCALATE_URL, json={
                        "user_email": user_email,
                        "messages": st.session_state.messages
                    })
                    resp.raise_for_status()
                    data = resp.json()

                    st.session_state.escalation_sent = True
                    st.session_state.show_escalation_form = False

                    # Add confirmation to chat
                    confirmation = (
                        f"✅ **Your request has been escalated!**\n\n"
                        f"We've sent a detailed summary of our conversation to our support team. "
                        f"A human agent will reach out to you at **{user_email}** shortly.\n\n"
                        f"Thank you for your patience! 💎"
                    )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": confirmation
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to send escalation: {e}")
        elif submitted and not user_email:
            st.warning("Please enter your email address.")

# Chat input
if prompt := st.chat_input("e.g. How much does a custom website cost?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Reset escalation state on new message so the form disappears
    st.session_state.escalation_sent = False
    st.session_state.show_escalation_form = False

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            with st.spinner("Classifying intent & searching knowledge base..."):
                response = requests.post(API_URL, json={"query": prompt})
                response.raise_for_status()
                data = response.json()

                bot_reply = data["response"]
                intent = data["intent"]

                # Check if escalation is needed
                is_escalation = "escalation" in intent.lower()

                if is_escalation:
                    bot_reply = (
                        "I understand you'd like to speak with a human agent. "
                        "I'm sorry I wasn't able to fully resolve your concern.\n\n"
                        "Please share your email address below and our support team "
                        "will get back to you with a personalized solution. 👇"
                    )
                    st.session_state.show_escalation_form = True

                message_placeholder.markdown(bot_reply)

                badge_class = "escalation-badge" if is_escalation else "intent-badge"
                icon = "🚨" if is_escalation else "🏷️"
                st.markdown(
                    f'<span class="{badge_class}">{icon} {intent}</span>',
                    unsafe_allow_html=True
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_reply,
                    "intent": intent
                })

                if is_escalation:
                    st.rerun()

        except requests.exceptions.ConnectionError:
            st.error("❌ Backend not running. Start it with: `uvicorn backend.main:app --reload`")
        except Exception as e:
            st.error(f"❌ Error: {e}")
