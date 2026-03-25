<div align="center">

# uSkills

**Agent 标准化技能底座**

以驾驭工程为方法论，将历史 SOP Prompt 批量转换为可驾驭、可复用、可调用、可迭代的标准化 Skills。

[![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square)](https://github.com/zhubao315/uSkills/actions)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)](https://github.com/zhubao315/uSkills/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/zhubao315/uSkills/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Docs](https://img.shields.io/badge/Docs-Published-00C2CB?style=flat-square)](https://zhubao315.github.io/uSkills/)

[快速开始](#快速开始) • [文档](https://zhubao315.github.io/uSkills/) • [贡献指南](CONTRIBUTING.md)

</div>

---

## 核心价值

| 特性 | 描述 |
|:---:|:---|
| 🎯 **可驾驭** | 技能定义、执行、结果、迭代全生命周期可控 |
| ♻️ **可复用** | 将零散 Prompt 沉淀为跨项目复用的技能资产 |
| 🔌 **可调用** | 提供统一 Schema、CLI 与 Python 接口 |
| 🔄 **可迭代** | 借助 Git + CI + 测试 + Pages 形成闭环 |
| 💡 **零成本开源** | 代码、文档、技能、发布全部托管在 GitHub |

## SOP 转换流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   SOP 文本      │────▶│   转换引擎      │────▶│   标准化 Skills │
│  (Prompt)       │     │  (Converter)    │     │  (YAML/JSON)    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
   原始步骤              步骤提取 & 拆分           Schema 验证
   非结构化              标准化处理               版本化管理
```

## 项目结构

```
uSkills/
├── core/               # 核心模块
│   └── uskills/        # Schema、验证器、转换器、索引器
├── cli/                # 命令行工具
├── adapters/           # 第三方适配器 (LangChain 等)
├── skills/             # 技能库
│   ├── atomic/         # 原子技能
│   ├── composite/      # 组合技能
│   ├── domain/         # 领域技能
│   ├── governance/     # 治理技能
│   └── imported/       # 导入的技能
├── docs/               # MkDocs 文档源文件
├── examples/           # 示例 SOP
├── tests/              # 测试用例
├── standards/          # Schema 标准文件
├── scripts/            # 辅助脚本
├── .github/            # GitHub Actions 配置
├── mkdocs.yml          # MkDocs 配置
├── pyproject.toml      # 项目配置
└── requirements.txt    # 依赖列表
```

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/zhubao315/uSkills.git
cd uSkills

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```bash
# 验证技能文件
python cli/uskills_cli.py validate skills/atomic/text_keyword_extract.yaml

# 转换 SOP 为技能
python cli/uskills_cli.py convert examples/customer_service_sop.md --output skills/generated

# 生成技能索引
python cli/uskills_cli.py index skills --output docs/generated/skills-index.md

# 导出 JSON Schema
python cli/uskills_cli.py schema --output standards/uskill.schema.json

# 查看技能统计
python cli/uskills_cli.py stats skills/
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_converter.py

# 带详细输出
pytest -v
```

## 技能示例

```yaml
skill_id: uskill-atomic-text-keyword-extract-v1-0-0
meta:
  name: 文本关键词提取
  version: "1.0.0"
  category: atomic
  domain: nlp
  description: 从输入文本中提取关键词，并返回结构化结果
  tags:
    - nlp
    - extract
    - atomic
input:
  params:
    - name: text
      type: string
      required: true
      description: 待提取关键词的原始文本
execute:
  prompt_template: |
    从{{text}}中提取 5 到 10 个最核心关键词。
    结果返回 JSON，包含 keywords 与 summary。
  steps:
    - 识别文本主题
    - 抽取高价值关键词
    - 去重并输出结构化结果
  temperature: 0.1
  model: gpt-4o-mini
output:
  format: json
  params:
    - keywords
    - summary
control:
  timeout: 10
  retry: 2
  interrupt: true
```

## 核心方法论

uSkills 基于"驾驭工程"推进 Agent 技能资产化：

1. **定义驾驭**：用标准 Schema 固化技能边界、约束和依赖
2. **过程驾驭**：为执行过程预留监控、干预、暂停、回滚能力
3. **结果驾驭**：输出结构校验与治理规则前置
4. **迭代驾驭**：执行数据回流，驱动版本化进化

## V1.0 能力

- [x] 历史 SOP 文本导入与原子步骤拆分
- [x] uSkill Pydantic V2 标准模型与 JSON Schema 导出
- [x] YAML/JSON 技能校验
- [x] 技能目录索引生成
- [x] MkDocs Material 项目文档站点
- [x] GitHub Actions 自动测试与 Pages 发布

## 开发

```bash
# 代码检查
ruff check .

# 类型检查
mypy core/

# 运行测试
pytest

# 构建文档
mkdocs build
```

## 文档

完整文档请访问：[https://zhubao315.github.io/uSkills/](https://zhubao315.github.io/uSkills/)

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**[文档](https://zhubao315.github.io/uSkills/)** • **[GitHub](https://github.com/zhubao315/uSkills)** • **[Issues](https://github.com/zhubao315/uSkills/issues)**

Made with ❤️ by [zhubao315](https://github.com/zhubao315)

</div>
