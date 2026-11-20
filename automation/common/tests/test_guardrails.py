import pathlib
import tempfile
import unittest

from common import guardrails as g


class HostRules(unittest.TestCase):
    def setUp(self):
        self.hosts = g.parse_hosts("qa1box.evalytics.in, QA2BOX.evalytics.in")

    def test_default_and_extra_hosts(self):
        self.assertEqual(self.hosts, ("evalytics.in", "qa1box.evalytics.in", "qa2box.evalytics.in"))

    def test_apex_and_own_tenants_allowed(self):
        for url in ("https://evalytics.in/pricing", "https://qa1box.evalytics.in/login"):
            self.assertTrue(g.host_allowed(url, self.hosts), url)

    def test_other_tenants_blocked(self):
        # other academies are real customers
        self.assertFalse(g.host_allowed("https://someoneelse.evalytics.in/", self.hosts))

    def test_lookalikes_blocked(self):
        for url in ("https://evalytics.in.evil.com/", "https://evil-evalytics.in/", "https://google.com/"):
            self.assertFalse(g.host_allowed(url, self.hosts), url)

    def test_require_raises(self):
        with self.assertRaises(g.GuardrailError):
            g.require_host_allowed("https://example.com/", self.hosts)

    def test_no_extra(self):
        self.assertEqual(g.parse_hosts(None), ("evalytics.in",))
        self.assertEqual(g.parse_hosts(""), ("evalytics.in",))


class KillSwitch(unittest.TestCase):
    def test_env(self):
        with tempfile.TemporaryDirectory() as d:
            missing = pathlib.Path(d) / "KILL"
            self.assertFalse(g.kill_switch_active({}, missing))
            self.assertTrue(g.kill_switch_active({"EVA_KILL": "1"}, missing))
            self.assertFalse(g.kill_switch_active({"EVA_KILL": "0"}, missing))

    def test_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "KILL"
            f.write_text("stop")
            self.assertTrue(g.kill_switch_active({}, f))


class WritesAndTrackers(unittest.TestCase):
    def test_methods(self):
        for m in ("GET", "head", "OPTIONS"):
            self.assertTrue(g.write_allowed(m, False))
        for m in ("POST", "PUT", "PATCH", "DELETE"):
            self.assertFalse(g.write_allowed(m, False))
            self.assertTrue(g.write_allowed(m, True))

    def test_trackers(self):
        seen = {"evalytics.in", "fonts.googleapis.com", "www.google-analytics.com", "cdn.hotjar.com"}
        self.assertEqual(g.tracker_hosts(seen), ["cdn.hotjar.com", "www.google-analytics.com"])
        self.assertEqual(g.tracker_hosts({"evalytics.in", "fonts.gstatic.com"}), [])


class ThrottleTest(unittest.TestCase):
    def test_waits_only_when_needed(self):
        now = [100.0]
        slept = []

        def clock():
            return now[0]

        def sleep(s):
            slept.append(round(s, 3))
            now[0] += s

        t = g.Throttle(2.0, clock, sleep)
        t.wait()                 # first call never waits
        now[0] += 0.5
        t.wait()                 # 0.5 s passed, needs 1.5 s more
        now[0] += 5
        t.wait()                 # plenty of time passed
        self.assertEqual(slept, [1.5])


class AcademyFormSafety(unittest.TestCase):
    valid = ("QA Academy", "my-qa-1", "Test Owner", "a@b.com", "Passw0rd!", "Passw0rd!")

    def test_valid_form_is_refused(self):
        self.assertEqual(g.academy_form_problems(*self.valid), [])
        with self.assertRaises(g.GuardrailError):
            g.require_invalid_academy_form(*self.valid)

    def test_each_single_fault_is_caught(self):
        n, s, y, e, p, c = self.valid
        cases = {
            "empty name": ("", s, y, e, p, c),
            "bad subdomain": (n, "My_QA", y, e, p, c),
            "uppercase subdomain": (n, "MyQA", y, e, p, c),
            "empty subdomain": (n, "", y, e, p, c),
            "empty your name": (n, s, " ", e, p, c),
            "bad email": (n, s, y, "not-an-email", p, c),
            "empty password": (n, s, y, e, "", ""),
            "mismatch": (n, s, y, e, p, "Different1!"),
        }
        for label, fields in cases.items():
            self.assertTrue(g.require_invalid_academy_form(*fields), label)

    def test_plus_address_is_valid(self):
        n, s, y, _, p, c = self.valid
        self.assertEqual(g.academy_form_problems(n, s, y, "box+o01@gmail.com", p, c), [])


if __name__ == "__main__":
    unittest.main()
