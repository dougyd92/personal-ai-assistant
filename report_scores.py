"""Add up the scores in a results file and print the pass rate.

Run it from the terminal:
    python report_scores.py results/baseline_held_out.json

A reply passes when it passes every criterion in rubric.md.
"""

import json
import sys

if len(sys.argv) != 2:
    sys.exit("Use it like this: python report_scores.py results/baseline_held_out.json")

with open(sys.argv[1], encoding="utf-8") as file:
    results = json.load(file)

# Stop if any score is still empty.
for result in results:
    for criterion, score in result["scores"].items():
        if score is None:
            sys.exit(f"Case {result['id']} has no score yet for {criterion}.")

total = len(results)
print(f"{sys.argv[1]}: {total} replies\n")

# How many replies pass each criterion?
for criterion in results[0]["scores"]:
    passed = len([r for r in results if r["scores"][criterion]])
    print(f"  {criterion}: {passed} of {total}")

# How many replies pass every criterion?
passing = [r for r in results if all(r["scores"].values())]
failing = [r for r in results if not all(r["scores"].values())]

percent = round(100 * len(passing) / total)
print(f"\nPass rate: {len(passing)} of {total} replies pass every criterion ({percent}%)")
print("Failed cases:", ", ".join(str(r["id"]) for r in failing) or "none")

# Runs made since Milestone 5 also record how many tokens each case used.
if "input_tokens" in results[0]:
    print("\nTokens used by each case:")
    for result in results:
        tokens = result["input_tokens"] + result["output_tokens"]
        print(f"  case {result['id']}: {tokens:,} ({result['input_tokens']:,} in, {result['output_tokens']:,} out)")
