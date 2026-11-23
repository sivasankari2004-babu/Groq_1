
import streamlit as st
import requests

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Tutor Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #273c75;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 17px;
}

.stButton button {
    background-color: #273c75;
    color: white;
    border-radius: 10px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("🤖 AI Tutor")
    st.write("Your personal AI learning assistant.")

    st.markdown("---")

    st.subheader("Features")
    st.write("📘 Simple explanations")
    st.write("💡 Practical examples")
    st.write("💻 Technical learning")
    st.write("📝 Step-by-step answers")

    st.markdown("---")

    st.info("Powered by your Groq AI backend.")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# MAIN PAGE
# ==========================================

st.markdown(
    '<div class="title">AI Tutor Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions and learn concepts with AI.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================

user_input = st.chat_input(
    "Ask your question here..."
)

# ==========================================
# SEND REQUEST TO BACKEND API
# ==========================================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:
                # Replace this URL with your deployed API URL.
                API_URL = "http://127.0.0.1:8000/chat"

                response = requests.post(
                    API_URL,
                    json={"message": user_input},
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()
                answer = data["response"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.RequestException:
                st.error(
                    "Could not connect to the backend API. "
                    "The frontend needs a running API endpoint."
                )

            except (KeyError, ValueError):
                st.error("The backend returned an invalid response.")
