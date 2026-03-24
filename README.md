# uSkills

uSkills 是以驾驭工程为方法论的 Agent 标准化技能底座，用于将历史 SOP Prompt 批量转换为可驾驭、可复用、可调用、可迭代的标准化 Skills，并通过 GitHub 原生工作流完成治理、验证与发布。

## 核心价值

- 可驾驭：技能定义、执行、结果、迭代全生命周期可控
- 可复用：将零散 Prompt 沉淀为跨项目复用的技能资产
- 可调用：提供统一 Schema、CLI 与 Python 接口
- 可迭代：借助 Git + CI + 测试 + Pages 形成闭环
- 零成本开源：代码、文档、技能、发布全部托管在 GitHub

## 项目结构

```text
uSkills/
├── .github/
├── adapters/
├── cli/
├── core/
├── docs/
├── examples/
├── skills/
├── standards/
├── tests/
├── mkdocs.yml
├── pyproject.toml
└── requirements.txt
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python cli/uskills_cli.py validate skills/atomic/text_keyword_extract.yaml
python cli/uskills_cli.py convert examples/customer_service_sop.md --output skills/generated
python cli/uskills_cli.py index skills --output docs/generated/skills-index.md
pytest
```

## 示例案例

- 以最新版 `skill-creator` 为样例，展示如何将一个技能纳入定义驾驭、过程驾驭、结果驾驭与迭代驾驭闭环

## V1.0 能力

- 历史 SOP 文本导入与原子步骤拆分
- uSkill Pydantic V2 标准模型与 JSON Schema 导出
- YAML/JSON 技能校验
- 技能目录索引生成
- MkDocs Material 项目文档站点
- GitHub Actions 自动测试与 Pages 发布

## 核心方法论

uSkills 基于“驾驭工程”推进 Agent 技能资产化：

1. 定义驾驭：用标准 Schema 固化技能边界、约束和依赖
2. 过程驾驭：为执行过程预留监控、干预、暂停、回滚能力
3. 结果驾驭：输出结构校验与治理规则前置
4. 迭代驾驭：执行数据回流，驱动版本化进化

## 开发

```bash
ruff check .
pytest
mkdocs build
```

Pages 站点发布地址：

`https://zhubao315.github.io/uSkills/`
