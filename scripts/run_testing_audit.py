"""
Generate a testing audit report for the README Testing section.
The script captures environment info, project snapshots, and Django checks.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = BASE_DIR / "documentation" / "testing" / "testing-audit.md"


def run_cmd(command: Iterable[str]) -> tuple[int, str]:
    """
    Run a shell command and return (returncode, combined_output).
    Output includes stdout and stderr.
    """
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=BASE_DIR,
    )
    combined = (result.stdout or "") + (result.stderr or "")
    return result.returncode, combined.strip()


def format_section(title: str, content: str) -> str:
    """Format a markdown section with a title and body."""
    body = content.strip() if content.strip() else "No output."
    return f"## {title}\n\n{body}\n\n"


def collect_tree_snapshot(paths: list[Path]) -> str:
    """
    Build a simple tree snapshot for selected paths.
    Each line shows a relative path from BASE_DIR.
    """
    lines: list[str] = []
    for root_path in paths:
        if not root_path.exists():
            lines.append(f"{root_path.name} (missing)")
            continue
        for item in sorted(root_path.rglob("*")):
            rel = item.relative_to(BASE_DIR)
            marker = "/" if item.is_dir() else ""
            lines.append(str(rel) + marker)
    return "\n".join(lines)


def safe_json(output: str) -> str:
    """Return output or note if empty."""
    return output if output else "No output."


def main() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    python_version = sys.version.replace("\n", " ")

    env_info = f"- Generated: {now}\n- Python: {python_version}"

    pip_rc, pip_output = run_cmd([sys.executable, "-m", "pip", "freeze"])
    pip_section = pip_output or f"pip freeze failed (exit {pip_rc})."

    snapshot = collect_tree_snapshot(
        [
            BASE_DIR / "accounts",
            BASE_DIR / "training",
            BASE_DIR / "templates",
            BASE_DIR / "static",
            BASE_DIR / "documentation",
        ]
    )

    checks = [
        ("python manage.py check", ["python", "manage.py", "check"]),
        ("python manage.py check --deploy", ["python", "manage.py", "check", "--deploy"]),
        ("python manage.py makemigrations --check --dry-run", ["python", "manage.py", "makemigrations", "--check", "--dry-run"]),
        ("python manage.py showmigrations", ["python", "manage.py", "showmigrations"]),
    ]

    check_outputs: list[str] = []
    for title, cmd in checks:
        rc, out = run_cmd(cmd)
        header = f"### {title}"
        if rc != 0:
            check_outputs.append(f"{header}\n\nExit code: {rc}\n{out}\n")
        else:
            check_outputs.append(f"{header}\n\n{out}\n")

    # Placeholders for linting and tests
    lint_placeholder = (
        "Not run in this script. Suggested command:\n"
        "`python -m flake8`\n"
    )
    tests_placeholder = (
        "Not run in this script. Suggested command:\n"
        "`python manage.py test`\n"
    )

    report_parts = [
        "# Testing audit\n\n",
        format_section("Audit summary", "Pending manual summary."),
        format_section("Environment", env_info),
        format_section("Project structure", snapshot),
        format_section("Django checks", "\n".join(check_outputs)),
        format_section("Migrations status", "See makemigrations and showmigrations above."),
        format_section("Linting", lint_placeholder),
        format_section("Automated tests", tests_placeholder),
        format_section("Packages", pip_section),
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("".join(report_parts))


if __name__ == "__main__":
    main()
