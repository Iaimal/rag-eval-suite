# eval_set.py

TESTS = [
    # baseline cases
    {"question": "What is overfitting?", "expected": ["overfitting.txt"]},
    {"question": "How do I stop overfitting?", "expected": ["overfitting.txt"]},
    {"question": "How does gradient descent work?", "expected": ["gradient_descent.txt"]},
    {"question": "What is the attention mechanism in transformers?", "expected": ["transformers.txt"]},
    {"question": "Compare gradient descent and overfitting", "expected": ["gradient_descent.txt", "overfitting.txt"]},
    {"question": "Who won the World Cup?", "expected": []},
    {"question": "What is the capital of France?", "expected": []},
    {"question": "How do I bake a chocolate cake?", "expected": []},

    # borderline / previously-measured low scores
    {"question": "How to minimize error in a model?", "expected": ["overfitting.txt"]},
    {"question": "Why the model memorizes instead of learning?", "expected": ["overfitting.txt"]},

    # paraphrased, no keyword overlap with the notes
    {"question": "My model does great on training data but terribly on new data. Why?", "expected": ["overfitting.txt"]},
    {"question": "How does a network figure out which parameters to change?", "expected": ["gradient_descent.txt"]},

    # near-miss: related to ML, but probably not in your notes
    {"question": "What is a convolutional neural network?", "expected": []},
    {"question": "What is reinforcement learning?", "expected": []},

    # vague or tricky
    {"question": "Tell me about machine learning", "expected": []},
    {"question": "overfitting", "expected": ["overfitting.txt"]},
]