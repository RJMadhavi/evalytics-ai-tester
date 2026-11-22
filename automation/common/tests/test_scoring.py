import unittest

from common.scoring import expected_result


class ReferenceScorer(unittest.TestCase):
    def test_all_correct(self):
        r = expected_result(list("ABCD"), list("ABCD"))
        self.assertEqual((r["correct"], r["wrong"], r["unattempted"]), (4, 0, 0))
        self.assertEqual((r["score"], r["max_score"], r["percentage"]), (16.0, 16.0, 100.0))

    def test_mixed_with_default_marks(self):
        # 2 right, 1 wrong, 1 blank: 2*4 - 1 = 7 out of 16
        r = expected_result(["A", "B", "D", None], list("ABCD"))
        self.assertEqual((r["correct"], r["wrong"], r["unattempted"]), (2, 1, 1))
        self.assertEqual(r["score"], 7.0)
        self.assertEqual(r["percentage"], 43.75)

    def test_negative_total_is_kept(self):
        r = expected_result(["B", "C", "D", "A"], list("AAAA"), 4.0, -1.0)
        # 1 right (the last "A" is wrong too): chosen B,C,D,A against A,A,A,A gives 1 right, 3 wrong
        self.assertEqual((r["correct"], r["wrong"]), (1, 3))
        self.assertEqual(r["score"], 1 * 4.0 + 3 * -1.0)

    def test_invalid_options_count_as_unattempted(self):
        r = expected_result(["a", "E", "", None, "A"], list("AAAAA"))
        self.assertEqual((r["correct"], r["wrong"], r["unattempted"]), (1, 0, 4))

    def test_custom_marks_and_rounding(self):
        r = expected_result(["A", "B", "C"], list("ABD"), 1.25, -0.33)
        self.assertEqual(r["correct"], 2)
        self.assertEqual(r["wrong"], 1)
        self.assertEqual(r["score"], round(2 * 1.25 - 0.33, 2))
        self.assertEqual(r["max_score"], 3.75)

    def test_no_negative_marking(self):
        r = expected_result(["B", "B"], list("AB"), 4.0, 0.0)
        self.assertEqual(r["score"], 4.0)

    def test_empty_exam(self):
        r = expected_result([], [])
        self.assertEqual((r["score"], r["max_score"], r["percentage"]), (0.0, 0.0, 0.0))

    def test_length_mismatch_is_an_error(self):
        with self.assertRaises(ValueError):
            expected_result(["A"], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
