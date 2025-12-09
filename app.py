import os
import json
import time
from datetime import datetime

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# =============================
# 🚀 APP SETUP
# =============================
st.set_page_config(
    page_title="🩺 AI Medical Assistant",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 AI Medical Assistant ")
st.caption("⚠️ General medical info only — not a substitute for a doctor or emergency services.")


# =============================
# 🧰 SIDEBAR — SETTINGS
# =============================
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get it from console.groq.com")

MODEL_OPTIONS = [
    "llama-3.1-8b-instant"
]
model_name = st.sidebar.selectbox("Groq Model", MODEL_OPTIONS, index=0)

temperature = st.sidebar.slider("Temperature (creativity)", 0.1,1.0,0.3,
                                help="Lower = factual, Higher = creative")
max_tokens = st.sidebar.slider("Max Tokens", 200,600,400)

# 🔥 Editable System Prompt
default_prompt = """You are a careful, friendly medical assistant.  
Rules:  
- Always answer in exactly 6 steps with numbering:  
  1) Summary 
  2) Common Causes  
  3) Safe Home Remedies  
  4) Prevention Tips  
  5) Medication Advice  
  6) Doctor Visit Advice  

- Adjust detail by max_tokens: <100 → 1-2 lines per step, 100–250 → 2–3 lines, >250-500 → 4–5 lines.  
- Only general health info (not a doctor).  
- Mix Roman Urdu + English.  
"""



custom_system_prompt = st.sidebar.text_area("System prompt (rules)", default_prompt, height=200)

col_a, col_b = st.sidebar.columns(2)
with col_a:
    clear_chat = st.button("🧹ClearChat")
with col_b:
    pass

# =============================
# 🧠 SESSION STATE
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Share your symptoms or question, and I’ll guide you step by step."}
    ]

if clear_chat:
    st.session_state.messages = [{"role": "assistant", "content": "Chat cleared. Fresh start!"}]


# =============================
# 🧩 PROMPT — SYSTEM GUARDRAILS
# =============================
SYSTEM_PROMPT = custom_system_prompt

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    HumanMessage(content="{input}"),
])

# =============================
# 🔗 LLM FACTORY
# =============================
def make_llm():
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar to start.")
        return None
    os.environ["GROQ_API_KEY"] = api_key
    try:
        llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return llm
    except Exception as e:
        st.error(f"LLM init error: {e}")
        return None

# =============================
# 💬 CHAT UI (history + input)
# =============================
# Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Describe your symptoms or ask a health question…")

# =============================
# 🧠 REPLY GENERATION
# =============================

def _lc_history_from_session():
    lc_msgs = []
    for m in st.session_state.messages:
        if m["role"] == "user":
            lc_msgs.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            lc_msgs.append(AIMessage(content=m["content"]))
    return lc_msgs

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    llm = make_llm()
    if llm is not None:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""
            try:
                chain = prompt | llm
                result = chain.invoke({
                    "history": _lc_history_from_session(),
                    "input": user_input,
                })
                full_reply = result.content if hasattr(result, "content") else str(result)

                
                placeholder.markdown(full_reply)
            except Exception as e:
                full_reply = f"Sorry, response error: {e}"
                placeholder.error(full_reply)

        st.session_state.messages.append({"role": "assistant", "content": full_reply})

# =============================
# 📥 DOWNLOAD CHAT
# =============================
chat_txt_lines = []
for m in st.session_state.messages:
    role = "User" if m["role"] == "user" else "Assistant"
    chat_txt_lines.append(f"[{role}] {m['content']}")
chat_txt = "\n\n".join(chat_txt_lines)

st.download_button(
    label="⬇️ Download Chat",
    data=chat_txt,
    file_name=f"medical_assistant_chat_{int(time.time())}.txt",
    mime="text/plain",
)


st.sidebar.markdown("---")  
st.sidebar.markdown("👩‍💻 **Developed by Bushra**")




