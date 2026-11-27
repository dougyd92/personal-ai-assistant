"""Prompt experiment: compare two system prompts on the same inputs.

Run it from the terminal:
    python experiment.py

How to use it:
    1. Paste your current system prompt into SYSTEM_PROMPT_A.
    2. Paste it again into SYSTEM_PROMPT_B, then change ONE thing.
    3. Run the file and read the replies.
    4. Write down what happened in experiments.md.
"""

import os
import time

import openai
from dotenv import load_dotenv

MODEL = "google/gemma-4-26b-a4b-it:floor"
MAX_REPLY_TOKENS = 300  # same limit as your app
RUNS = 3  # how many times to ask each question, because replies vary

# ---------- Part 1: the two system prompts ----------
# A is what you have now. B is A with ONE change.
SYSTEM_PROMPT_A = """You are Tavi, a patient language practice partner.
The learner speaks English and is practicing Spanish.
Your one job is to help them practice through short, friendly conversation.
Reply in simple Spanish: two or three short sentences, then one question to keep the conversation going.
If the learner makes a mistake, correct it kindly and explain it in English.
Correct only the most important mistake in each message. Leave the others alone."""

SYSTEM_PROMPT_B = """You are Tavi, a patient language practice partner.
The learner speaks English and is practicing Spanish.
Your one job is to help them practice through short, friendly conversation.
Reply in simple Spanish: two or three short sentences, then one question to keep the conversation going.
If the learner makes a mistake, correct it kindly and explain it in English.
Correct only the most important mistake in each message. Leave the others alone.
When you correct a mistake, put it on its own first line that starts with "Correction:". If there is no mistake, do not write that line."""

# ---------- Part 2: the test inputs ----------
# The messages a visitor might send. Both prompts get the same ones.
TEST_INPUTS = [
    "¿Dónde es el baño?",
    "Quiero practicar español para mi viaje a México.",
]

# Read your key from the .env file, the same way your app does.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


def get_reply(system_prompt, user_text):
    """Send one message to the model and return its reply."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            max_tokens=MAX_REPLY_TOKENS,
        )
    except openai.APIError as error:
        return f"(No reply. The model returned an error: {error})"
    time.sleep(1)  # a short pause so we don't send requests too fast
    return response.choices[0].message.content or "(The model sent back an empty reply.)"


# ---------- Part 3: run the experiment ----------
for user_text in TEST_INPUTS:
    print("=" * 70)
    print(f"INPUT: {user_text}")
    print("=" * 70)

    for name, system_prompt in [("SYSTEM PROMPT A", SYSTEM_PROMPT_A), ("SYSTEM PROMPT B", SYSTEM_PROMPT_B)]:
        print(f"\n--- {name} ---")
        for run in range(1, RUNS + 1):
            reply = get_reply(system_prompt, user_text)
            print(f"\n[{name} · run {run} of {RUNS}]")
            print(reply.strip())

    print()

print("Done. Now write down what happened in experiments.md.")
