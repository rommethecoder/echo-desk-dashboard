import copy
import json
from pathlib import Path
import unittest
import generate

CONFIG = json.loads(
    (Path(__file__).resolve().parents[1] / "examples/entities.json").read_text()
)


class Dashboard(unittest.TestCase):
    def test_native_layout(self):
        view = generate.generate(CONFIG)["views"][0]
        self.assertEqual(view["type"], "sections")
        self.assertEqual(view["max_columns"], 2)
        cards = view["sections"][0]["cards"]
        self.assertEqual(len(cards), 7)
        self.assertTrue(all(not c["type"].startswith("custom:") for c in cards))

    def test_no_private_hosts_or_auth(self):
        result = json.dumps(generate.generate(CONFIG))
        self.assertNotIn("http", result)
        self.assertNotIn("token", result)
        self.assertNotIn("/home/", result)

    def test_no_entity_injection(self):
        for value in ["{{ states }}", "binary_sensor.a'); evil", "light.wrong_domain"]:
            config = copy.deepcopy(CONFIG)
            config["door"] = value
            with self.assertRaises(ValueError):
                generate.generate(config)

    def test_empty_and_invalid_timezone(self):
        with self.assertRaises(ValueError):
            generate.generate({})
        config = copy.deepcopy(CONFIG)
        config["timezone"] = "Not/A_Zone"
        with self.assertRaises(KeyError):
            generate.generate(config)

    def test_unknown_sensor_states(self):
        result = json.dumps(generate.generate(CONFIG))
        self.assertIn("Door status unavailable", result)
        self.assertIn("Battery status unavailable", result)

    def test_optional_entities(self):
        result = generate.generate(
            {"lights": [{"name": "Lamp", "entity": "light.lamp"}]}
        )
        self.assertEqual(len(result["views"][0]["sections"][0]["cards"]), 2)
