"""Tavi's personality and the call to the model.

The app (streamlit_app.py) and the test runner (run_tests.py) both use
this file. That way the Tavi I test is the same Tavi that is live.
"""

import os

import openai
from dotenv import load_dotenv

# ---------- The personality ----------
# The words in {curly braces} are filled in with the learner's two languages.
SYSTEM_PROMPT = """You are Tavi, a patient language practice partner.
The learner speaks {native_language} and is practicing {practice_language}.
Your one job is to help them practice through short, friendly conversation.
Reply in simple {practice_language}: two or three short sentences, then one question to keep the conversation going.
If the learner makes a mistake, correct it kindly and explain it in {native_language}.
Correct only the most important mistake in each message. Leave the others alone.
When you correct a mistake, put it on its own first line that starts with "Correction:". If there is no mistake, do not write that line."""

# ---------- Settings ----------
MODEL = "google/gemma-4-26b-a4b-it:floor"
MAX_REPLY_TOKENS = 300  # the longest reply allowed, in tokens

# On your Codespace, the key comes from .env. Once deployed, it comes
# from the app's secrets. Either way, it never appears in this file.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


def build_system_prompt(native_language, practice_language):
    """Fill the learner's two languages into the system prompt."""
    return SYSTEM_PROMPT.format(
        native_language=native_language,
        practice_language=practice_language,
    )


def get_reply(system_prompt, messages):
    """Send the conversation to the model and return Tavi's reply."""
    response = client.chat.completions.create(
        model=MODEL,
        # The personality goes first, then the conversation so far
        messages=[{"role": "system", "content": system_prompt}] + messages,
        max_tokens=MAX_REPLY_TOKENS,
    )
    return response.choices[0].message.content or "(The model sent back an empty reply.)"
