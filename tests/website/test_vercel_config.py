from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERCEL_CONFIG = ROOT / "vercel.json"
WEBSITE = ROOT / "website"


class VercelConfigurationTests(unittest.TestCase):
    def test_vercel_config_publishes_website_directory(self) -> None:
        self.assertTrue(VERCEL_CONFIG.exists(), "missing root vercel.json")
        config = json.loads(VERCEL_CONFIG.read_text(encoding="utf-8"))
        self.assertEqual(
            config.get("$schema"),
            "https://openapi.vercel.sh/vercel.json",
        )
        self.assertIsNone(config.get("framework"))
        self.assertEqual(config.get("outputDirectory"), "website")

    def test_output_directory_has_static_entrypoint_and_assets(self) -> None:
        self.assertTrue((WEBSITE / "index.html").is_file())
        self.assertTrue((WEBSITE / "assets" / "styles.css").is_file())
        self.assertTrue((WEBSITE / "assets" / "app.js").is_file())


if __name__ == "__main__":
    unittest.main()
