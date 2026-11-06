#!/usr/bin/env python3
"""Generate a native-card Home Assistant dashboard from an explicit entity map."""

import argparse
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

DOMAINS = {
    "weather": "weather",
    "climate": "climate",
    "doorbell": "camera",
    "door": "binary_sensor",
    "battery": "sensor",
}


def entity(value, domain):
    if not isinstance(value, str) or not re.fullmatch(
        re.escape(domain) + r"\.[a-z0-9_]+", value
    ):
        raise ValueError(f"Expected a {domain} entity ID.")
    return value


def generate(config):
    values = {k: entity(config[k], d) for k, d in DOMAINS.items() if config.get(k)}
    if not values and not config.get("lights"):
        raise ValueError("Configure at least one entity.")
    clock = {
        "type": "clock",
        "clock_style": "digital",
        "clock_size": "medium",
        "time_format": "24",
        "show_seconds": False,
    }
    if config.get("timezone"):
        ZoneInfo(config["timezone"])
        clock["time_zone"] = config["timezone"]
    cards = [clock]
    if "weather" in values:
        cards.append(
            {
                "type": "weather-forecast",
                "entity": values["weather"],
                "show_current": True,
                "show_forecast": False,
            }
        )
    if "climate" in values:
        cards.append(
            {
                "type": "tile",
                "entity": values["climate"],
                "name": "Thermostat",
                "features": [{"type": "target-temperature"}],
            }
        )
    if "doorbell" in values:
        cards.append(
            {
                "type": "tile",
                "entity": values["doorbell"],
                "name": "Doorbell",
                "tap_action": {"action": "more-info"},
            }
        )
    status = []
    if "door" in values:
        status.append(
            "{% set door = states('"
            + values["door"]
            + "') %}{{ 'Door open' if door == 'on' else 'All clear' if door == 'off' else 'Door status unavailable' }}"
        )
    if "battery" in values:
        status.append(
            "{% set battery = states('"
            + values["battery"]
            + "') %}{{ 'Battery: ' ~ battery ~ '%' if is_number(battery) else 'Battery status unavailable' }}"
        )
    if status:
        cards.append(
            {"type": "markdown", "title": "Status", "content": "\n\n".join(status)}
        )
    for light in config.get("lights", []):
        if not isinstance(light.get("name"), str) or not 0 < len(light["name"]) <= 80:
            raise ValueError("Light names must contain 1–80 characters.")
        cards.append(
            {
                "type": "tile",
                "entity": entity(light["entity"], "light"),
                "name": light["name"],
                "tap_action": {"action": "toggle"},
                "icon_tap_action": {"action": "toggle"},
            }
        )
    return {
        "title": "Echo Desk",
        "views": [
            {
                "title": "Desk",
                "path": "desk",
                "type": "sections",
                "max_columns": 2,
                "sections": [{"type": "grid", "cards": cards}],
            }
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("config", type=Path)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    try:
        result = generate(json.loads(a.config.read_text()))
        with a.output.open("x") as f:
            json.dump(result, f, indent=2)
            f.write("\n")
        print(a.output)
    except (OSError, ValueError, KeyError) as e:
        p.exit(1, str(e) + "\n")


if __name__ == "__main__":
    main()
