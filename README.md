# Tavi, a language practice partner

My Project 1 for the AI Engineer Bootcamp.

Tavi is a chat assistant for practicing a new language. You pick the language you speak and the language you want to practice. Tavi chats with you in the practice language and explains your mistakes in your own language.

**Live app:** (link to be added once this example is deployed)

## The personality brief

- **Who it is:** Tavi, a patient language practice partner.
- **Its one job:** help a learner practice a new language through short conversations, and correct their mistakes kindly.
- **How it talks:** short, simple sentences in the practice language. Explanations in the learner's own language. Always ends with a question so the learner has something to answer.

The system prompt in `streamlit_app.py` is written from this brief.

## Milestones

- [x] 1. Deploy: the app is live and answers in Tavi's personality
- [x] 2. Prompt experiments: see `experiments.md` and `surprising_replies.md`
- [x] 3. Rubric: see `rubric.md` and `scored_replies.md`
- [ ] 4. Test set
- [ ] 5. Memory and hardening

## Run it yourself

1. Open this repository in a Codespace.
2. Put your API key in a file named `.env`: `OPENROUTER_API_KEY=your-key-here`
3. In the terminal, run: `streamlit run streamlit_app.py`
