# Results

How Tavi scores on my test set, measured with `rubric.md`.

## The test set

`test_set.json` has 18 cases. Each case has the learner's message, its kind, what a good reply must do, what failure it guards against, and an answer key for scoring.

| Kind | Tuning half | Held-out half |
| --- | --- | --- |
| Typical use | 4 | 4 |
| Edge cases | 3 | 2 |
| Known failures | 2 | 3 |
| Total | 9 | 9 |

Where the cases came from: messages friends typed into the app, my surprising replies, the failure modes from Session 2, one case for each rubric criterion, and three cases my partner wrote to break Tavi (cases 6, 17, and 18).

I use the tuning half when I decide what to change. I only use the held-out half to report a number. I have not changed the prompt since I wrote the held-out cases.

## Baseline

I ran the held-out half and scored each reply by hand. The replies and my scores are in `results/baseline_held_out.json`.

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
