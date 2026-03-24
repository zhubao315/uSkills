# Contributing

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Required checks

```bash
python cli/uskills_cli.py schema
python cli/uskills_cli.py index skills --output docs/generated/skills-index.md
ruff check .
pytest
mkdocs build --strict
```

## Contribution rules

1. 新技能必须保留 `source` 溯源字段。
2. 变更技能时同步更新文档和索引。
3. 破坏性 Schema 变更必须在 PR 中明确说明。
