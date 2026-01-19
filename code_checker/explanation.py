def explain_grade(score):
    if score >= 90:
        return (
            "Excellent code quality. The codebase is clean, readable, and shows "
            "strong maintainability with minimal risk indicators."
        )
    elif score >= 80:
        return (
            "Good overall quality with a few minor issues. Cleaning up warnings "
            "and improving consistency would raise the quality further."
        )
    elif score >= 70:
        return (
            "Moderate quality. The code works but shows maintainability concerns. "
            "Refactoring and cleanup are recommended."
        )
    elif score >= 50:
        return (
            "Low quality. Multiple structural or security-related issues were "
            "detected and should be addressed soon."
        )
    else:
        return (
            "Poor code quality. High risk of bugs, security vulnerabilities, and "
            "long-term maintenance problems. Immediate improvements are required."
        )


def suggest_improvements(findings):
    suggestions = set()

    for severity, _, message in findings:
        msg = message.lower()

        if "large" in msg:
            suggestions.add("Split large files into smaller, focused modules.")

        if "long line" in msg:
            suggestions.add("Limit line length to improve readability.")

        if "todo" in msg or "fixme" in msg:
            suggestions.add("Resolve TODO/FIXME comments or track them properly.")

        if "secret" in msg:
            suggestions.add(
                "Remove hardcoded secrets and use environment variables or secure vaults."
            )

        if severity == "warning":
            suggestions.add("Address warnings to improve code maintainability.")

        if severity == "error":
            suggestions.add("Fix critical issues immediately to reduce risk.")

    if not suggestions:
        suggestions.add(
            "No major improvements required. Maintain current coding standards."
        )

    return sorted(suggestions)
