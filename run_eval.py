# run_eval.py
import requests
from eval_set import TESTS

API_URL = "http://127.0.0.1:8000/ask"

def run_evaluation():
    correct = 0
    total = len(TESTS)

    for case in TESTS:
        response = requests.post(API_URL, json={"question": case["question"]})
        result = response.json()
        actual_sources = result.get("sources") or []

        expected = case["expected"]
        is_correct = set(actual_sources) == set(expected)

        if is_correct:
            correct += 1

        print(f"Q: {case['question']}")
        print(f"  Expected: {expected} | Got: {actual_sources} | {'PASS' if is_correct else 'FAIL'}")

    print(f"\nScore: {correct}/{total}")

if __name__ == "__main__":
    run_evaluation()