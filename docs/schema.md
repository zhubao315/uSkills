# uSkill Schema

`USkill` 是统一技能格式，核心字段包括：

- `skill_id`：技能唯一标识
- `meta`：名称、版本、分类、领域、标签、所有者
- `input`：输入参数定义
- `execute`：Prompt 模板、执行步骤、模型与工具策略
- `output`：输出格式与校验规则
- `control`：超时、重试、中断、断点和 Mock 能力
- `source`：SOP 来源与步骤溯源

JSON Schema 文件位于 `standards/uskill.schema.json`。
