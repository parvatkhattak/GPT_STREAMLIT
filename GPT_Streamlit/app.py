import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHAT_FOLDER = "chats"
PINS_FILE = os.path.join(CHAT_FOLDER, "_pins.json")
os.makedirs(CHAT_FOLDER, exist_ok=True)


def save_chat(chat_name, messages):
    filepath = os.path.join(CHAT_FOLDER, chat_name)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)


def load_chat(chat_name):
    filepath = os.path.join(CHAT_FOLDER, chat_name)
    if not os.path.exists(filepath):
        return [{"role": "system", "content": "You are a helpful assistant."}]
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_pins():
    if not os.path.exists(PINS_FILE):
        return []
    with open(PINS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_pins(pins):
    with open(PINS_FILE, "w", encoding="utf-8") as f:
        json.dump(pins, f, indent=4)


def toggle_pin(chat_name):
    pins = load_pins()
    if chat_name in pins:
        pins.remove(chat_name)
    else:
        pins.append(chat_name)
    save_pins(pins)


def new_chat():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_name = f"chat_{timestamp}.json"
    st.session_state.chat_name = chat_name
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    save_chat(chat_name, st.session_state.messages)


def chat_preview(chat_name):
    messages = load_chat(chat_name)
    for m in messages:
        if m["role"] == "user":
            text = m["content"].strip().replace("\n", " ")
            return text[:28] + ("..." if len(text) > 28 else "")
    return chat_name.replace(".json", "")


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.divider()

    chat_files = sorted(
        [f for f in os.listdir(CHAT_FOLDER) if f.endswith(".json") and f != "_pins.json"],
        reverse=True,
    )
    pins = load_pins()
    pinned_chats = [c for c in chat_files if c in pins]
    other_chats = [c for c in chat_files if c not in pins]

    # Floating scrollable chat window
    with st.container(height=450, border=True):
        if pinned_chats:
            st.caption("📌 PINNED")
            for chat in pinned_chats:
                col1, col2 = st.columns([5, 1])
                active = st.session_state.get("chat_name") == chat
                label = ("👉 " if active else "") + chat_preview(chat)
                with col1:
                    if st.button(label, key=f"select_{chat}", use_container_width=True):
                        st.session_state.chat_name = chat
                        st.session_state.messages = load_chat(chat)
                        st.rerun()
                with col2:
                    if st.button("📌", key=f"pin_{chat}", help="Unpin chat"):
                        toggle_pin(chat)
                        st.rerun()
            st.divider()

        if other_chats:
            st.caption("RECENT")
            for chat in other_chats:
                col1, col2 = st.columns([5, 1])
                active = st.session_state.get("chat_name") == chat
                label = ("👉 " if active else "") + chat_preview(chat)
                with col1:
                    if st.button(label, key=f"select_{chat}", use_container_width=True):
                        st.session_state.chat_name = chat
                        st.session_state.messages = load_chat(chat)
                        st.rerun()
                with col2:
                    if st.button("📍", key=f"pin_{chat}", help="Pin chat"):
                        toggle_pin(chat)
                        st.rerun()

        if not chat_files:
            st.info("No chats yet. Start a new one!")

# ---------------- INIT SESSION ----------------
if "messages" not in st.session_state:
    if pins and pins[0] in chat_files:
        st.session_state.chat_name = pins[0]
        st.session_state.messages = load_chat(pins[0])
    elif chat_files:
        st.session_state.chat_name = chat_files[0]
        st.session_state.messages = load_chat(chat_files[0])
    else:
        new_chat()

# ---------------- MAIN CHAT AREA ----------------
st.title("OpenAI Chatbot")

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask Something...")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Generating response..."):
        response = client.responses.create(
            model="gpt-4o-mini",
            input=st.session_state.messages,
        )
        answer = response.output_text

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_chat(st.session_state.chat_name, st.session_state.messages)