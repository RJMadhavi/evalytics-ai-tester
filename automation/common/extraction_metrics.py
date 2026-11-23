"""Score how well an extraction (from a PDF or DOCX) matches the known questions.

Used as a test oracle for the AI features. A question here is a dict with
question_text, option_a, option_b, option_c, option_d and correct_option (A to D, or
None when the answer is missing). Extra keys are ignored.

Matching is one-to-one and tolerant of small wording differences, so formatting changes
such as H2O versus H2O with a subscript two do not count as a miss.
"""
import difflib
import re
import unicodedata

OPTION_KEYS = ("option_a", "option_b", "option_c", "option_d")
_DROP = re.compile(r"[^\w+\-*/^=<>().%]")


def normalise_text(text):
    """Lowercase, fold subscripts and similar forms to plain characters, drop spaces and most punctuation."""
    text = unicodedata.normalize("NFKD", str(text or "")).lower()
    return _DROP.sub("", text)


def similarity(a, b):
    na, nb = normalise_text(a), normalise_text(b)
    if not na and not nb:
        return 1.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def match_questions(truth, extracted, threshold=0.8):
    """Pair each known question with at most one extracted question, best matches first.

    Returns (pairs, missed, spurious): pairs are (truth_index, extracted_index, score),
    missed are truth indexes with no match, spurious are extracted indexes with no match.
    """
    scored = []
    for i, t in enumerate(truth):
        for j, e in enumerate(extracted):
            s = similarity(t.get("question_text", ""), e.get("question_text", ""))
            if s >= threshold:
                scored.append((s, i, j))
    scored.sort(reverse=True)
    used_t, used_e, pairs = set(), set(), []
    for s, i, j in scored:
        if i in used_t or j in used_e:
            continue
        used_t.add(i)
        used_e.add(j)
        pairs.append((i, j, round(s, 3)))
    missed = [i for i in range(len(truth)) if i not in used_t]
    spurious = [j for j in range(len(extracted)) if j not in used_e]
    return sorted(pairs), missed, spurious


def evaluate_extraction(truth, extracted, threshold=0.8):
    """Compare an extraction with the known questions and return the metrics.

    question_recall      matched / known questions
    question_precision   matched / extracted questions (junk and duplicates lower it)
    option_accuracy      average share of the 4 options that match, over matched questions
    answer_coverage      share of matched questions that have an answer
    answer_key_accuracy  share of the answers given that are right, over matched questions
    """
    if not truth:
        raise ValueError("truth must contain at least one question")
    pairs, missed, spurious = match_questions(truth, extracted, threshold)
    matched = len(pairs)

    option_scores, answered, right = [], 0, 0
    for i, j, _ in pairs:
        t, e = truth[i], extracted[j]
        good = sum(1 for k in OPTION_KEYS if similarity(t.get(k, ""), e.get(k, "")) >= threshold)
        option_scores.append(good / len(OPTION_KEYS))
        given = str(e.get("correct_option") or "").strip().upper()
        if given in ("A", "B", "C", "D"):
            answered += 1
            if given == str(t.get("correct_option") or "").strip().upper():
                right += 1

    def ratio(a, b):
        return round(a / b, 4) if b else 0.0

    return {
        "known": len(truth),
        "extracted": len(extracted),
        "matched": matched,
        "question_recall": ratio(matched, len(truth)),
        "question_precision": ratio(matched, len(extracted)),
        "option_accuracy": round(sum(option_scores) / matched, 4) if matched else 0.0,
        "answer_coverage": ratio(answered, matched),
        "answer_key_accuracy": ratio(right, answered),
        "missed": missed,
        "spurious": spurious,
    }
