import json, re, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1] / "skills"

class SkillConfigTests(unittest.TestCase):
    def test_no_secrets_and_local_hosts_only(self):
        for p in SK.glob("*.skill.json"):
            text = p.read_text(); d = json.loads(text)
            self.assertFalse(re.search(r'(?i)"(password|token|cookie|api_?key|secret)"\s*:', text))
            self.assertTrue(set(d["allowed_hosts"]) <= {"127.0.0.1", "localhost", "[::1]"})
            self.assertIn("skill_version", d); self.assertTrue(d["stop_on"])
    def test_dates_are_parameters_not_literals(self):
        d = json.loads((SK / "upright-paid-orders.skill.json").read_text())
        fills = [s["value"] for s in d["steps"] if s["op"] == "fill"]
        self.assertEqual(fills, ["{start_date}", "{end_date}"])
    def test_runner_blocks_non_allowed_hosts_in_source(self):
        src = (SK.parent / "run_skill.cjs").read_text()
        for needle in ("host_not_allowed", "allowed_hosts", "bad_params", "expired_session", "label_changed", "timeout"):
            self.assertIn(needle, src)

if __name__ == "__main__": unittest.main()
