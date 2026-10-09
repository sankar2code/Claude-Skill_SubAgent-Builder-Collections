#!/usr/bin/env python3
"""Check that every strategy output file ends with a complete handoff block,
and that the decision log records the gates.

A handoff block is a '## Handoff' section with these fields (one per line,
'- Field: value'):
  Role, Status, As-of, Inputs, Output, Labels, Contradictions, Open issues,
  Checks, Next, Human approval

Status must be draft, challenged or approved.

Usage:
    python handoff_lint.py strategy-output/
Standard library only.
"""
import os
import re
import sys

FIELDS = ["Role", "Status", "As-of", "Inputs", "Output", "Labels", "Contradictions",
          "Open issues", "Checks", "Next", "Human approval"]
STATUSES = {"draft", "challenged", "approved"}
FIELD_RE = re.compile(r"^\s*[-*]\s*\**([A-Za-z \-/]+?)\**\s*:\s*(.*)$")


def handoff_section(text):
    m = re.search(r"^##\s+Handoff\s*$", text, re.M | re.I)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    folder = sys.argv[1]
    bad = 0
    files = sorted(f for f in os.listdir(folder) if f.endswith(".md") and f != "decision-log.md")
    for fn in files:
        sec = handoff_section(open(os.path.join(folder, fn)).read())
        issues = []
        if sec is None:
            issues.append("no '## Handoff' section")
        else:
            found = {}
            for line in sec.splitlines():
                m = FIELD_RE.match(line)
                if m:
                    found[m.group(1).strip().lower()] = m.group(2).strip()
            for f in FIELDS:
                v = found.get(f.lower())
                if v is None:
                    issues.append(f"missing field '{f}'")
                elif not v:
                    issues.append(f"empty field '{f}'")
            st = (found.get("status") or "").lower().split()[0] if found.get("status") else ""
            if st and st not in STATUSES:
                issues.append(f"status '{found.get('status')}' is not draft | challenged | approved")
        if issues:
            bad += 1
            print(f"FAIL {fn}")
            for i in issues:
                print(f"     - {i}")
        else:
            print(f"ok   {fn}")

    log = os.path.join(folder, "decision-log.md")
    if os.path.exists(log):
        t = open(log).read()
        gates = re.findall(r"^\|\s*Gate\s*([123])\s*\|([^|]*)\|([^|]*)\|", t, re.M | re.I)
        passed = [g for g, who, when in gates if who.strip() and who.strip() not in ("-", "")]
        print(f"\nDecision log: gates recorded with an approver: {', '.join(sorted(set(passed))) or 'none'}")
    else:
        print("\nNo decision-log.md found. Create it from assets/templates/decision-log.md.")

    print()
    if bad:
        print(f"RESULT: FAIL ({bad} of {len(files)} files)")
        sys.exit(1)
    print(f"RESULT: PASS ({len(files)} files)")


if __name__ == "__main__":
    main()
