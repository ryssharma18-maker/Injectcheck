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

from unittest.mock import patch, Mock
import requests
from injectcheck.scanner import send

class RetryTests(unittest.TestCase):
    @patch("injectcheck.scanner.time.sleep")
    @patch("injectcheck.scanner.requests.post")
    def test_429_then_success(self, post, sleep):
        limited = Mock(status_code=429, headers={"Retry-After": "1"})
        success = Mock(status_code=200, headers={})
        success.json.return_value = {"choices": [{"message": {"content": "Hello"}}]}
        post.side_effect = [limited, success]
        result = send("https://example.test", "x", "hello", "openai", "test-model")
        self.assertEqual(result, "Hello")
        self.assertEqual(post.call_count, 2)
        sleep.assert_called_once_with(1)

    @patch("injectcheck.scanner.time.sleep")
    @patch("injectcheck.scanner.requests.post")
    def test_persistent_429_raises_error(self, post, sleep):
        limited = Mock(status_code=429, headers={})
        limited.raise_for_status.side_effect = requests.HTTPError("429")
        post.return_value = limited
        with self.assertRaises(requests.HTTPError):
            send("https://example.test", "x", "hello", "openai", "test-model")
        self.assertEqual(post.call_count, 3)
        self.assertEqual(sleep.call_count, 2)
