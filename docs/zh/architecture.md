# 架构

DocTrail 提供已有项目整改与开发中持续维护两个入口，共同区分当前事实与历史选择。

轻量 Skill 入口按需链接不同工作流，模板仅服务重要决策，不强制固定页数。Python 标准库脚本负责确定性盘点、有界 HEAD 历史检索和本地结构检查，不修改目标项目、不调用模型；Agent 负责语义理解和文档编辑。

可选 JSON 决策索引承载机器检查所用的生命周期，Markdown 承载理由与阅读导航。已有 ADR／OpenSpec 目录可以保留；没有索引时，应明确关系检查由人工完成。文件目标存在不等于文档符合实现。

任务合同、派工、重试、成本与交接归编排器，见[集成边界](../../skills/doctrail/references/integration.md)。DocTrail 可独立使用，不依赖 AgentRelay。

调整上述职责前阅读 [D-0001](../decisions/D-0001-scope.md)。当前未实现自动模型评测或语义真实性验证。

可移植核心位于 `skills/doctrail/`，文件访问和可选命令执行能力由宿主提供。产品界面元数据独立放在[适配目录](../../adapters/README.md)，不改变核心流程要求。增加产品依赖前阅读 [D-0002](../decisions/D-0002-host-neutral.md)。
