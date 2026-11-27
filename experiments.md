# Prompt experiments

This is my experiment log for Project 1, Milestone 2.

## How to run an experiment

1. Open `experiment.py`.
2. Paste your current system prompt into `PROMPT_A`.
3. Paste it again into `PROMPT_B`, then change ONE thing.
4. Put two or three test messages in `TEST_INPUTS`.
5. In the terminal, run: `python experiment.py`
6. Read the replies. Each prompt answers each message three times.
7. Fill in one experiment below.
8. If B was better, B becomes your new `PROMPT_A` for the next experiment.

When all three experiments are done:

1. Copy your winning prompt into `SYSTEM_PROMPT` in `streamlit_app.py`.
2. Commit your changes.
3. Click Sync. Commit alone does not update your live app.
4. Open your live URL and check that the assistant uses the new prompt.

Milestone 2 is done when this file has three experiments filled in and your winning prompt is live.

---

A note before the experiments: my app lets the visitor pick two languages. For these experiments I fixed them, so every run is comparable: the learner speaks English and is practicing Spanish.

## Experiment 1: instructions

**The one thing I changed:**

I added one line to the end of the prompt:

"Correct only the most important mistake in each message. Leave the others alone."

**Test messages I used:**

Both messages have three mistakes.

1. Yo soy 25 años y yo gusto la música y mi hermano es alta.
2. Ayer yo ir al mercado y compro muchos frutas.

**What happened across the runs:**

Prompt A corrected every mistake in all 6 replies, three corrections each time. 4 of the 6 replies also ran longer than three sentences, because each correction came with its own explanation.

Prompt B made exactly one correction in 5 of 6 replies. In 1 reply it made two.

One thing I did not expect: for message 1, Prompt B picked "soy 25 años" in 2 replies and "yo gusto" in 1. It does not always agree with itself about which mistake is the most important.

**Keep or revert, and why:**

Keep. This fixes Reply 1 in `surprising_replies.md`. A beginner who gets three corrections at once will not remember any of them. "Most important" is vague, and the model fills that gap differently on different runs, but one correction of any kind is better than three.

---

## Experiment 2: examples

**The one thing I changed:**

I added two examples to the end of the prompt, to show the shape of reply I want:

```
Example 1
Learner: Yo tener un perro.
Tavi: Tengo un perro. (Use "tengo" with "yo".) ¡Qué bien! ¿Cómo se llama tu perro?

Example 2
Learner: Me gusta los libros.
Tavi: Me gustan los libros. (Use "gustan" because "libros" is plural.) ¡A mí también! ¿Qué libro lees ahora?
```

**Test messages I used:**

Message 1 has a mistake. Messages 2 and 3 are correct Spanish.

1. Mi hermano es muy alta.
2. Me gusta cocinar con mi familia los domingos.
3. Hoy estoy cansado porque trabajé mucho.

**What happened across the runs:**

9 replies for each prompt.

On message 1, Prompt B copied the shape well: the corrected sentence first, a short reason in parentheses, then a question. 3 of 3 replies. Prompt A did this in 1 of 3.

On messages 2 and 3, which have no mistakes, Prompt B invented a correction in 4 of 6 replies. For example, it changed "los domingos" to "en los domingos", which is wrong. Prompt A invented a correction in 1 of 6.

**Keep or revert, and why:**

Revert. Both of my examples show a learner making a mistake. So the pattern the model saw was "every message gets a correction", and it copied that together with the shape. Inventing mistakes is the worst thing a tutor can do, because the learner cannot tell.

Next time I would try three examples, with one where the learner makes no mistake. I still wanted the fixed shape, so I tried to get it a different way in Experiment 3.

---

## Experiment 3: output constraints

**The one thing I changed:**

I added one line to the end of the prompt:

'When you correct a mistake, put it on its own first line that starts with "Correction:". If there is no mistake, do not write that line.'

**Test messages I used:**

Message 1 has a mistake. Message 2 is correct Spanish.

1. ¿Dónde es el baño?
2. Quiero practicar español para mi viaje a México.

**What happened across the runs:**

On message 1, Prompt A put the correction in a different place each time: at the start in 1 reply and in the middle of the reply in 2. Prompt B started with a "Correction:" line in 3 of 3 replies.

On message 2, Prompt A made no correction in 3 of 3 replies. Prompt B left the line out in 2 of 3 replies. In 1 reply it wrote "Correction: none".

**Keep or revert, and why:**

Keep. The correction is now easy to find, for the learner and for me when I score replies. "Correction: none" is a small problem. I will watch for it.

---

## My winning system prompt

This is my first prompt plus the two changes I kept (Experiments 1 and 3). In the app, `{native_language}` and `{practice_language}` are replaced with the two languages the visitor picks.

```
You are Tavi, a patient language practice partner.
The learner speaks {native_language} and is practicing {practice_language}.
Your one job is to help them practice through short, friendly conversation.
Reply in simple {practice_language}: two or three short sentences, then one question to keep the conversation going.
If the learner makes a mistake, correct it kindly and explain it in {native_language}.
Correct only the most important mistake in each message. Leave the others alone.
When you correct a mistake, put it on its own first line that starts with "Correction:". If there is no mistake, do not write that line.
```
