from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.uskills.converter import convert_sop_file  # noqa: E402
from core.uskills.indexer import build_skills_index  # noqa: E402
from core.uskills.schema import exported_json_schema  # noqa: E402
from core.uskills.validator import validate_skill_file  # noqa: E402


def cmd_validate(args: argparse.Namespace) -> int:
    ok, message = validate_skill_file(args.path)
    print(message)
    return 0 if ok else 1


def cmd_convert(args: argparse.Namespace) -> int:
    written = convert_sop_file(args.path, args.output)
    print(f"generated {len(written)} skills")
    for item in written:
        print(item)
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    schema_text = json.dumps(exported_json_schema(), ensure_ascii=False, indent=2)
    target.write_text(schema_text, encoding="utf-8")
    print(target)
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    target = build_skills_index(args.path, args.output)
    print(target)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="uskills")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a uSkill YAML or JSON file.")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)

    convert = subparsers.add_parser("convert", help="Convert a SOP text file into atomic skills.")
    convert.add_argument("path")
    convert.add_argument("--output", default="skills/generated")
    convert.set_defaults(func=cmd_convert)

    schema = subparsers.add_parser("schema", help="Export the JSON schema for uSkills.")
    schema.add_argument("--output", default="standards/uskill.schema.json")
    schema.set_defaults(func=cmd_schema)

    index_cmd = subparsers.add_parser("index", help="Build the markdown skills index.")
    index_cmd.add_argument("path")
    index_cmd.add_argument("--output", default="docs/generated/skills-index.md")
    index_cmd.set_defaults(func=cmd_index)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
