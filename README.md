# RAG Evaluation Suite

An automated test suite that measures how well the [Notes RAG Chatbot](https://github.com/Iaimal/rag-notes-chatbot) retrieves and answers questions — instead of manually typing questions and eyeballing the results.

## What it does

Sends 16 predefined questions to the RAG API, compares the sources it retrieves against the sources it *should* retrieve, and reports a pass/fail score. The test set is split into three tiers of difficulty:

1. **Baseline cases** — direct questions that should clearly match one note, plus clearly unrelated questions that should be rejected.
2. **Borderline cases** — a question from earlier manual testing that scored just above the rejection threshold (0.31 against a 0.2 cutoff).
3. **Stress cases** — paraphrased questions with no shared vocabulary with the notes, and questions on related-but-uncovered ML topics, designed specifically to find where the system's retrieval breaks down.

## Result: 10/16

```
PASS  What is overfitting?
PASS  How do I stop overfitting?
PASS  How does gradient descent work?
PASS  What is the attention mechanism in transformers?
PASS  Compare gradient descent and overfitting
PASS  Who won the World Cup?
PASS  What is the capital of France?
PASS  How do I bake a chocolate cake?
PASS  How to minimize error in a model?
FAIL  Why the model memorizes instead of learning?
FAIL  My model does great on training data but terribly on new data. Why?
FAIL  How does a network figure out which parameters to change?
FAIL  What is a convolutional neural network?
FAIL  What is reinforcement learning?
FAIL  Tell me about machine learning
PASS  overfitting
```

## What the failures actually reveal

The 6 failures split into two distinct, opposite-pulling problems — not one bug to fix, but a real structural limitation worth understanding.

**1. Under-retrieval: indirect phrasing with no shared vocabulary**

"Why the model memorizes instead of learning?" and "How does a network figure out which parameters to change?" describe overfitting and gradient descent accurately, but use none of the notes' own wording. One scored below the 0.2 rejection threshold entirely; the other matched the wrong note. This suggests the embedding model's similarity scores degrade faster than expected once a question shares no surface-level vocabulary with the source text, even when the underlying concept is identical.

**2. Over-retrieval: topically adjacent but out-of-scope questions**

"What is a convolutional neural network?", "What is reinforcement learning?", and "Tell me about machine learning" are all ML topics — related in subject, but not covered by any of the three notes. The system retrieved sources for all three anyway, instead of rejecting them the way it correctly rejects clearly unrelated questions (World Cup, cake, France).

**Why one threshold can't fix both:** the under-retrieval failures need a *lower* `MIN_SCORE` to catch weakly-worded but valid matches. The over-retrieval failures need a *higher* `MIN_SCORE` to reject topically-adjacent-but-uncovered questions. A single global cutoff can't satisfy both at once — these two failure modes pull the threshold in opposite directions. This is a known, structural limitation of simple similarity-threshold retrieval, not a bug introduced by a specific setting.

## Why 10/16 is the right number to publish

It would have been easy to tune `MIN_SCORE` against this exact test set until the score looked better. That was deliberately avoided: with only 16 examples, tuning against them risks fitting the threshold to this specific list rather than improving genuine retrieval quality — the same failure mode as overfitting a model to its own test set. The honest, lower score is more informative than an inflated one.

## Project structure

```
├── eval_set.py     # The 16 test cases: question + expected source(s)
└── run_eval.py     # Sends each question to the API, compares results, reports a score
```

## Run it yourself

1. Have the RAG API running (locally via uvicorn, or in Docker):
```
   docker run -p 8000:8000 -e GROQ_API_KEY=your_key rag-api
```
2. Install the one dependency this needs:
```
   pip install requests
```
3. Run the evaluation:
```
   python run_eval.py
```

## Possible improvements

- Try a reranking step after retrieval, rather than adjusting the single similarity threshold
- Experiment with query expansion (rephrasing the user's question before embedding it) to close the vocabulary gap behind the under-retrieval failures
- Add partial-credit scoring once there's a larger, more varied test set to justify it
- Expand the test set beyond 16 questions, and track the score over time as the project changes

## Built with

Python · requests · the Notes RAG Chatbot's FastAPI endpoint
