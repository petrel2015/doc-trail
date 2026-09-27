# 使用说明

## 调用

可分发的 Skill 位于 `skills/doctrail/`，应一起保留 references、assets 和 scripts。支持本地 Skill 的宿主可按自身安装方式载入该目录。Codex 的个人 Skill 通常位于 `~/.agents/skills/doctrail/`；已有安装应先比较，不直接覆盖。参见 [Codex 官方说明](https://developers.openai.com/codex/skills/)。

本项目尚未验证宿主自动激活。也可以直接要求 Agent 阅读仓库中的 Skill 入口；读取源文件不等于自动发现已验证。

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
