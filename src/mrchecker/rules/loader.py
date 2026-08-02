import re
import tomllib
from pathlib import Path

from mrchecker.models.rule import Rule

RULE_FILE = Path(__file__).parent / "builtin.toml"


def load_rules() -> list[Rule]:
    """
    Load built-in detection rules.
    """

    with RULE_FILE.open("rb") as f:
        data = tomllib.load(f)

    rules: list[Rule] = []

    for entry in data["rules"]:
        rules.append(
            Rule(
                id=entry["id"],
                name=entry["name"],
                description=entry["description"],
                category=entry["category"],
                severity=entry["severity"],
                recommendation=entry["recommendation"],
                pattern=re.compile(entry["pattern"]),
            )
        )

    return rules
