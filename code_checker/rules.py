import re

def analyze_file(content):
    issues = []
    penalty = 0
    lines = content.splitlines()

    if len(lines) > 500:
        issues.append(("warning", "File is very large (>500 lines)"))
        penalty += 5

    if len(lines) < 5:
        issues.append(("info", "File is suspiciously small"))
        penalty += 1

    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            issues.append(("warning", f"Long line at {i} (>120 characters)"))
            penalty += 1

        if re.search(r"\b(TODO|FIXME|HACK)\b", line):
            issues.append(("info", f"TODO/FIXME comment at line {i}"))
            penalty += 1

        if re.search(r"(api_key|secret|token|password)\s*=\s*['\"]", line, re.I):
            issues.append(("error", f"Possible hardcoded secret at line {i}"))
            penalty += 10

    return issues, penalty
