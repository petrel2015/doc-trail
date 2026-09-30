# 使用说明

## 调用

DocTrail 是独立、宿主中立的 Skill。核心采用 [Agent Skills 规范](https://agentskills.io/specification)描述的目录布局：`SKILL.md`、references、assets 和 scripts。模型、账号、工具名称与安装位置由宿主决定。

按环境选择接入方式：

1. **直接读取**：让完整的 `skills/doctrail/` 目录可访问，要求 Agent 阅读 `skills/doctrail/SKILL.md`，再按任务加载相关参考资料。资源链接相对所在文件解析，`<skill-dir>` 指向本次实际载入的 Skill 目录。这种方式无需自动发现 Skill。
2. **宿主注册**：通过宿主配置的 Skill 机制复制或注册完整 `skills/doctrail/` 目录，保持名称与内部路径。已有安装先比较再替换；声称已激活前，应确认宿主确实暴露了入口。DocTrail 不规定通用安装路径或调用语法。

Claude、ZCode、DSH、Hermes、Codex 等均是目标宿主，前提是其工具具备对应能力。这是基于能力的设计，不代表各产品的原生发现与调用已经实测。直接读取时使用普通提示词即可，宿主专属选择器或命令为可选。

## 所需能力

| 工作 | 能力要求 |
| --- | --- |
| 阅读流程／审阅提供的材料 | 读取 Markdown 并按需访问本地参考资料 |
| 初始化或维护仓库文档 | 读取项目文件，在授权文档范围内写入 |
| 执行确定性辅助脚本 | Python 3.10+；只有 Git 元数据／历史需要 Git |

文档流程可不使用辅助脚本，改用宿主等价的检查工具或审阅提供的材料，并如实报告覆盖范围。缺少 Git、文件或执行能力时，明确对应证据缺口。

产品专属界面元数据另放在[可选适配](../../adapters/README.md)中，核心 Skill 无需它们。各宿主原生激活仍未验证。

请求示例：

- “阅读 DocTrail，初始化这个项目的文档，保留已有内容，检查相关 Git 历史，未知原因明确标注。”
- “用 DocTrail 记录这次从 A 回退为 B 的原因、证据及重新考虑 A 的条件。”
- “只审计文档，报告导航缺失与无依据的历史判断，不修改文件。”

## 辅助脚本

在本仓库根目录运行：

```sh
python3 skills/doctrail/scripts/doctrail.py inventory . --limit 100
python3 skills/doctrail/scripts/doctrail.py history . --limit 20 --path skills/doctrail
python3 skills/doctrail/scripts/doctrail.py check .
```

用于其他项目时，把 `.` 换成目标路径，同时确保脚本路径可访问。详细范围见[脚本约定](../../skills/doctrail/references/tools.md)。

初始化由 Agent 执行：盘点、文档处置映射、定向历史追溯、有依据的写作、链接与关系检查、缺口报告。脚本本身不创建或覆盖文档。重复执行应维护原有路径与记录。

## 边界与排错

无 Git 或没有提交时，history 报错，inventory 仍可运行。浅克隆和截断有明确标记。检查不访问远端、不验证锚点和正文真实性；没有决策索引时，关系校验需要人工完成。

脚本不安装依赖、不部署、不调用模型、不发布。输出可能包含私有文件名或提交说明，分享前应检查脱敏。这是文本 Skill，不需要网页部署或截图。Agent 验证项目命令时仍遵循项目授权范围。
