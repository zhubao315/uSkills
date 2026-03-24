# 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python cli/uskills_cli.py schema
python cli/uskills_cli.py validate skills/atomic/text_keyword_extract.yaml
python cli/uskills_cli.py convert examples/customer_service_sop.md --output skills/generated
python cli/uskills_cli.py index skills --output docs/generated/skills-index.md
mkdocs serve
```

## 典型流程

1. 导入历史 SOP 文本
2. 执行 `convert` 生成原子技能
3. 人工微调 YAML 元数据
4. 执行 `validate` 校验
5. 更新技能索引并提交 PR
