---
hide:
  - navigation
---

# uSkills

<div class="hero" markdown>

## Agent 标准化技能底座

以驾驭工程为方法论，将历史 SOP Prompt 批量转换为可驾驭、可复用、可调用、可迭代的标准化 Skills。

[:octicons-mark-github-16: GitHub](https://github.com/zhubao315/uSkills){ .md-button .md-button--primary }
[:octicons-rocket-16: 快速开始](quickstart.md){ .md-button .md-button--accent }

</div>

## 核心价值

<div class="grid" markdown>

<div class="card" markdown>

:material-cog-outline:{ .icon }

### 可驾驭

技能定义、执行、结果、迭代全生命周期可控。通过标准 Schema 固化技能边界、约束和依赖。

</div>

<div class="card" markdown>

:material-recycle-variant:{ .icon }

### 可复用

将零散 Prompt 沉淀为跨项目复用的技能资产。一次定义，多处使用。

</div>

<div class="card" markdown>

:material-api:{ .icon }

### 可调用

提供统一 Schema、CLI 与 Python 接口。支持 YAML/JSON 格式，易于集成。

</div>

<div class="card" markdown>

:material-git:{ .icon }

### 可迭代

借助 Git + CI + 测试 + Pages 形成闭环。执行数据回流，驱动版本化进化。

</div>

<div class="card" markdown>

:material-open-source-initiative:{ .icon }

### 零成本开源

代码、文档、技能、发布全部托管在 GitHub。100% 开源，社区驱动。

</div>

<div class="card" markdown>

:material-shield-check:{ .icon }

### 工程化治理

通过 GitHub 原生工作流完成协作、校验、发布。自动测试 + Pages 文档。

</div>

</div>

## V1.0 能力

<div class="grid" markdown>

<div class="card" markdown>

### SOP 转换

将历史 SOP 文本批量导入，自动拆分为原子步骤，生成标准化 Skills。

```bash
uskills convert sop.txt --output skills/
```

</div>

<div class="card" markdown>

### Schema 验证

基于 Pydantic V2 的类型安全验证，支持 YAML/JSON 格式，导出 JSON Schema。

```bash
uskills validate skills/
```

</div>

<div class="card" markdown>

### 索引生成

自动生成技能目录索引，支持分类统计和快速检索。

```bash
uskills index skills/ --output docs/index.md
```

</div>

</div>

## 核心方法论

uSkills 基于"驾驭工程"推进 Agent 技能资产化：

<div class="skill-graph hexagon-pattern" markdown>

1. **定义驾驭**：用标准 Schema 固化技能边界、约束和依赖
2. **过程驾驭**：为执行过程预留监控、干预、暂停、回滚能力
3. **结果驾驭**：输出结构校验与治理规则前置
4. **迭代驾驭**：执行数据回流，驱动版本化进化

</div>

## 快速体验

=== "安装"

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

=== "验证技能"

    ```bash
    # 验证单个技能文件
    python cli/uskills_cli.py validate skills/atomic/text_keyword_extract.yaml

    # 验证整个目录
    python cli/uskills_cli.py validate skills/
    ```

=== "转换 SOP"

    ```bash
    # 将 SOP 文本转换为技能
    python cli/uskills_cli.py convert examples/customer_service_sop.md

    # 指定输出目录
    python cli/uskills_cli.py convert sop.txt --output my_skills/
    ```

=== "生成索引"

    ```bash
    # 生成技能目录索引
    python cli/uskills_cli.py index skills/

    # 指定输出路径
    python cli/uskills_cli.py index skills/ --output docs/skills.md
    ```

## 技能示例

一个典型的 uSkill 定义（YAML 格式）：

```yaml title="text_keyword_extract.yaml"
skill_id: uskill-atomic-text-keyword-extract-v1-1-0
meta:
  name: 文本关键词提取
  version: "1.1.0"
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

## 社区

<div class="grid" markdown>

<div class="card" markdown>

:material-github:{ .icon }

### GitHub

访问我们的 GitHub 仓库，参与贡献和讨论。

[:octicons-arrow-right-16: 访问仓库](https://github.com/zhubao315/uSkills)

</div>

<div class="card" markdown>

:material-bug:{ .icon }

### 问题反馈

遇到问题？请在 GitHub Issues 中反馈。

[:octicons-arrow-right-16: 提交 Issue](https://github.com/zhubao315/uSkills/issues)

</div>

<div class="card" markdown>

:material-book-open:{ .icon }

### 文档

查看完整文档了解更多信息。

[:octicons-arrow-right-16: 阅读文档](quickstart.md)

</div>

</div>

---

<div style="text-align: center; color: var(--md-default-fg-color--lighter); padding: 2rem 0;">

Made with :material-heart:{ style="color: #FF8C00;" } by [zhubao315](https://github.com/zhubao315)

</div>
