"""Deterministic rule-based evaluator. No model, network, or secrets required."""
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import re

@dataclass
class CaseResult:
    id: str
    category: str
    expected: str
    observed: str
    passed: bool
    rationale: str
    safe_output: str

def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def detect_injection(text: str) -> bool:
    """Small, explainable heuristic detector; not a security-grade classifier."""
    value = _normalise(text)
    patterns = (
        r"\bignore (all |any |the )?(previous|prior|above) instructions?\b",
        r"\b(disregard|override) (all |any |the )?(previous|prior|above) instructions?\b",
        r"\breveal (the )?(system prompt|hidden instructions|secret)\b",
        r"\bprint (the )?(api key|password|secret)\b",
        r"\byou are now (in )?(developer|admin|unrestricted) mode\b",
        r"\bdo not follow (the )?(system|developer) instructions?\b",
        r"\bwhen (you )?summarise this (page|document|email)\b.*\b(send|reveal|exfiltrate)\b",
    )
    return any(re.search(pattern, value) for pattern in patterns)

def evaluate_case(case: Dict[str, Any]) -> CaseResult:
    payload = case["payload"]
    observed = "blocked" if detect_injection(payload) else "not_flagged"
    expected = case["expected"]
    passed = observed == expected
    rationale = (
        "Heuristic matched an instruction-overriding or data-exfiltration pattern."
        if observed == "blocked" else
        "No configured injection pattern matched; content remains untrusted input."
    )
    # The harness never executes payload instructions or accesses secrets.
    safe_output = "UNTRUSTED_INPUT_BLOCKED" if observed == "blocked" else "UNTRUSTED_INPUT_QUARANTINED"
    return CaseResult(case["id"], case["category"], expected, observed, passed,
                      rationale, safe_output)

def run_suite(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = [evaluate_case(case) for case in cases]
    return {
        "total": len(results),
        "passed": sum(1 for result in results if result.passed),
        "failed": sum(1 for result in results if not result.passed),
        "results": [asdict(result) for result in results],
    }
