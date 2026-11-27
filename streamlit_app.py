"""Tavi, a language practice partner.

Run it from the terminal:
    streamlit run streamlit_app.py
"""

import os

import openai
import streamlit as st
from dotenv import load_dotenv

# ---------- Part 1: the personality ----------
TITLE = "Tavi, your language practice partner"

# The words in {curly braces} are filled in with the visitor's two languages.
SYSTEM_PROMPT = """You are Tavi, a patient language practice partner.
The learner speaks {native_language} and is practicing {practice_language}.
Your one job is to help them practice through short, friendly conversation.
Reply in simple {practice_language}: two or three short sentences, then one question to keep the conversation going.
If the learner makes a mistake, correct it kindly and explain it in {native_language}.
Correct only the most important mistake in each message. Leave the others alone.
When you correct a mistake, put it on its own first line that starts with "Correction:". If there is no mistake, do not write that line."""

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

# ---------- Settings ----------
MODEL = "google/gemma-4-26b-a4b-it:floor"
MAX_REPLY_TOKENS = 300  # the longest reply allowed, in tokens
MAX_MESSAGES = 20  # the most messages one visitor can send in a chat

# On your Codespace, the key comes from .env. Once deployed, it comes
# from the app's secrets. Either way, it never appears in this file.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

st.title(TITLE)

# ---------- Part 2: the visitor's two languages ----------
native_language = st.sidebar.selectbox("I speak", LANGUAGES, index=0)
practice_language = st.sidebar.selectbox("I want to practice", LANGUAGES, index=1)

if native_language == practice_language:
    st.info("Pick two different languages in the sidebar to start.")
    st.stop()

system_prompt = SYSTEM_PROMPT.format(
    native_language=native_language,
    practice_language=practice_language,
)

# ---------- Part 3: this chat's history ----------
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

# ---------- Part 4: the call ----------
user_text = st.chat_input(f"Write something in {practice_language}")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.chat_message("user").write(user_text)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            # The personality goes first, then the conversation so far
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
            max_tokens=MAX_REPLY_TOKENS,
        )
    except openai.APIError as error:
        st.session_state.messages.pop()  # forget the message that didn't get a reply
        st.error(f"Couldn't get a reply from the model: {error}")
        st.stop()

    reply = response.choices[0].message.content or "(The model sent back an empty reply.)"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
