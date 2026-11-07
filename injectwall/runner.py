"""Fixture loading and suite orchestration."""
import json
from pathlib import Path
from typing import List, Dict, Any
from .engine import run_suite

def load_cases(path=None) -> List[Dict[str, Any]]:
    fixture_path = Path(path) if path else Path(__file__).parent / "fixtures" / "cases.json"
    with fixture_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Fixture file must contain a JSON array")
    required = {"id", "category", "payload", "expected"}
    for index, case in enumerate(data):
        if not isinstance(case, dict) or not required.issubset(case):
            raise ValueError(f"Case {index} must contain: {', '.join(sorted(required))}")
        if case["expected"] not in {"blocked", "not_flagged"}:
            raise ValueError(f"Case {index} has unsupported expected value")
    return data

def run(path=None):
    return run_suite(load_cases(path))
