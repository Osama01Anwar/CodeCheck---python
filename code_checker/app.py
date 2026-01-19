import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from languages import LANGUAGE_MAP
from rules import analyze_file
from explanation import explain_grade, suggest_improvements

SKIP_DIRS = {".git", "node_modules", "build", ".dart_tool", "__pycache__"}
MAX_FILES = 800


class CodeCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Checker")
        self.root.geometry("900x600")

        self.files = []
        self.build_ui()

    def build_ui(self):
        top = tk.Frame(self.root)
        top.pack(pady=10)

        tk.Button(top, text="Select Code Folder", command=self.select_folder).pack(side=tk.LEFT, padx=10)
        tk.Button(top, text="Start Analysis", command=self.start_analysis).pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(self.root, length=600, mode="determinate")
        self.progress.pack(pady=15)

        self.status = tk.Label(self.root, text="Idle")
        self.status.pack()

        self.summary = tk.Label(self.root, text="", font=("Segoe UI", 12))
        self.summary.pack(pady=10)

        self.text = tk.Text(self.root, wrap=tk.NONE)
        self.text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def select_folder(self):
        path = filedialog.askdirectory()
        if not path:
            return

        self.files = self.collect_files(path)
        self.status.config(text=f"{len(self.files)} files ready for analysis")
        self.progress["value"] = 0

    def collect_files(self, root):
        collected = []
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if os.path.splitext(f)[1] in LANGUAGE_MAP:
                    collected.append(os.path.join(base, f))
                    if len(collected) >= MAX_FILES:
                        return collected
        return collected

    def start_analysis(self):
        if not self.files:
            messagebox.showwarning("No files", "Please select a folder first.")
            return

        self.text.delete("1.0", tk.END)
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        score = 100
        findings = []

        self.progress["maximum"] = len(self.files)

        for idx, file in enumerate(self.files, 1):
            self.status.config(text=f"Analyzing {os.path.basename(file)}")
            self.progress["value"] = idx

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

        explanation = explain_grade(score)
        improvements = suggest_improvements(findings)

        self.status.config(text="Analysis complete")
        self.summary.config(text=f"Score: {score}/100   Grade: {grade}   Issues: {len(findings)}")

        self.text.insert(tk.END, "=== GRADE EXPLANATION ===\n")
        self.text.insert(tk.END, explanation + "\n\n")

        self.text.insert(tk.END, "=== RECOMMENDED IMPROVEMENTS ===\n")
        for s in improvements:
            self.text.insert(tk.END, f"- {s}\n")

        self.text.insert(tk.END, "\n=== DETAILED FINDINGS ===\n\n")
        for sev, file, msg in findings:
            self.text.insert(tk.END, f"[{sev.upper()}] {file}\n  {msg}\n\n")


if __name__ == "__main__":
    root = tk.Tk()
    CodeCheckerApp(root)
    root.mainloop()
