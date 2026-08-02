from re import Pattern
from typing import Literal

from pydantic import BaseModel


class Rule(BaseModel):
    id: str
    name: str

    description: str

    category: str

    severity: Literal[
        "critical",
        "high",
        "medium",
        "low",
    ]

    recommendation: str

    pattern: Pattern[str]
