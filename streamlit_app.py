"""Tavi, a language practice partner.

Run it from the terminal:
    streamlit run streamlit_app.py

Tavi's system prompt and the call to the model are in assistant.py.
"""

import logging

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

logging.basicConfig(level=logging.INFO)

st.title(TITLE)

# ---------- Part 1: the visitor's two languages ----------
native_language = st.sidebar.selectbox("I speak", LANGUAGES, index=0)
practice_language = st.sidebar.selectbox("I want to practice", LANGUAGES, index=1)

if native_language == practice_language:
    st.info("Pick two different languages in the sidebar to start.")
    st.stop()

system_prompt = assistant.build_system_prompt(native_language, practice_language)

# ---------- Part 2: this chat's history and its cost ----------
# The model remembers nothing between calls, so the app keeps the
# conversation here. assistant.py sends only the most recent turns.
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.input_tokens = 0
    st.session_state.output_tokens = 0

cost_box = st.sidebar.empty()


def show_cost():
    """Show what this chat has used so far, in the sidebar."""
    dollars = assistant.estimate_cost(
        st.session_state.input_tokens,
        st.session_state.output_tokens,
    )
    cost_box.caption(
        f"This chat so far: {st.session_state.input_tokens:,} tokens in, "
        f"{st.session_state.output_tokens:,} tokens out. "
        f"About ${dollars:.5f}."
    )


show_cost()

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
        reply, usage = assistant.get_reply(system_prompt, st.session_state.messages)
    except assistant.TaviUnavailable:
        # The model was busy and the retries ran out.
        st.session_state.messages.pop()  # forget the message that didn't get a reply
        st.warning("Tavi is taking a short break. Please send your message again in a minute.")
        st.stop()
    except openai.APIError as error:
        # Something a retry can't fix, like a wrong key. The visitor gets a
        # friendly message, and the real error goes to the log for me.
        logging.getLogger("tavi").error("The call failed: %s", error)
        st.session_state.messages.pop()
        st.warning("Tavi isn't working right now. The problem is on our side, not yours.")
        st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

    st.session_state.input_tokens += usage["input_tokens"]
    st.session_state.output_tokens += usage["output_tokens"]
    show_cost()
