# 贡献指南

感谢你对 uSkills 项目的关注！我们欢迎各种形式的贡献。

## 开发环境设置

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

# 安装开发依赖
pip install mypy
```

## 开发工作流

### 1. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 2. 进行修改

- 遵循现有代码风格
- 添加必要的测试
- 更新相关文档

### 3. 运行检查

```bash
# 生成 Schema 和索引
python cli/uskills_cli.py schema
python cli/uskills_cli.py index skills --output docs/generated/skills-index.md

# 代码检查
ruff check .

# 类型检查
mypy core/

# 运行测试
pytest

# 构建文档
mkdocs build --strict
```

### 4. 提交代码

```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request

在 GitHub 上创建 Pull Request，并填写相关信息。

## 代码规范

### Python 代码风格

- 使用 Ruff 进行代码格式化
- 遵循 PEP 8 规范
- 使用类型注解
- 编写清晰的文档字符串

### 提交信息格式

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

类型（type）：

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：

```
feat(converter): add batch conversion support
fix(validator): handle empty skill files
docs(readme): update installation guide
```

## 贡献技能

### 创建新技能

1. 在 `skills/` 目录下选择合适的分类：
   - `atomic/` - 原子技能（单一任务）
   - `composite/` - 组合技能（多个原子技能组合）
   - `domain/` - 领域特定技能
   - `governance/` - 治理相关技能

2. 创建 YAML 文件，遵循以下命名规范：
   ```
   uskill-{category}-{name}-{version}.yaml
   ```

3. 确保技能定义包含所有必要字段：
   ```yaml
   skill_id: uskill-atomic-your-skill-v1-1-0
   meta:
     name: 技能名称
     version: "1.1.0"
     category: atomic  # atomic, composite, domain, governance
     domain: general
     description: 技能描述
     tags: [tag1, tag2]
   input:
     params:
       - name: param_name
         type: string
         required: true
         description: 参数描述
   execute:
     prompt_template: "你的 Prompt 模板"
     steps:
       - 步骤 1
       - 步骤 2
     temperature: 0.1
     model: gpt-4o-mini
   output:
     format: json
     params: [result]
   control:
     timeout: 30
     retry: 1
   source:
     sop_name: 源 SOP 名称
     step_index: 1
     raw_step: 原始步骤内容
   ```

4. 验证技能文件：
   ```bash
   python cli/uskills_cli.py validate skills/your-category/your-skill.yaml
   ```

### 技能贡献规则

1. **必须保留 `source` 溯源字段**：便于追溯技能来源
2. **遵循命名规范**：确保 skill_id 格式正确
3. **验证通过**：提交前确保技能文件通过验证
4. **更新文档**：添加技能后更新相关文档和索引

## 报告问题

### Bug 报告

请使用 GitHub Issues 报告 Bug，并包含：

1. 问题描述
2. 复现步骤
3. 期望行为
4. 实际行为
5. 环境信息（Python 版本、操作系统等）
6. 相关日志或错误信息

### 功能请求

请使用 GitHub Issues 提交功能请求，并说明：

1. 功能描述
2. 使用场景
3. 期望的实现方式

## 行为准则

- 尊重所有参与者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 许可证

贡献即表示你同意你的贡献将在 MIT 许可证下发布。

## 联系方式

如有任何问题，请通过 GitHub Issues 联系我们。
