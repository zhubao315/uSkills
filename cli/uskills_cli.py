"""uSkills CLI Tool.

Command-line interface for uSkills operations including:
- Skill file validation
- SOP to Skill conversion
- JSON Schema export
- Skills index generation
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.uskills.converter import ConversionError, convert_sop_file  # noqa: E402
from core.uskills.indexer import build_skills_index, get_skill_stats  # noqa: E402
from core.uskills.schema import exported_json_schema, get_schema_version  # noqa: E402
from core.uskills.validator import validate_directory, validate_skill_file  # noqa: E402

# Version information
__version__ = "1.1.0"


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate skill file(s).

    Args:
        args: Parsed command arguments.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    path = Path(args.path)

    if path.is_dir():
        results = validate_directory(path, recursive=args.recursive)
        failed = 0
        for file_path, (ok, message) in sorted(results.items()):
            status = "✓" if ok else "✗"
            print(f"{status} {file_path}: {message}")
            if not ok:
                failed += 1

        total = len(results)
        passed = total - failed
        print(f"\n{passed}/{total} files valid")
        return 0 if failed == 0 else 1
    else:
        ok, message = validate_skill_file(path)
        status = "✓" if ok else "✗"
        print(f"{status} {path}: {message}")
        return 0 if ok else 1


def cmd_convert(args: argparse.Namespace) -> int:
    """Convert SOP file to uSkill files.

    Args:
        args: Parsed command arguments.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    try:
        written = convert_sop_file(
            args.path,
            args.output,
            domain=args.domain,
            owner=args.owner,
        )
        print(f"Generated {len(written)} skills:")
        for item in written:
            print(f"  → {item}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ConversionError as e:
        print(f"Conversion error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


def cmd_schema(args: argparse.Namespace) -> int:
    """Export JSON Schema for uSkills.

    Args:
        args: Parsed command arguments.

    Returns:
        Exit code (0 for success).
    """
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)

    schema = exported_json_schema()
    schema_text = json.dumps(schema, ensure_ascii=False, indent=2)
    target.write_text(schema_text, encoding="utf-8")

    print(f"Schema v{get_schema_version()} exported to: {target}")
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    """Build skills index markdown file.

    Args:
        args: Parsed command arguments.

    Returns:
        Exit code (0 for success).
    """
    try:
        target = build_skills_index(args.path, args.output)

        # Print stats
        stats = get_skill_stats(args.path)
        print(f"Index generated: {target}")
        print(f"  Skills: {stats['total_skills']}")
        print(f"  Sources: {stats['total_sources']}")
        print(f"  Categories: {stats['categories']}")

        return 0
    except Exception as e:
        print(f"Error building index: {e}", file=sys.stderr)
        return 1


def cmd_stats(args: argparse.Namespace) -> int:
    """Show skill statistics.

    Args:
        args: Parsed command arguments.

    Returns:
        Exit code (0 for success).
    """
    try:
        stats = get_skill_stats(args.path)
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(f"Error getting stats: {e}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="uskills",
        description="uSkills - Agent skill foundation for controllable execution.",
        epilog="For more information, visit: https://zhubao315.github.io/uSkills/",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Validate command
    validate = subparsers.add_parser(
        "validate",
        help="Validate uSkill YAML or JSON file(s).",
        description="Validate skill files against the uSkill schema.",
    )
    validate.add_argument(
        "path",
        help="Path to skill file or directory.",
    )
    validate.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=True,
        help="Search subdirectories recursively (default: True).",
    )
    validate.set_defaults(func=cmd_validate)

    # Convert command
    convert = subparsers.add_parser(
        "convert",
        help="Convert a SOP text file into atomic skills.",
        description="Parse SOP text and generate standardized uSkill definitions.",
    )
    convert.add_argument(
        "path",
        help="Path to SOP text file.",
    )
    convert.add_argument(
        "--output",
        default="skills/generated",
        help="Output directory for generated skills (default: skills/generated).",
    )
    convert.add_argument(
        "--domain",
        default="general",
        help="Skill domain category (default: general).",
    )
    convert.add_argument(
        "--owner",
        default="uSkills",
        help="Skill owner name (default: uSkills).",
    )
    convert.set_defaults(func=cmd_convert)

    # Schema command
    schema = subparsers.add_parser(
        "schema",
        help="Export the JSON schema for uSkills.",
        description="Export the USkill JSON Schema definition.",
    )
    schema.add_argument(
        "--output",
        default="standards/uskill.schema.json",
        help="Output path for JSON schema (default: standards/uskill.schema.json).",
    )
    schema.set_defaults(func=cmd_schema)

    # Index command
    index_cmd = subparsers.add_parser(
        "index",
        help="Build the markdown skills index.",
        description="Generate a markdown index of all skills in a directory.",
    )
    index_cmd.add_argument(
        "path",
        help="Path to skills directory.",
    )
    index_cmd.add_argument(
        "--output",
        default="docs/generated/skills-index.md",
        help="Output path for index file (default: docs/generated/skills-index.md).",
    )
    index_cmd.set_defaults(func=cmd_index)

    # Stats command
    stats_cmd = subparsers.add_parser(
        "stats",
        help="Show skill statistics.",
        description="Display statistics about skills in a directory.",
    )
    stats_cmd.add_argument(
        "path",
        help="Path to skills directory.",
    )
    stats_cmd.set_defaults(func=cmd_stats)

    return parser


def main() -> int:
    """Main entry point.

    Returns:
        Exit code.
    """
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
