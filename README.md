# Echo Desk Dashboard

A configurable Home Assistant dashboard starter for a small desk display. Adapted from a working Echo Show desk setup, with native cards for a clock, weather, thermostat, doorbell, door/battery status and lights.

The public generator creates a separate dashboard from a small entity map. It does not contact Home Assistant, store tokens, provision integrations, root a device or install firmware. It does not include the author's home configuration or the private shadow-DOM CSS adjustments used on the original display.

## Requirements and generation

Python 3.11+ and a Home Assistant version supporting the native Clock card, Tile features and Sections views. Card contracts were checked against the Home Assistant 2026.11 documentation. Older installations may need updating or substituting a card.

```sh
cp examples/entities.json entities.local.json
# Edit entities.local.json with your own entity IDs and time zone.
python generate.py entities.local.json --output dashboard.local.json
python -m unittest discover -s tests -v
```

Optional entities can be omitted or set to an empty string. At least one entity/light must be configured. Use a valid IANA time zone or omit it to use the Home Assistant profile's setting. The generator refuses to overwrite an existing output file.

## Import as a separate dashboard

1. Back up any dashboard you intend to edit. Create a new dashboard in Home Assistant rather than replacing your default one.
2. Open that dashboard's raw configuration editor. Paste the generated JSON object (JSON is also valid YAML) and save it.
3. Confirm that every entity exists in **Developer Tools → States**. Check the thermostat feature against your climate integration, and test each light tile before sharing the dashboard.
4. Open the new dashboard on your intended display and phone. Adjust section/card sizing in the visual editor for your screen, text size and browser zoom. The Sections layout can reflow; this release does not promise that every combination fits a single 800×480 screen without scrolling.
5. Use an ordinary authenticated Home Assistant user/session for the kiosk. Camera, climate and light access still follows your Home Assistant account's permissions; this template adds no separate authorization layer.

The status card distinguishes unavailable door/battery data from an actual clear state or a zero-percent battery. The camera opens its More info view; the generated dashboard does not make a continuous camera feed or doorbell announcement automation.

## Validation and limits

Tests check required card structure, example generation, optional entities, domain validation, unsafe entity strings and explicit unavailable states. This extracted generator has not been deployed to the author's live Home Assistant instance; a real integration/device check remains necessary. The earlier personal dashboard's successful screen checks do not validate this new package on every device.

No HACS cards, cloud service, firmware image, local hostname, photos or account credentials are included. Generated local files are ignored by Git. Keep your entity map and real dashboard export private; open issues using the example map and a minimal reproduction.

## References

- [Clock card](https://www.home-assistant.io/dashboards/clock/)
- [Sections views](https://www.home-assistant.io/dashboards/sections/)
- [Tile card](https://www.home-assistant.io/dashboards/tile/)

Original generator and examples by Terry (Romme) Felton, developed with AI assistance. MIT licensed.
