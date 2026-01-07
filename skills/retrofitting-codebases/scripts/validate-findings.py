#!/usr/bin/env python3
"""
Validates archaeology findings against actual code.
Checks that all file:line references in findings actually exist.

Usage: python scripts/validate-findings.py <findings.md>
"""

import sys
import os
import re


def validate_file_references(findings_path: str) -> list[str]:
    """Check that all file:line references in findings actually exist."""
    errors = []
    warnings = []

    if not os.path.exists(findings_path):
        return [f"Findings file not found: {findings_path}"]

    with open(findings_path, encoding="utf-8") as f:
        content = f.read()

    # Find patterns like "src/foo.cs:42" or "path/to/file.py:123"
    # Matches common extensions: .cs, .py, .ts, .js, .java, .go, .rb, .rs
    refs = re.findall(
        r"[`]?(\S+\.(?:cs|py|ts|js|tsx|jsx|java|go|rb|rs|php|cpp|c|h)):(\d+)[`]?",
        content,
    )

    checked_files = set()

    for filepath, line in refs:
        # Clean up the filepath (remove backticks, quotes)
        filepath = filepath.strip("`'\"")

        # Check if file exists
        if not os.path.exists(filepath):
            # Try relative to current directory
            if not os.path.exists(filepath):
                errors.append(f"File not found: {filepath}:{line}")
                continue

        # Check if line number is valid
        if filepath not in checked_files:
            try:
                with open(filepath, encoding="utf-8") as f:
                    lines = f.readlines()
                    line_count = len(lines)
                    checked_files.add(filepath)

                    if int(line) > line_count:
                        errors.append(
                            f"Line {line} out of range in {filepath} (file has {line_count} lines)"
                        )
                    elif int(line) < 1:
                        errors.append(f"Invalid line number {line} in {filepath}")
            except Exception as e:
                warnings.append(f"Could not read {filepath}: {e}")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate-findings.py <findings.md>")
        print("")
        print("Validates that all file:line references in the findings file")
        print("point to actual files and valid line numbers.")
        sys.exit(1)

    findings_path = sys.argv[1]
    result = validate_file_references(findings_path)

    # Handle both old (list) and new (tuple) return format
    if isinstance(result, tuple):
        errors, warnings = result
    else:
        errors = result
        warnings = []

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
        print("")

    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"All file references in {findings_path} are valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
