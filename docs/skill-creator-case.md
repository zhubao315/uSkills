# skill-creator 驾驭示例

本页以当前本地最新版 `skill-creator` 为样例，展示 uSkills 如何把一个可调用技能纳入“可控、可测、可复现、可干预、可进化”的治理框架。

## 样例对象

`skill-creator` 的核心职责是创建或更新技能，并明确要求：

- 保持上下文精简
- 根据任务脆弱度设置合适自由度
- 保护验证独立性
- 通过 `SKILL.md`、`references/`、`scripts/` 实现渐进加载
- 按“理解 -> 规划 -> 初始化 -> 编辑 -> 验证 -> 迭代”流程工作

## 一、定义驾驭

将 `skill-creator` 从“会用”变成“可驾驭”，第一步不是调用它，而是先定义边界：

- 输入：技能目标、约束、验证证据要求
- 过程：允许加载哪些文件，何时进入 `references/` 或 `scripts/`
- 输出：治理计划、执行轨迹、验证摘要、下一轮迭代建议
- 控制：超时、重试、中断、回滚、人工复核

对应的标准化技能文件见：`skills/domain/skill_creator_governance_demo.yaml`

## 二、过程驾驭

对 `skill-creator` 的过程控制，重点不是替它思考，而是限制它在正确边界内运行：

1. 先确认本次是“创建技能”还是“更新技能”
2. 只读取与当前任务直接相关的 `SKILL.md` 片段
3. 当技能存在多变体或内容过长时，拆到 `references/`
4. 对高风险、低容错流程，优先转为脚本化执行
5. 全程记录读取了哪些资源、执行了哪些校验

## 三、结果驾驭

使用 `skill-creator` 时，输出不能只看“写出了文件”，还要检查：

- 技能结构是否完整
- `SKILL.md` 是否遵守简洁原则
- 是否把变体细节下沉到 `references/`
- 是否给出了真实验证证据，而不是主观说明
- 是否留下失败模式与回滚路径

## 四、迭代驾驭

`skill-creator` 特别强调验证独立性。uSkills 将这一点落成迭代规则：

- 验证时只提供最小任务上下文
- 不向验证环节泄露预期答案、怀疑点和预设修复方案
- 优先保留原始证据：日志、diff、样例输出、失败轨迹
- 用这些证据驱动技能下一轮优化，而不是凭感觉修改

## 五、命令示例

```bash
python cli/uskills_cli.py validate skills/domain/skill_creator_governance_demo.yaml
python cli/uskills_cli.py index skills --output docs/generated/skills-index.md
```

## 六、发布结果

本次示例已作为 `uSkills` 仓库中的公开案例提交，并通过 GitHub Actions 自动发布到 Pages。
