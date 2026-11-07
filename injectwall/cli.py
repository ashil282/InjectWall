"""Command-line interface."""
import argparse
import json
import sys
from .runner import run

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="injectwall",
        description="Run safe, deterministic prompt-injection fixtures locally."
    )
    parser.add_argument("--cases", help="Optional path to a JSON fixture file")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        report = run(args.cases)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"injectwall: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("InjectWall | local prompt-injection checks")
        print("=" * 46)
        for item in report["results"]:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"[{status}] {item['id']:<18} {item['category']:<9} "
                  f"expected={item['expected']:<11} observed={item['observed']}")
            print(f"       {item['rationale']}")
        print("-" * 46)
        print(f"Total: {report['total']}  Passed: {report['passed']}  Failed: {report['failed']}")
    return 0 if report["failed"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
