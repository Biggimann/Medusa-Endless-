import json
from pathlib import Path

config = json.loads(
    (Path(__file__).resolve().parent / "subscription_config.json").read_text(encoding="utf-8")
)

print(f"{config['project']}: {config['subscription_terms']['access']}")
print(f"Payment method: {config['subscription_terms']['payment']['method']}")
print(f"Renewal: {config['subscription_terms']['payment']['renewal']}")
