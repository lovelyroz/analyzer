from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "reply.md"
TOKENS = (
    "codal_excel_source_metadata",
    "Migration(9",
    "Migration(version=9",
    "version = 9",
    "version=9",
)

def git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return (result.stdout or result.stderr).strip()
    except Exception as exc:
        return f"GIT COMMAND ERROR: {exc}"

def source_files() -> list[Path]:
    roots = [ROOT / "src", ROOT / "tests"]
    found: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if any(part in {".venv", "__pycache__", ".pytest_cache"} for part in path.parts):
                continue
            found.append(path)
    return sorted(found)

def main() -> None:
    lines: list[str] = [
        "# Migration 9 local source reconciliation audit",
        "",
        "- Mode: read-only; no database access or mutation; no tests run.",
        f"- Repository: {ROOT}",
        "",
        "## Git identity",
        "",
        "HEAD:",
        git("rev-parse", "HEAD"),
        "",
        "Branch:",
        git("branch", "--show-current"),
        "",
        "## Working tree status",
        "",
        git("status", "--short") or "(clean)",
        "",
        "## Changed-file summary",
        "",
        git("diff", "--stat"),
        "",
        "## Staged-file summary",
        "",
        git("diff", "--cached", "--stat"),
        "",
        "## Migration 9 references in local Python source",
        "",
    ]

    matched = 0
    for path in source_files():
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        source_lines = text.splitlines()
        hit_indexes = [
            i for i, line in enumerate(source_lines)
            if any(token.lower() in line.lower() for token in TOKENS)
        ]
        if not hit_indexes:
            continue
        matched += 1
        lines.extend([f"### {path.relative_to(ROOT).as_posix()}", ""])
        emitted: set[int] = set()
        for index in hit_indexes:
            start = max(0, index - 12)
            end = min(len(source_lines), index + 21)
            for line_no in range(start, end):
                if line_no not in emitted:
                    lines.append(f"{line_no + 1}: {source_lines[line_no]}")
                    emitted.add(line_no)
            lines.append("")
    if matched == 0:
        lines.append("No Migration 9 token found in local Python files under src/ or tests/.")

    lines.extend([
        "",
        "## Migration directory files",
        "",
    ])
    migration_dir = ROOT / "src" / "migrations"
    if migration_dir.exists():
        for path in sorted(migration_dir.iterdir()):
            if path.is_file():
                lines.append(f"- {path.name} ({path.stat().st_size} bytes)")
    else:
        lines.append("src/migrations directory not found.")

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Migration 9 audit written to: {OUTPUT}")
    print(f"Python source files containing matching references: {matched}")
    print("No tests were run. No database was opened or modified.")

if __name__ == "__main__":
    main()
