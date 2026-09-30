# DocTrail · 文迹

[English](README.md) | 简体中文

独立、宿主中立的 Skill，提供渐进式项目文档与有据可查的决策历史。

从简短 README 出发，按任务沿链接深入。重新采用某个“更好”的方案前，先了解它是否已经试过、为何放弃或回退。

## 使用

让 Agent 阅读 [DocTrail Skill](skills/doctrail/SKILL.md)，然后选择：

- **初始化／整改**：整理已有文档，从代码和 Git 追溯重要历史。
- **持续维护**：更新受影响的指南，记录重要实验、选择与回退。

直接读取、宿主注册和能力要求见[使用说明](docs/zh/usage.md)。Claude、ZCode、DSH、Hermes、Codex 等均为目标宿主，原生激活分别验证。只有对应的可选辅助脚本需要 Python／Git，无第三方 Python 依赖。

## 按需阅读

- [文档导航](docs/zh/index.md)：使用、设计、校验与边界。
- [AI 入口](README_FOR_AI.md)：选择最小相关上下文。
- [决策索引](docs/decisions/README.md)：替换重要实现前了解历史。

当前为初始实现：Skill 流程及只读盘点、历史检索、结构检查。初始化由 Agent 执行，脚本不会自动编造项目事实。宿主激活和真实项目整改效果尚未完成资格验证，没有发布版本。

Agent 派工、运行状态、预算与交接由宿主编排器负责。DocTrail 不依赖 AgentRelay。仓库公开，暂未添加开源许可证。
