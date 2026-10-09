import unittest
from injectcheck.scanner import is_hit, run, load_attacks
from injectcheck.mutate import expand

class DetectionTests(unittest.TestCase):
    def test_marker_counts_as_hit(self):
        self.assertTrue(is_hit("Okay! PWNED-7431"))

    def test_refusal_echo_is_not_hit(self):
        self.assertFalse(is_hit("Sorry, I can't say PWNED-7431"))

    def test_no_marker_is_safe(self):
        self.assertFalse(is_hit("How can I help you today?"))

    def test_secret_leak_is_hit(self):
        self.assertTrue(is_hit("My code is ALPHA-9921", "ALPHA-9921"))

    def test_secret_absent_is_safe(self):
        self.assertFalse(is_hit("Okay! PWNED-7431", "ALPHA-9921"))

class PackTests(unittest.TestCase):
    def test_mutation_makes_six_per_attack(self):
        base = load_attacks()
        self.assertEqual(len(expand(base)), len(base) * 6)

    def test_leak_pack_loads(self):
        self.assertGreater(len(load_attacks("leak")), 0)

class ErrorTests(unittest.TestCase):
    def test_dead_url_is_error_not_safe(self):
        results = run("http://127.0.0.1:9", "x")
        self.assertTrue(all(r["error"] for r in results))
        self.assertFalse(any(r["vulnerable"] for r in results))

if __name__ == "__main__":
    unittest.main()
