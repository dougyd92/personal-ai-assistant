# Tavi: project write-up

## What it is for

Tavi is a practice partner for someone learning a new language. The learner writes a short message in the language they are practicing. Tavi corrects one mistake, explains it in the learner's own language, and asks a question to keep the conversation going.

I built and tested it for an English speaker practicing Spanish.

## How it scores

I score replies with a five-criterion rubric (`rubric.md`) on a test set of 20 cases (`test_set.json`). Half of the cases are held out: I never used them to tune the prompt. The numbers below are for that half.

| | Before Milestone 5 | After Milestone 5 |
| --- | --- | --- |
| **Quality:** replies that pass every criterion | 5 of 10 (50%) | 6 of 10 (60%) |
| **Cost:** tokens for a ten-turn chat | 3,441 | 3,416 |
| **Robustness:** still answers when the API fails? | No, it shows a raw error | Yes, it tries up to 3 times |

What changed between the two columns: Tavi now sees only the last 8 turns of the chat, failed calls are tried again, and the app counts tokens and shows the cost.

The quality number looks better, and I do not think it is. One case went from fail to pass, and nothing I changed can explain it. Replies vary from run to run, and with 10 cases one reply is 10 points. My honest summary is "about half, before and after". The details are in `results.md`.

A ten-turn chat costs about $0.0003.

## Where it still fails

Tavi is good at the shape of a reply and unreliable about the content of a correction. Three of the four failing cases are Criterion 4, "the correction is right".

- **It corrects sentences that are already correct** (case 12). This is the worst failure, because a learner cannot tell. It happened on an ordinary message.
- **It misses mistakes of meaning** (case 16). "Estoy embarazada" is good grammar, so Tavi congratulated the learner on the baby. It sees the words, not what the learner meant.
- **It treats regional Spanish as a mistake** (case 17). "Vos tenés" is correct in Argentina.
- **It stops doing its job when told to** (case 18). "Talk to me in English from now on" works.

One more limit that the test set cannot show: I only tested one pair of languages.

## What I would try next

1. **Fix the invented corrections.** Add three examples to the prompt, with one where the learner makes no mistake. Experiment 2 failed because both of my examples had a mistake in them.
2. **Run each case three times.** One run per case is too noisy to see a small change.
3. **Shorten the system prompt.** It is about half of the input tokens in a ten-turn chat, so it is where the cost is.
4. **Summarize old turns** so that Tavi can keep the learner's name without keeping the whole chat.
5. **Test a second language pair**, scored by someone who speaks that language well.
6. **Streaming,** so the reply appears word by word.
