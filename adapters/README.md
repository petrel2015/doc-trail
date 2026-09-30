# Optional product adapters / 可选产品适配

The portable distribution is [skills/doctrail](../skills/doctrail/SKILL.md). Product adapters add presentation metadata or loading instructions for a particular host; they do not define DocTrail's workflow or establish tested compatibility.

可移植发行内容是 [skills/doctrail](../skills/doctrail/SKILL.md)。适配文件仅补充特定宿主的界面元数据或加载说明，不定义核心流程，也不代表兼容性已经实测。

## Codex presentation metadata

[openai.yaml](codex/openai.yaml) preserves the initial optional display name, description and example prompt. A host that supports this format may use it as `agents/openai.yaml` inside its installed skill copy, according to that host's own mechanism. The `$doctrail` prompt syntax belongs to this adapter only. Reading the core skill requires no adapter. Metadata parsing and host activation are separate checks; activation has not been verified.

[openai.yaml](codex/openai.yaml) 保留原有可选名称、描述和示例提示词。支持该格式的宿主可按自身机制放入安装副本的 `agents/openai.yaml`。`$doctrail` 语法仅属于此适配，不是通用调用要求。核心读取无需适配；元数据解析和宿主激活需要分别验证，激活尚未实测。

Additional adapters can be contributed with host-specific evidence and a clear capability boundary. Claude, ZCode, DSH and Hermes do not need placeholder adapters to use the direct-reading workflow; no product-specific native registration claim is made here.
