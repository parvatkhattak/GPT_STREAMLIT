# 💬 GPT Streamlit Chat

A lightweight ChatGPT-style app built on the OpenAI API (`gpt-4o-mini`). It comes in two versions: a **terminal chat** and a **Streamlit web app** with saved and pinned conversations.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

## ✨ Features

- 🧠 Multi-turn conversations with full message history
- ➕ Start new chats from the sidebar
- 💾 Chats saved automatically as JSON (`GPT_Streamlit/chats/`)
- 📌 Pin and unpin important conversations
- 🖥️ Minimal terminal version (`1.py`): type `exit` to quit

## 📁 Structure

```
├── 1.py                     # Terminal chat
└── GPT_Streamlit/
    ├── app.py               # Streamlit chat app
    ├── requirements.txt
    └── chats/               # Saved conversations + _pins.json
```

## 🚀 Getting Started

```sh
git clone https://github.com/parvatkhattak/GPT_STREAMLIT.git
cd GPT_STREAMLIT/GPT_Streamlit
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env

streamlit run app.py      # web app
# or
python ../1.py            # terminal chat
```

---

Built by [Parvat Khattak](https://github.com/parvatkhattak)
