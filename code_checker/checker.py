import os
from tqdm import tqdm
from languages import LANGUAGE_MAP
from rules import analyze_file

SKIP_DIRS = {".git", "node_modules", "build", ".dart_tool", "__pycache__"}

def collect_files(root):
    collected = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1] in LANGUAGE_MAP:
                collected.append(os.path.join(base, f))
    return collected

def main(path):
    files = collect_files(path)
    score = 100
    findings = []

    for file in tqdm(files, desc="Analyzing code", unit="file"):
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue

        issues, penalty = analyze_file(content)
        score -= penalty

        for sev, msg in issues:
            findings.append((sev, file, msg))

    score = max(0, score)
    grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 50 else "F"

    print(f"\nScore: {score}/100")
    print(f"Grade: {grade}")
    print(f"Issues found: {len(findings)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python checker.py <project_path>")
    else:
        main(sys.argv[1])
