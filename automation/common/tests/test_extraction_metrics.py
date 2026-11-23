import copy
import unittest

from common.extraction_metrics import evaluate_extraction, match_questions, normalise_text, similarity

TRUTH = [
    {"question_text": "What is the chemical formula of water?", "option_a": "H2O", "option_b": "CO2",
     "option_c": "NaCl", "option_d": "O2", "correct_option": "A"},
    {"question_text": "Which planet is known as the Red Planet?", "option_a": "Venus", "option_b": "Mars",
     "option_c": "Jupiter", "option_d": "Saturn", "correct_option": "B"},
    {"question_text": "The square root of 144 is", "option_a": "10", "option_b": "11",
     "option_c": "12", "option_d": "14", "correct_option": "C"},
    {"question_text": "Which organ pumps blood through the human body?", "option_a": "Lungs", "option_b": "Liver",
     "option_c": "Heart", "option_d": "Kidney", "correct_option": "C"},
]


def perfect():
    return copy.deepcopy(TRUTH)


class Normalisation(unittest.TestCase):
    def test_subscripts_and_spacing_do_not_matter(self):
        self.assertEqual(normalise_text("H\u2082O"), normalise_text("h2o "))
        self.assertGreaterEqual(similarity("H\u2082SO\u2084", "H2SO4"), 0.99)

    def test_different_text_is_not_similar(self):
        self.assertLess(similarity("Mars", "Heart"), 0.6)

    def test_empty_strings_match(self):
        self.assertEqual(similarity("", None), 1.0)


class Matching(unittest.TestCase):
    def test_order_does_not_matter(self):
        shuffled = list(reversed(perfect()))
        pairs, missed, spurious = match_questions(TRUTH, shuffled)
        self.assertEqual((len(pairs), missed, spurious), (4, [], []))

    def test_each_extracted_question_is_used_once(self):
        doubled = perfect() + perfect()
        pairs, missed, spurious = match_questions(TRUTH, doubled)
        self.assertEqual((len(pairs), missed, len(spurious)), (4, [], 4))


class Evaluation(unittest.TestCase):
    def test_perfect_extraction(self):
        r = evaluate_extraction(TRUTH, perfect())
        self.assertEqual((r["question_recall"], r["question_precision"]), (1.0, 1.0))
        self.assertEqual((r["option_accuracy"], r["answer_coverage"], r["answer_key_accuracy"]), (1.0, 1.0, 1.0))

    def test_missing_question_lowers_recall_only(self):
        r = evaluate_extraction(TRUTH, perfect()[:3])
        self.assertEqual((r["question_recall"], r["question_precision"], r["missed"]), (0.75, 1.0, [3]))

    def test_junk_and_duplicates_lower_precision_only(self):
        ex = perfect() + [{"question_text": "Page 3 of 10 Evalytics sample paper"}, perfect()[0]]
        r = evaluate_extraction(TRUTH, ex)
        self.assertEqual(r["question_recall"], 1.0)
        self.assertAlmostEqual(r["question_precision"], 4 / 6, places=3)

    def test_wrong_option_text(self):
        ex = perfect()
        ex[1]["option_b"] = "Earth"
        r = evaluate_extraction(TRUTH, ex)
        # 15 of the 16 options match (one option in one question is wrong)
        self.assertAlmostEqual(r["option_accuracy"], 15 / 16, places=3)

    def test_wrong_answer_key(self):
        ex = perfect()
        ex[0]["correct_option"] = "B"
        r = evaluate_extraction(TRUTH, ex)
        self.assertEqual((r["answer_coverage"], r["answer_key_accuracy"]), (1.0, 0.75))

    def test_missing_answers_lower_coverage_not_accuracy(self):
        ex = perfect()
        ex[0]["correct_option"] = None
        ex[1]["correct_option"] = ""
        r = evaluate_extraction(TRUTH, ex)
        self.assertEqual((r["answer_coverage"], r["answer_key_accuracy"]), (0.5, 1.0))

    def test_invalid_answer_letter_counts_as_no_answer(self):
        ex = perfect()
        ex[2]["correct_option"] = "E"
        r = evaluate_extraction(TRUTH, ex)
        self.assertEqual(r["answer_coverage"], 0.75)

    def test_formatting_changes_do_not_count_as_errors(self):
        ex = perfect()
        ex[0]["option_a"] = "H\u2082O"
        ex[0]["question_text"] = "  What is the chemical formula of  water ? "
        r = evaluate_extraction(TRUTH, ex)
        self.assertEqual((r["question_recall"], r["option_accuracy"]), (1.0, 1.0))

    def test_empty_extraction(self):
        r = evaluate_extraction(TRUTH, [])
        self.assertEqual((r["question_recall"], r["question_precision"], r["missed"]), (0.0, 0.0, [0, 1, 2, 3]))

    def test_empty_truth_is_an_error(self):
        with self.assertRaises(ValueError):
            evaluate_extraction([], perfect())


if __name__ == "__main__":
    unittest.main()
