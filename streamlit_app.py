"""Tavi, a language practice partner.

Run it from the terminal:
    streamlit run streamlit_app.py

Tavi's system prompt and the call to the model are in assistant.py.
"""

import openai
import streamlit as st

import assistant

TITLE = "Tavi, your language practice partner"
MAX_MESSAGES = 20  # the most messages one visitor can send in a chat

# The languages a visitor can pick. I have only tested English speakers
# practicing Spanish. The others are here so you can try them.
LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Portuguese",
    "Italian",
    "Japanese",
    "Korean",
    "Chinese",
    "Hindi",
    "Arabic",
]

st.title(TITLE)

# ---------- Part 1: the visitor's two languages ----------
native_language = st.sidebar.selectbox("I speak", LANGUAGES, index=0)
practice_language = st.sidebar.selectbox("I want to practice", LANGUAGES, index=1)

if native_language == practice_language:
    st.info("Pick two different languages in the sidebar to start.")
    st.stop()

system_prompt = assistant.build_system_prompt(native_language, practice_language)

# ---------- Part 2: this chat's history ----------
# The model remembers nothing between calls, so the app keeps the whole
# conversation here and sends all of it every time.
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

messages_sent = len([m for m in st.session_state.messages if m["role"] == "user"])
if messages_sent >= MAX_MESSAGES:
    st.info("You've reached the message limit for this chat. Thanks for practicing!")
    st.stop()

# ---------- Part 3: the call ----------
user_text = st.chat_input(f"Write something in {practice_language}")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.chat_message("user").write(user_text)

    try:
        reply = assistant.get_reply(system_prompt, st.session_state.messages)
    except openai.APIError as error:
        st.session_state.messages.pop()  # forget the message that didn't get a reply
        st.error(f"Couldn't get a reply from the model: {error}")
        st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
