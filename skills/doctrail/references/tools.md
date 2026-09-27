# Helper contract

Run `python3 <skill-dir>/scripts/doctrail.py COMMAND ROOT`. All commands print JSON. Exit 0 means the requested structural operation completed without detected errors; exit 2 means invalid input, missing history, or a detected check failure. Argparse usage errors are plain text. No command writes files or calls a model/network service.

| Command | Behavior |
| --- | --- |
| `inventory ROOT --limit 100` | Lists Markdown paths and top-level entries, bounded to 100 returned docs; reports total found and truncation; optional Git HEAD/shallow metadata |
| `history ROOT --limit 20 --path src/component` | Current HEAD ancestry, literal path selection; hashes, commit dates and subjects only; repeat --path for more paths |
| `check ROOT --decisions docs/decisions/index.json` | Checks supported local Markdown file links and an optional decision relationship index |

Limits are 1–1000 items; file scans cap at 10,000 files and documents at 1 MiB. Hidden paths, symlinks and common build/vendor directories are excluded. This is not a complete repository crawler or gitignore implementation. Git calls time out after 15 seconds. Subjects are capped at 500 characters with a truncation flag. No branches are fetched and rename following is not automatic. Selected deeper `git show` investigation is an agent step. Non-Git inventory works; history without commits fails.

Link support: ordinary inline links/images and reference definitions, URL-encoded filenames and angle-bracket destinations. Fenced and simple inline code examples are skipped. Local paths resolve relative to the source document and must stay inside ROOT. External URL schemes are skipped. Fragments are reported as unchecked. Nested-parenthesis destinations, HTML links, Markdown extensions and unresolved reference uses are not fully parsed. Use a full Markdown/site checker when these matter. An empty error list is not a claim that every rendered link works or every page is reachable.

Decision index is optional; [schema and semantics](decisions.md) describe it. Absent index reports manual relationship review needed. Invalid JSON/schema, duplicate IDs or paths, missing files/predecessors, invalid lifecycle, replacement cycles and superseded records without successors fail. Evidence truth and competing current decisions require semantic review.

Reports may contain sensitive filenames and commit subjects. Keep them private unless sanitized; do not redirect raw reports into the public documentation tree by default.
