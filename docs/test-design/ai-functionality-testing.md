---
id: EVA-DOC-007
title: AI Functionality Testing Strategy
goal: G6
status: Draft
related: EVA-DOC-006
---

# AI Functionality Testing Strategy

Goal 6 is testing the underlying AI functionality. This document says what that means, what can go wrong and how each feature is tested.

**What is in scope:** the AI-powered features of Evalytics and how the app uses them. **What is not:** benchmarking the language model itself, which belongs to its maker. A test fails when the app produces a wrong or unsafe result, whatever the cause.

## 1. The AI features

| Feature | What the user gets | Main risk |
|---------|--------------------|-----------|
| Question extraction | Questions pulled from a PDF or DOCX into the question bank | Missing, merged, duplicated or garbled questions and options |
| Answer inference | When a paper has no answer key, the app works the answers out | A wrong answer key that looks as trustworthy as a real one |
| Explanations | A step-by-step solution for a question | A solution that contradicts the key, or is wrong |
| Formula handling | Chemistry formulas and maths symbols made readable | Corrupted subscripts, powers or symbols |
| Diagrams | Figures cropped and attached to the right question | A figure on the wrong question, or lost |
| Translation | Questions in Hindi, Marathi and Kannada | Changed numbers, units or formulas, or text left in English |
| Question generation | New questions for a chapter and difficulty mix | Unanswerable, duplicate or wrongly keyed questions |
| Genie | Natural-language questions about academy data | Wrong numbers, data from the wrong academy, instructions hidden in data |

## 2. What can go wrong

1. **Wrong content** that looks right: a swapped option, a mistaken answer key, a translated number.
2. **Silent failure**: when an AI call fails, the app skips a step and says nothing, for example showing no translation instead of an error.
3. **Fallback paths** that behave differently: the app has more than one way to read a file, and each way should be tested.
4. **Non-determinism**: the same file can give slightly different results on two runs.
5. **Prompt injection**: text inside a paper, a student name or a batch name that tries to give the AI orders.
6. **Cost and quota**: each upload and each AI call costs money and uses a small allowance.
7. **Speed**: the site claims extraction in under 10 seconds.
8. **Availability**: what happens when the AI service is slow, down or returns a malformed answer.

## 3. Approach

| Layer | What is tested | How | Where |
|-------|----------------|-----|-------|
| Pure logic | Cleanup rules, formula formatting, answer-key parsing, scoring | Unit tests with fixed inputs, no AI call | CI |
| Contract | The app handles AI replies correctly, including bad ones | Feed canned replies (valid, wrapped in extra text, broken, empty, too long) | Private local copy |
| Golden corpus | Extraction quality | Known papers, scored with `common/extraction_metrics.py` | Own academy for a few uploads, local copy for many |
| Answer inference | How often the app's worked-out answers are right | Papers with no key and known answers | Own academy, local copy |
| Explanations | Correct, consistent with the key | Rubric, plus a check that numbers re-derive | Local copy |
| Translation | Meaning kept, numbers and formulas intact | Automatic invariants plus a bilingual reviewer sample | Own academy, local copy |
| Generation | Valid, answerable, distinct, right difficulty mix | Structure checks, duplicate checks, human sample | Local copy |
| Genie | Accuracy, isolation, injection | See the test design document | Local copy |
| Resilience | Behaviour on timeouts, errors, limits | Fault injection on the local copy | Local copy |
| Speed and cost | Time and spend per upload | Timed runs, a cost log | Own academy, local copy |

## 4. Handling non-determinism

- Run each case at least **3 times** and report the average and the worst result, not one lucky run.
- Judge with **thresholds**, not exact text. Exact matching is only for pure logic.
- Record the date, the app version and the model settings with every run, so a drop in quality can be tied to a change.
- Keep a **baseline** after the first full run, then compare every later run against it.
- Prefer automatic checks. Where a person must judge (translations, explanations), use a fixed rubric and a sample.

## 5. Golden corpus

The corpus is invented. It contains no real papers and nothing copyrighted.

**Built so far** (`automation/ai_eval/corpus`): four papers of 9 to 10 questions each, with truth files. They cover a clean paper with a key, a paper without a key, two columns and chemical formulas.

**Still to build** (to reach 15 to 20):

- scanned (image-only) pages, and pages photographed at an angle
- bilingual side-by-side papers, and papers in Hindi, Marathi and Kannada
- diagram questions and questions whose options are images
- tables inside questions, and long passages with several questions
- DOCX papers in several layouts, including equations
- answer keys in different layouts, and a partly wrong key
- documents that are not question papers (to check they are rejected)
- a question containing text that tries to instruct the AI
- very large and very small files

## 6. Metrics and proposed targets

Targets are starting points and will be set after the first full baseline run.

| Metric | Proposed target on clean papers |
|--------|--------------------------------|
| Question recall | at least 0.95 |
| Question precision | at least 0.95 |
| Option accuracy | at least 0.97 |
| Answer accuracy when the file has a key | 1.00 |
| Answer accuracy when the app infers the answer | report it, then agree a target |
| Answers inferred but shown as if from a key | none |
| Extraction time | median under 10 seconds, to test the claim |

Whatever the inferred-answer accuracy turns out to be, the product should say which answers were worked out by the AI. Test that the screen makes the difference visible.

## 7. Safety and cost rules

- Use only invented papers and synthetic names. Never upload real student work or copyrighted papers.
- Every upload uses the academy's small AI allowance, so write down the number left after each one.
- Ask the owner for a higher allowance and a cost cap before any large run. Large runs go to the private local copy.
- Tests must not try to make the AI say harmful things. Injection tests use harmless instructions.

## 8. Work and estimates

These fit inside the existing epic EVA-E11 (52 hours).

| Work | Hours | Status |
|------|------:|--------|
| Extraction scorer and unit tests | 3 | Done |
| First four golden papers and generator | 4 | Done |
| Remaining corpus (11 to 16 more papers) | 8 | To do |
| Extraction runs and baseline | 7 | To do |
| Answer inference accuracy | 4 | To do |
| Explanation checks | 6 | To do |
| Translation checks | 8 | To do |
| Generation checks | 4 | To do |
| Contract and resilience tests (local copy) | 6 | To do |
| Speed and cost log | 3 | To do |

## 9. Questions for the owner

1. Can the AI allowance of the test academy be raised, and what cost cap applies?
2. Is there a way to run the AI features with test settings, or is the allowance the only control?
3. Does the app say anywhere which answers were inferred by the AI rather than taken from a key?
4. How are changes to the AI settings announced, so a quality drop can be traced to its cause?
