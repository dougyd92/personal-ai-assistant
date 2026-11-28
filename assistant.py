"""Tavi's personality and the call to the model.

The app (streamlit_app.py) and the test runner (run_tests.py) both use
this file. That way the Tavi I test is the same Tavi that is live.
"""

import logging
import os
import time

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

# Memory: how many past turns Tavi gets to see. One turn is one learner
# message plus Tavi's reply to it. Older turns are not sent to the model.
MAX_HISTORY_TURNS = 8

# Retries: how many times to try the call before giving up.
MAX_TRIES = 3

# For testing only. Set this to 2 and every reply fails twice before it
# works. Set it to 3 and every reply fails. Keep it at 0 in the live app.
SIMULATE_FAILURES = 0

# Cost: US dollars for one million tokens. Prices change, and they depend
# on which provider answers, so check the model's page on OpenRouter.
PRICE_PER_MILLION_INPUT_TOKENS = 0.06
PRICE_PER_MILLION_OUTPUT_TOKENS = 0.33

logger = logging.getLogger("tavi")

# On your Codespace, the key comes from .env. Once deployed, it comes
# from the app's secrets. Either way, it never appears in this file.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


class SimulatedFailure(Exception):
    """A pretend rate limit, raised on purpose when SIMULATE_FAILURES is set."""


class TaviUnavailable(Exception):
    """Every try failed. The app shows a friendly message when it sees this."""


def build_system_prompt(native_language, practice_language):
    """Fill the learner's two languages into the system prompt."""
    return SYSTEM_PROMPT.format(
        native_language=native_language,
        practice_language=practice_language,
    )


def trim_history(messages):
    """Keep only the most recent turns of the conversation.

    The system prompt is not in this list. It is added later, in
    call_model, so trimming can never remove it.
    """
    # Two messages for each past turn, plus the learner's new message.
    messages_to_keep = MAX_HISTORY_TURNS * 2 + 1
    return messages[-messages_to_keep:]


def call_model(system_prompt, messages):
    """Call the model. If it is busy, wait and try again."""
    for attempt in range(1, MAX_TRIES + 1):
        try:
            if attempt <= SIMULATE_FAILURES:
                raise SimulatedFailure("pretend rate limit")
            return client.chat.completions.create(
                model=MODEL,
                # The personality goes first, then the conversation so far
                messages=[{"role": "system", "content": system_prompt}] + messages,
                max_tokens=MAX_REPLY_TOKENS,
            )
        # Only retry when waiting can help: a rate limit (429) or a server
        # error (5xx). A wrong key (401) will be just as wrong next time,
        # so that error is not caught here and fails at once.
        except (openai.RateLimitError, openai.InternalServerError, SimulatedFailure) as error:
            if attempt == MAX_TRIES:
                logger.error("Try %s of %s failed. Giving up. %s", attempt, MAX_TRIES, error)
                raise TaviUnavailable("The model did not answer.") from error
            wait_seconds = 2 ** (attempt - 1)  # 1 second, then 2
            logger.warning(
                "Try %s of %s failed. Waiting %s seconds. %s",
                attempt, MAX_TRIES, wait_seconds, error,
            )
            time.sleep(wait_seconds)


def get_reply(system_prompt, messages):
    """Send the conversation to the model.

    Returns two things: Tavi's reply, and how many tokens the call used.
    """
    response = call_model(system_prompt, trim_history(messages))
    reply = response.choices[0].message.content or "(The model sent back an empty reply.)"

    usage = {"input_tokens": 0, "output_tokens": 0}
    if response.usage:
        usage["input_tokens"] = response.usage.prompt_tokens
        usage["output_tokens"] = response.usage.completion_tokens

    if response.choices[0].finish_reason == "length":
        logger.warning("The model's reply was cut off because it was too long.")
        reply += "\n\n(Note: The model's reply was cut off because it was too long.)"

    return reply, usage


def estimate_cost(input_tokens, output_tokens):
    """Turn token counts into an estimated cost in US dollars."""
    input_cost = input_tokens / 1_000_000 * PRICE_PER_MILLION_INPUT_TOKENS
    output_cost = output_tokens / 1_000_000 * PRICE_PER_MILLION_OUTPUT_TOKENS
    return input_cost + output_cost
