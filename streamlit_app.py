"""Your personal AI assistant.

Run it from the terminal:
    streamlit run app.py
"""

import os
import sqlite3

import openai
import streamlit as st
from dotenv import load_dotenv

# ---------- Part 1: the personality ----------
# Change these to make the assistant your own.
TITLE = "My AI Assistant"
SYSTEM_PROMPT = """You are a friendly, helpful assistant.
Keep your answers short: two or three sentences."""

# ---------- Settings ----------
MODEL = "google/gemma-4-26b-a4b-it:floor"
MAX_REPLY_TOKENS = 300  # the longest reply allowed, in tokens
MAX_MESSAGES = 20  # the most messages one visitor can send in a chat
CHAT_DB = os.path.join(os.path.dirname(__file__), "chat_history.db")

# On your Codespace, the key comes from .env. Once deployed, it comes
# from the app's secrets. Either way, it never appears in this file.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

def load_messages():
    """Load the saved conversation from the local SQLite database."""
    with sqlite3.connect(CHAT_DB) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """
        )
        rows = connection.execute(
            "SELECT role, content FROM messages ORDER BY id"
        ).fetchall()
    return [{"role": role, "content": content} for role, content in rows]


def save_message(role, content):
    """Append one message to the persistent conversation."""
    with sqlite3.connect(CHAT_DB) as connection:
        connection.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content),
        )


def clear_messages():
    """Delete the saved conversation."""
    with sqlite3.connect(CHAT_DB) as connection:
        connection.execute("DELETE FROM messages")


st.title(TITLE)

# ---------- Part 2: persistent chat history ----------
# Conversation messages are stored in SQLite, so they survive browser
# refreshes and Streamlit reruns (and app restarts if the disk persists).
if st.button("Clear chat"):
    clear_messages()
    st.rerun()

messages = load_messages()

for message in messages:
    st.chat_message(message["role"]).write(message["content"])

messages_sent = sum(1 for message in messages if message["role"] == "user")
if messages_sent >= MAX_MESSAGES:
    st.info("You've reached the message limit for this chat. Thanks for trying it out!")
    st.stop()

# ---------- Part 3: the call ----------
user_text = st.chat_input("Say something")
if user_text:
    save_message("user", user_text)
    messages.append({"role": "user", "content": user_text})
    st.chat_message("user").write(user_text)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            # The personality goes first, then the conversation so far
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=MAX_REPLY_TOKENS,
        )
    except openai.APIError as error:
        # Keep the user message in history so they can retry or refer to it.
        st.error(f"Couldn't get a reply from the model: {error}")
        st.stop()

    reply = response.choices[0].message.content or "(The model sent back an empty reply.)"
    save_message("assistant", reply)
    st.chat_message("assistant").write(reply)