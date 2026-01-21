"""
Markdown Format Checker
Check markdown files for common formatting issues
"""

import sys
import re
from pathlib import Path


def check_markdown_syntax(file_path):
    """Check for basic markdown syntax issues"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues = []
    in_code_block = False
    code_block_start = 0

    for i, line in enumerate(lines, 1):
        # Check code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                in_code_block = False
            else:
                in_code_block = True
                code_block_start = i

        # Skip checks inside code blocks
        if in_code_block:
            continue

        # Check heading format
        if line.startswith('#'):
            if not line.startswith('# ') and len(line) > 1 and not line.startswith('##'):
                issues.append(f"Line {i}: Missing space after # in heading")

        # Check list format
        stripped = line.strip()
        if stripped.startswith(('-', '*', '+')) and not stripped.startswith('---'):
            # Make sure it's actually a list, not bold text or other markdown
            if len(stripped) > 1 and stripped[1:2] not in (' ', '-', '*', '+'):
                issues.append(f"Line {i}: Missing space after list marker")

        # Check trailing whitespace
        if line.rstrip() != line.rstrip('\n'):
            issues.append(f"Line {i}: Trailing whitespace")

    # Check unclosed code blocks
    if in_code_block:
        issues.append(f"Line {code_block_start}: Unclosed code block")

    return issues


def check_structure(file_path):
    """Check document structure"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Check heading hierarchy
    headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)

    prev_level = 0
    h1_count = 0
    
    for heading, text in headings:
        level = len(heading)

        # Count H1
        if level == 1:
            h1_count += 1

        # Check for skipped levels
        if level > prev_level + 1:
            issues.append(f"Heading '{text}': Skipped level (H{prev_level} → H{level})")

        prev_level = level

    # Check for multiple H1
    if h1_count > 1:
        issues.append(f"Multiple H1 headings found ({h1_count} total)")
    elif h1_count == 0:
        issues.append("No H1 heading found")

    return issues


def check_code_blocks(file_path):
    """Check code block formatting"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Find all code blocks
    code_blocks = re.findall(r'```(\w*)\n(.*?)```', content, re.DOTALL)

    for i, (lang, code) in enumerate(code_blocks, 1):
        if not lang:
            issues.append(f"Code block {i}: Missing language specification")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_markdown.py <markdown_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    print(f"📄 Checking: {file_path.name}\n")

    # Run checks
    syntax_issues = check_markdown_syntax(file_path)
    structure_issues = check_structure(file_path)
    code_issues = check_code_blocks(file_path)

    # Report results
    total_issues = len(syntax_issues) + len(structure_issues) + len(code_issues)

    if total_issues == 0:
        print("✓ No issues found!")
        sys.exit(0)

    print(f"⚠ Found {total_issues} issues:\n")

    if syntax_issues:
        print("## Syntax Issues:")
        for issue in syntax_issues[:10]:  # Limit to first 10
            print(f"  - {issue}")
        if len(syntax_issues) > 10:
            print(f"  ... and {len(syntax_issues) - 10} more")
        print()

    if structure_issues:
        print("## Structure Issues:")
        for issue in structure_issues:
            print(f"  - {issue}")
        print()

    if code_issues:
        print("## Code Block Issues:")
        for issue in code_issues[:10]:  # Limit to first 10
            print(f"  - {issue}")
        if len(code_issues) > 10:
            print(f"  ... and {len(code_issues) - 10} more")
        print()


if __name__ == "__main__":
    main()
