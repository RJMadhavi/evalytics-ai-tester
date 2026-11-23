#!/usr/bin/env python3
"""Score an extraction against a golden truth file.

Run from the automation/ folder:
    python3 ai_eval/score.py ai_eval/corpus/clean_with_key.truth.json extracted.json

extracted.json is a list of questions with question_text, option_a to option_d and
correct_option, as the app produces them.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from common.extraction_metrics import evaluate_extraction  # noqa: E402


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    truth = json.loads(pathlib.Path(sys.argv[1]).read_text())
    extracted = json.loads(pathlib.Path(sys.argv[2]).read_text())
    truth_questions = truth["questions"] if isinstance(truth, dict) else truth
    result = evaluate_extraction(truth_questions, extracted)
    for key, value in result.items():
        print(f"{key:22} {value}")


if __name__ == "__main__":
    main()
