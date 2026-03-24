from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.uskills.converter import convert_sop_file  # noqa: E402

EXCLUDED_NAMES = {
    "SOP索引.md",
    "SOP模板.md",
    "SOP分类.md",
    "SOP（标准作业程序）.md",
    "Claude_Skill_IM报告撰写专家.md",
}


def should_import(path: Path) -> bool:
    if path.name in EXCLUDED_NAMES:
        return False
    if path.suffix.lower() != ".md":
        return False
    return path.name.startswith("SOP-") or path.name == "my_sop.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("--output", default="skills/imported")
    args = parser.parse_args()

    source_root = Path(args.source)
    output_root = PROJECT_ROOT / args.output
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in source_root.rglob("*.md") if should_import(path))
    total_skills = 0
    for path in files:
        written = convert_sop_file(path, output_root)
        total_skills += len(written)
        print(f"{path.name}: {len(written)} skills")

    print(f"imported {len(files)} SOP files into {total_skills} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
