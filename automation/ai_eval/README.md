# AI evaluation

Tools for testing the AI features of Evalytics (goal 6). Everything here is synthetic.

## Contents

| File | Purpose |
|------|---------|
| `make_golden_pdfs.py` | Builds synthetic multiple-choice papers with known answers |
| `corpus/*.pdf` and `corpus/*.truth.json` | The generated papers and what a perfect extraction would return |
| `score.py` | Scores an extraction against a truth file |
| `../common/extraction_metrics.py` | The scoring functions, with unit tests that run in CI |

## The papers

| Paper | Questions | Answer key in file | What it checks |
|-------|----------:|--------------------|----------------|
| `clean_with_key` | 10 | Yes, on a last page | Basic extraction and reading the answer key |
| `clean_no_key` | 10 | No | Whether the app works out the answers itself, and how accurately |
| `two_column_with_key` | 10 | Yes | Reading order across two columns |
| `formulas_with_key` | 9 | Yes | Chemical formulas, powers and symbols such as `H2SO4`, `Ca(OH)2`, `x^2` |

## Rebuild the papers

```bash
pip install -r ai_eval/requirements.txt
python3 ai_eval/make_golden_pdfs.py
```

## Score a run

Upload a paper to your own test academy (this uses AI quota, so plan each upload), copy the extracted
questions into a JSON list, then run:

```bash
python3 ai_eval/score.py ai_eval/corpus/clean_with_key.truth.json extracted.json
```

| Metric | Meaning |
|--------|---------|
| `question_recall` | Share of the known questions that were found |
| `question_precision` | Share of the extracted items that are real, distinct questions |
| `option_accuracy` | Share of the four options that match, over the questions found |
| `answer_coverage` | Share of found questions that have an answer |
| `answer_key_accuracy` | Share of the answers given that are right |

Formatting changes such as a subscript two in `H2O` are not counted as errors.

## Rules

- Do not add real exam papers or anything copyrighted. Invent the questions.
- Each upload uses the academy's AI quota. Record how much is left after every upload.
- Never commit extraction results that contain real student data. There should be none.
