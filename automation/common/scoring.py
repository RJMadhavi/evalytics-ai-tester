"""Independent reference scorer for Evalytics exams.

Used as a test oracle: compute the expected result from the answers a test submitted,
then compare it with what the app shows. It is written from the product rules, not copied
from the app, so a bug in the app does not hide a matching bug here.

Rules:
  - A chosen option must be one of A, B, C, D. Anything else counts as unattempted.
  - Correct answer: + marks_correct. Wrong answer: + marks_wrong (normally negative).
  - Unattempted: 0.
  - Score is rounded to 2 decimals. Maximum score is questions x marks_correct.
  - Percentage is score / maximum x 100, rounded to 2 decimals, and 0.0 if the maximum is 0.
"""

VALID_OPTIONS = ("A", "B", "C", "D")


def expected_result(chosen, key, marks_correct=4.0, marks_wrong=-1.0):
    """chosen and key are equal-length lists. chosen entries may be None or an option letter."""
    if len(chosen) != len(key):
        raise ValueError(f"chosen has {len(chosen)} entries but key has {len(key)}")
    correct = wrong = unattempted = 0
    for given, right in zip(chosen, key):
        if given not in VALID_OPTIONS:
            unattempted += 1
        elif given == right:
            correct += 1
        else:
            wrong += 1
    score = round(correct * marks_correct + wrong * marks_wrong, 2)
    max_score = len(key) * marks_correct
    percentage = round(score / max_score * 100, 2) if max_score > 0 else 0.0
    return {
        "correct": correct,
        "wrong": wrong,
        "unattempted": unattempted,
        "score": score,
        "max_score": max_score,
        "percentage": percentage,
    }
