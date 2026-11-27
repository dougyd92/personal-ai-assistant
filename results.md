# Results

How Tavi scores on my test set, measured with `rubric.md`.

## The test set

`test_set.json` has 20 cases. Each case has the learner's message, its kind, what a good reply must do, what failure it guards against, and an answer key for scoring.

| Kind | Tuning half | Held-out half |
| --- | --- | --- |
| Typical use | 5 | 4 |
| Edge cases | 3 | 2 |
| Known failures | 2 | 4 |
| Total | 10 | 10 |

Where the cases came from: messages friends typed into the app, my surprising replies, the failure modes from Session 2, one case for each rubric criterion, and three cases my partner wrote to break Tavi (cases 6, 17, and 18). Cases 19 and 20 are ten-turn chats that I added in Milestone 5.

I use the tuning half when I decide what to change. I only use the held-out half to report a number. I have not changed the prompt since I wrote the held-out cases.

## Baseline (Milestone 4)

I ran the held-out half and scored each reply by hand. The replies and my scores are in `results/baseline_held_out.json`. At this point the held-out half had 9 cases.

```
python run_tests.py held_out baseline
python report_scores.py results/baseline_held_out.json
```

**Baseline pass rate: 4 of 9 replies pass every criterion (44%).**

| Criterion | Replies that pass |
| --- | --- |
| 1. One correction at most | 8 of 9 |
| 2. Reason in the learner's language | 9 of 9 |
| 3. Keeps the practice going | 8 of 9 |
| 4. The correction is right | 6 of 9 |

The five cases that failed:

| Case | Kind | What went wrong |
| --- | --- | --- |
| 12 | Typical | It "corrected" a sentence that was already correct. |
| 14 | Edge | It fixed two of the three mistakes. The limit is one. |
| 16 | Known failure | It missed "embarazada" and congratulated the learner. |
| 17 | Known failure | It called Argentine Spanish a mistake. |
| 18 | Known failure | It switched to English when told to ignore its instructions. |

44% is lower than I expected. When I chat with Tavi it feels much better than that. But the test set has hard cases on purpose, and all three of the known failures failed. Tavi does well on the format (Criteria 1 to 3) and badly on the thing that matters most for a tutor, which is Criterion 4.

Case 12 worries me most. It is a typical message, not a trick, and Tavi still invented a mistake.

## Before and after (Milestone 5)

In Milestone 5 I changed three things in `assistant.py`: Tavi now sees only the most recent turns of the chat, a failed call is tried again, and every call's tokens are counted. Then I measured again.

Three kinds of number:

- **Quality:** the pass rate on the held-out half.
- **Cost:** the tokens used by one ten-turn chat (case 19, start to finish).
- **Robustness:** does the app still answer when the API fails?

| Version | Quality | Cost | Robustness |
| --- | --- | --- | --- |
| Before: full history, no retries | 5 of 10 (50%) | 3,441 tokens | No. One failed call shows a red error with the raw API message. |
| Tried: only the last 4 turns | Case 19 now fails | 2,983 tokens | Not tested |
| After: the last 8 turns, with retries | 6 of 10 (60%) | 3,416 tokens | Yes. With two failed tries it answers on the third, about 3 seconds later. |

At the prices in `assistant.py`, the ten-turn chat costs about $0.0003 before and after. That is three hundredths of a cent.

### How I got each number

**Before.** The baseline above has 9 cases. To compare fairly I also needed case 19 with full history, so I set `MAX_HISTORY_TURNS = 100` and ran it alone. It passed, which makes 5 of 10. That run also gave me the cost.

```
python run_tests.py 19 full_history
```

**Tried: 4 turns.** I set `MAX_HISTORY_TURNS = 4` and ran case 19 again. The chat got 13% cheaper. But the learner says their name in the second message and asks for it in the tenth, and by then the second message was no longer being sent. Tavi answered "Lo siento, todavía no sé tu nombre." Criterion 5 failed. I only ran case 19 here, because the other held-out cases have one message each, so there is no history to trim.

```
python run_tests.py 19 four_turns
```

**After: 8 turns.** I set `MAX_HISTORY_TURNS = 8`, ran the whole held-out half, and scored it. The scores are in `results/final_held_out.json`. Case 19 passes again.

```
python run_tests.py held_out final
python report_scores.py results/final_held_out.json
```

**Robustness.** I set `SIMULATE_FAILURES = 2` and sent a message in the app. The log showed two failed tries and the reply arrived on the third. Then I set it to 3. The app showed "Tavi is taking a short break. Please send your message again in a minute." and did not crash. I set it back to 0 afterwards.

### What I learned from the table

**Quality did not really change.** It went from 5 of 10 to 6 of 10, but the one case that changed is case 14 (three mistakes in one message). Last time Tavi fixed two of them. This time it fixed one. Nothing I changed in Milestone 5 can explain that: I did not touch the prompt, and case 14 is one message, so it has no history. Replies vary from run to run, and Experiment 1 already showed that Tavi follows the one-correction rule about 5 times in 6. With 10 cases, one lucky reply is 10 points. I would need more cases, or several runs of each case, to trust a change this small.

The four cases that still fail are 12, 16, 17, and 18. Three of them are Criterion 4.

**The history limit saves less than I expected.** With 8 turns, the ten-turn chat is less than 1% cheaper, because it only goes over the limit on its last turn. With 4 turns it is 13% cheaper, and Tavi forgets the learner's name. I chose 8. A tutor that forgets your name is worse than one that costs a few thousandths of a cent more. The limit will matter more in longer chats, up to the 20-message cap. I did not measure that.

**About half of the input tokens are the system prompt.** It is about 165 tokens, and it is sent again on every turn: 1,650 of the 3,215 input tokens in the ten-turn chat. A shorter prompt would save more than trimming the history does.

**Retries did not change the quality number, and they should not.** They are for the third column.
