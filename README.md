# Tavi, a language practice partner

> **This is an example submission for Project 1** of the AI Engineer Bootcamp. It shows what a finished project can look like. Your own project should be a different assistant, with your own experiments and your own numbers.
>
> The code is real and it runs. The replies, scores, and token counts are **sample data, written by hand** to show what results look like. They were not measured on the live app.

Tavi is a chat assistant for practicing a new language. You pick the language you speak and the language you want to practice. Tavi chats with you in the practice language and explains your mistakes in your own language.

**Live app:** (link to be added once this example is deployed)

## The personality brief

- **Who it is:** Tavi, a patient language practice partner.
- **Its one job:** help a learner practice a new language through short conversations, and correct their mistakes kindly.
- **How it talks:** short, simple sentences in the practice language. Explanations in the learner's own language. Always ends with a question so the learner has something to answer.

The system prompt in `assistant.py` is written from this brief.

## How it scores

Start with the one-page write-up: [`WRITEUP.md`](WRITEUP.md).

| | Before | After |
| --- | --- | --- |
| Quality: pass rate on the held-out half of the test set | 5 of 10 | 6 of 10 |
| Cost: tokens for a ten-turn chat | 3,441 | 3,416 |
| Robustness: still answers when the API fails? | No | Yes |

The write-up explains why 5 to 6 is not a real improvement, and where Tavi still fails.

## What is in this repository

Each milestone is one commit. Open the commit history to see what was added at each step.

| Milestone | Files |
| --- | --- |
| 1. Deploy | `streamlit_app.py`, the personality brief above |
| 2. Prompt experiments | `experiments.md`, `surprising_replies.md`, `experiment.py` |
| 3. Rubric | `rubric.md`, `scored_replies.md` |
| 4. Test set | `test_set.json`, `run_tests.py`, `report_scores.py`, `results/baseline_held_out.json` |
| 5. Memory and hardening | `assistant.py`, `results.md`, the other files in `results/` |
| Write-up | `WRITEUP.md` |

## Which languages work

I tested one pair: an English speaker practicing Spanish. Every experiment, test case, and score in this repository is for that pair.

The app lets you pick other languages, and I have not tested them. The model was trained on text in many languages, but that does not mean it is a good tutor in all of them. Before trusting Tavi in another language, ask someone who speaks it well to check the corrections.

## Run it yourself

1. Open this repository in a Codespace.
2. Put your API key in a file named `.env`: `OPENROUTER_API_KEY=your-key-here`
3. In the terminal, run: `streamlit run streamlit_app.py`

To run the test set and see the scores:

```
python run_tests.py held_out my_run
python report_scores.py results/my_run_held_out.json
```

The first command saves Tavi's replies. Score them by hand with `rubric.md` before you run the second one.

## Where an AI assistant helped

This example was built with Claude, an AI coding assistant, directed by the course instructor. Claude drafted the code, the test set, and the sample data.

In your own README, say which parts an assistant helped with, and which parts you wrote and checked yourself.
