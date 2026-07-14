import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHAT_FOLDER="chats"
os.makedirs(CHAT_FOLDER, exist_ok=True)


def save_chat(chat_name, messages):
    filepath = os.path.join(CHAT_FOLDER, chat_name)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)

def load_chat(chat_name):
    filepath = os.path.join(CHAT_FOLDER, chat_name)

    if not os.path.exists(filepath):
        return [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

    

st.sidebar.title("Chat History")
chat_files = sorted(
    [f for f in os.listdir(CHAT_FOLDER) if f.endswith(".json")],
    reverse=True
)


if st.sidebar.button("New Chat"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_name = f"chat_{timestamp}.json"

    st.session_state.chat_name = chat_name
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    save_chat(chat_name, st.session_state.messages)

    st.rerun()


selected_chat = st.sidebar.selectbox("Previous Chats",[""] + chat_files)

if selected_chat:
    if("chat_name" not in st.session_state or st.session_state.chat_name != selected_chat):
        st.session_state.chat_name = selected_chat
        st.session_state.messages = load_chat(selected_chat)

if "messages" not in st.session_state:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_name = f"chat_{timestamp}.json"
    st.session_state.chat_name = chat_name
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    save_chat(chat_name, st.session_state.messages)


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
            input=st.session_state.messages
        )
        answer = response.output_text
        st.chat_message("assistant").markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_chat(st.session_state.chat_name, st.session_state.messages)




#homeowork
# in the side bar there should be proper log instead of dropdown and we can pins the chat
