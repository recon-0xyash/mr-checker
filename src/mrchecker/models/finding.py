from pathlib import Path

from pydantic import BaseModel


class Finding(BaseModel):
    file: Path

    line: int

    rule_id: str
    rule_name: str

    description: str

    category: str

    severity: str

    recommendation: str

    secret: str
