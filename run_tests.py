"""Run test cases through Tavi and save the replies, ready to score.

Run it from the terminal:
    python run_tests.py held_out baseline

The first word says which cases to run: tuning, held_out, or the number
of one case (for example 19).
The second word is a name for this run. You choose it.

The replies are saved in the results folder. Open the file and score
each reply by hand with rubric.md: change each null to true (pass) or
false (fail). Then run report_scores.py on the file.
"""

import json
import logging
import os
import sys
import time

import assistant

# The test set is written for one pair of languages.
NATIVE_LANGUAGE = "English"
PRACTICE_LANGUAGE = "Spanish"

# One score for each criterion in rubric.md, in the same order.
CRITERIA = [
    "one_correction_at_most",
    "reason_in_learners_language",
    "keeps_practice_going",
    "correction_is_right",
    "remembers_the_conversation",
]

logging.basicConfig(level=logging.INFO)

if len(sys.argv) != 3:
    sys.exit("Use it like this: python run_tests.py held_out baseline")

which_cases = sys.argv[1]
run_name = sys.argv[2]

with open("test_set.json", encoding="utf-8") as file:
    test_set = json.load(file)

if which_cases in ["tuning", "held_out"]:
    cases = [case for case in test_set if case["half"] == which_cases]
    output_path = os.path.join("results", f"{run_name}_{which_cases}.json")
else:
    cases = [case for case in test_set if str(case["id"]) == which_cases]
    output_path = os.path.join("results", f"{run_name}_case_{which_cases}.json")

if not cases:
    sys.exit(f"No cases found for '{which_cases}'. Use tuning, held_out, or a case number.")

if os.path.exists(output_path):
    # Running again would replace the scores you filled in by hand.
    sys.exit(f"{output_path} already exists. Pick a new run name.")

system_prompt = assistant.build_system_prompt(NATIVE_LANGUAGE, PRACTICE_LANGUAGE)

results = []
for case in cases:
    # Most cases have one message. A multi-turn case has a list of them.
    if "turns" in case:
        learner_messages = case["turns"]
    else:
        learner_messages = [case["input"]]

    print(f"Running case {case['id']} ({len(learner_messages)} message(s))")

    # Play the learner's messages in order, the way the app would.
    conversation = []
    input_tokens = 0
    output_tokens = 0
    for learner_message in learner_messages:
        conversation.append({"role": "user", "content": learner_message})
        reply, usage = assistant.get_reply(system_prompt, conversation)
        conversation.append({"role": "assistant", "content": reply})
        input_tokens += usage["input_tokens"]
        output_tokens += usage["output_tokens"]
        time.sleep(1)  # a short pause so we don't send requests too fast

    result = {"id": case["id"], "kind": case["kind"]}
    if "turns" in case:
        result["turns"] = case["turns"]
    else:
        result["input"] = case["input"]
    result["answer_key"] = case["answer_key"]
    result["must_do"] = case["must_do"]
    # For a multi-turn case, this is the reply to the last message.
    result["reply"] = reply
    result["input_tokens"] = input_tokens
    result["output_tokens"] = output_tokens
    # Fill these in by hand: true for pass, false for fail.
    result["scores"] = {criterion: None for criterion in CRITERIA}
    result["note"] = ""
    results.append(result)

os.makedirs("results", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2, ensure_ascii=False)

print(f"\nSaved {len(results)} replies in {output_path}.")
print("Now score them by hand with rubric.md, then run:")
print(f"    python report_scores.py {output_path}")
