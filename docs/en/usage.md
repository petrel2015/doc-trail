# Usage

## Invocation

DocTrail is an independent, host-neutral skill. Its core uses the directory layout described by the [Agent Skills specification](https://agentskills.io/specification): `SKILL.md`, references, assets and scripts. Model choice, accounts, tool names and installation locations belong to the host.

Choose the entry your environment supports:

1. **Direct reading:** make the complete `skills/doctrail/` directory accessible and ask the agent to read `skills/doctrail/SKILL.md`. Follow only the route relevant to the task. Resolve resource links relative to the file containing them, and `<skill-dir>` relative to this skill's actual directory. This entry works without automatic skill discovery.
2. **Native registration:** copy or register the complete `skills/doctrail/` directory using the host's configured skill mechanism. Keep its name and internal paths intact. Compare any existing installation before replacing it; confirm the host exposes the entry before claiming activation. DocTrail does not prescribe a universal installation path or invocation syntax.

Claude, ZCode, DSH, Hermes, Codex and other agents are intended hosts when their tools provide the required capabilities. This is a capability-based design, not a claim that each product's native discovery or invocation has been tested. Use ordinary prompts for direct reading; host-specific selectors or commands are optional.

## Required capabilities

| Work | Capability |
| --- | --- |
| Read guidance / review supplied material | Read Markdown and follow the relevant local references |
| Initialize or maintain a repository's docs | Read project files; write only within the authorized documentation scope |
| Run deterministic helpers | Execute Python 3.10+; Git only for repository metadata/history |

The documentation workflow can run without the helpers. Use the host's equivalent inspection/checking tools or inspect supplied material, and report the actual coverage. If Git, files or command execution are unavailable, leave the corresponding evidence gap explicit.

Product-specific presentation metadata is available separately in [optional adapters](../../adapters/README.md). The core skill does not require it. Native host activation remains unverified.

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
