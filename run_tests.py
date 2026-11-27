"""Run test cases through Tavi and save the replies, ready to score.

Run it from the terminal:
    python run_tests.py held_out baseline

The first word says which half of the test set to run: tuning or held_out.
The second word is a name for this run. You choose it.

The replies are saved in results/<name>_<half>.json. Open that file and
score each reply by hand with rubric.md: change each null to true (pass)
or false (fail). Then run report_scores.py on the file.
"""

import json
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
]

if len(sys.argv) != 3 or sys.argv[1] not in ["tuning", "held_out"]:
    sys.exit("Use it like this: python run_tests.py held_out baseline")

half = sys.argv[1]
run_name = sys.argv[2]

output_path = os.path.join("results", f"{run_name}_{half}.json")
if os.path.exists(output_path):
    # Running again would replace the scores you filled in by hand.
    sys.exit(f"{output_path} already exists. Pick a new run name.")

with open("test_set.json", encoding="utf-8") as file:
    test_set = json.load(file)

system_prompt = assistant.build_system_prompt(NATIVE_LANGUAGE, PRACTICE_LANGUAGE)

results = []
for case in test_set:
    if case["half"] != half:
        continue

    print(f"Running case {case['id']}: {case['input']}")
    reply = assistant.get_reply(
        system_prompt,
        [{"role": "user", "content": case["input"]}],
    )
    time.sleep(1)  # a short pause so we don't send requests too fast

    results.append(
        {
            "id": case["id"],
            "kind": case["kind"],
            "input": case["input"],
            "answer_key": case["answer_key"],
            "must_do": case["must_do"],
            "reply": reply,
            # Fill these in by hand: true for pass, false for fail.
            "scores": {criterion: None for criterion in CRITERIA},
            "note": "",
        }
    )

os.makedirs("results", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2, ensure_ascii=False)

print(f"\nSaved {len(results)} replies in {output_path}.")
print("Now score them by hand with rubric.md, then run:")
print(f"    python report_scores.py {output_path}")
