# Maintain documentation during development

Before proposing a replacement for a significant implementation, follow its topic/architecture links and search the decision index. Read only matching records, including superseded predecessors when they explain the current choice. If evidence is missing, report that absence; do not interpret it as approval or as a permanent prohibition.

After a change, inspect its actual diff and verification evidence:

| Change | Documentation impact |
| --- | --- |
| Observable behavior, configuration or interface | Current usage/reference and relevant entry links |
| Significant new capability | Topic guide; README only if important for discovery |
| Tried approach rejected or reverted | Decision/evaluation record, evidence and reconsideration conditions |
| Decision superseded | New record linked to the old; retain old rationale and update current topic index |
| Small internal refactor | Usually no new decision; update existing explanation only if now inaccurate |
| Historical claim corrected | Add an explicit correction with evidence, preserving the prior decision's historical meaning |

Keep rejected-without-testing distinct from tested-and-failed. Keep failure of an implementation distinct from impossibility of an approach. Significant experiments can deserve a record even without a merged code change.

For a reversal, ask: what changed since the previous choice, what failure was observed, why does the replacement address it, what tradeoff remains, and what would justify trying again? These are writing prompts, not mandatory user questions. Derive answers from evidence; leave unknown fields explicit.

Do not rewrite historical records into a retrospective success story. Update status/correction links; explain a changed decision in its successor. Prefer a regression test for a deterministic failure when code changes are in scope. Documentation maintenance alone does not authorize implementing tests or changing behavior.

Finish with focused local checks and a statement of outstanding semantic or runtime validation. Avoid rereading all history or regenerating every guide for an ordinary change.
