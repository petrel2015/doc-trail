# Usage

## Invocation

The distributable skill folder is `skills/doctrail/`; preserve its references, assets and scripts together. A host with local skill discovery can install this folder using its supported installation mechanism. For Codex, the personal skill location is normally `~/.agents/skills/doctrail/`. Do not overwrite an existing installation without comparing it. See [official skill documentation](https://developers.openai.com/codex/skills/).

Host activation has not been tested here. A portable alternative is to ask an agent to read the repository's skill entry explicitly. Reading skill source is not proof of automatic discovery.

Example requests:

- “Read DocTrail and initialize this project's docs. Preserve existing content, inspect relevant Git history, and mark unknown reasons.”
- “Use DocTrail to document this A-to-B reversal, its evidence and the conditions for reconsidering A.”
- “Audit the documentation only; report broken navigation and unsupported historical claims without editing.”

## Helpers

From this repository root:

```sh
python3 skills/doctrail/scripts/doctrail.py inventory . --limit 100
python3 skills/doctrail/scripts/doctrail.py history . --limit 20 --path skills/doctrail
python3 skills/doctrail/scripts/doctrail.py check .
```

For another project, replace `.` with its path while keeping the script path resolvable. Read the [helper contract](../../skills/doctrail/references/tools.md) before relying on check results.

Initialization is a guided workflow: inventory, disposition map, targeted history, factual writing, link/relationship checks and a gaps report. It does not automatically create or overwrite documents. Repeated runs maintain existing paths and records.

## Limits and troubleshooting

A missing/empty Git history returns an error for `history`; `inventory` still works. Shallow history and truncated results are labeled. Checks ignore remote URLs and do not verify anchors or prose truth. A missing decision index means relationships need manual review, not that every decision passed validation.

No dependency installation, deployment, model usage or publishing is performed by the helper. Its stdout may expose repository filenames or commit subjects: inspect and sanitize before sharing. No web deployment or screenshots apply to this text skill. Follow your project's authorization when an agent executes documented project commands.
