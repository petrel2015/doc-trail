#!/usr/bin/env python3
"""Read-only, bounded documentation inventory and structural checks (stdlib only)."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

SKIP = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'dist', 'build', '.next', '.cache'}
LIMIT = 10000


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, timeout=15)
    if result.returncode:
        raise ValueError('Git operation unavailable: ' + ' '.join(args[:2]))
    return result.stdout.decode('utf-8', errors='replace')


def inside(root, path):
    try:
        path.resolve().relative_to(root)
        return True
    except (ValueError, OSError, RuntimeError):
        return False


def files(root):
    """Return at most LIMIT files; never descend through a symlink."""
    found = []
    capped = False
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith('.')
                         and not (Path(base) / d).is_symlink())
        for name in sorted(names):
            p = Path(base) / name
            if name.startswith('.') or p.is_symlink() or not p.is_file():
                continue
            if len(found) >= LIMIT:
                capped = True
                return found, capped
            found.append(p)
    return found, capped


def read_doc(path):
    if path.stat().st_size > 1024 * 1024:
        raise ValueError('Document exceeds 1 MiB scan limit')
    return path.read_text(encoding='utf-8')


def inventory(root, limit):
    paths, capped = files(root)
    docs = [str(p.relative_to(root)) for p in paths if p.suffix.lower() == '.md']
    try:
        head = git(root, 'rev-parse', '--verify', 'HEAD').strip()
        shallow = git(root, 'rev-parse', '--is-shallow-repository').strip() == 'true'
    except (ValueError, FileNotFoundError):
        head, shallow = None, None
    return {'command': 'inventory', 'head': head, 'shallow': shallow,
            'files_scanned': len(paths), 'scan_truncated': capped,
            'documents': docs[:limit], 'documents_found': len(docs),
            'documents_truncated': len(docs) > limit,
            'entry_points': [p for p in docs if '/' not in p],
            'limits': ['Hidden files/directories, symlinks and common build/vendor directories excluded.',
                       'No file contents, Git motives or semantic correctness inferred.']}


def history(root, limit, paths):
    selected = []
    for value in paths:
        p = root / value
        if Path(value).is_absolute() or not inside(root, p):
            raise ValueError('History paths must stay inside the repository')
        selected.append(str(p.relative_to(root)))
    args = ['--literal-pathspecs', 'log', f'--max-count={limit + 1}',
            '--format=%H%x00%cs%x00%s%x00']
    if selected:
        args += ['--', *selected]
    rows = git(root, *args).strip().split('\x00')
    commits = []
    for i in range(0, len(rows) - 2, 3):
        subject = rows[i + 2]
        commits.append({'commit': rows[i].strip(), 'date': rows[i + 1],
                        'subject': subject[:500], 'subject_truncated': len(subject) > 500})
    return {'command': 'history', 'commits': commits[:limit],
            'truncated': len(commits) > limit,
            'shallow': git(root, 'rev-parse', '--is-shallow-repository').strip() == 'true',
            'scope': 'current HEAD ancestry; selected literal paths; rename following not automatic',
            'paths': selected,
            'warning': 'Commit subjects are leads and attributed statements, not proof of motivation.'}


def prose(text):
    lines, fenced = [], None
    for line in text.splitlines():
        m = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if m:
            marker = m.group(1)
            if fenced is None:
                fenced = marker
            elif marker[0] == fenced[0] and len(marker) >= len(fenced):
                fenced = None
            continue
        if fenced is None:
            lines.append(re.sub(r'(`+).*?\1', '', line))
    return '\n'.join(lines)


def links(text):
    text = prose(text)
    # Deliberately a limited Markdown subset; see references/tools.md.
    for match in re.finditer(r'!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+[^)]*)?\)', text):
        yield match.group(1).strip('<>')
    for match in re.finditer(r'^\s{0,3}\[[^\]]+\]:\s*(<[^>\n]+>|\S+)', text, re.M):
        yield match.group(1).strip('<>')


def decisions(root, manifest):
    errors = []
    p = root / manifest
    if not inside(root, p):
        return ['Decision index escapes repository'], 'invalid'
    if not p.exists():
        return [], 'absent; relationship review must be manual'
    try:
        data = json.loads(read_doc(p))
    except (ValueError, OSError, UnicodeError) as e:
        return ['Invalid decision index: ' + str(e)], 'invalid'
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('records'), list):
        return ['Decision index requires version 1 and a records array'], 'invalid'
    records, used_paths = {}, set()
    for item in data['records']:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id'].strip():
            errors.append('Decision record requires a nonempty string id')
            continue
        key = item['id']
        if key in records:
            errors.append(f'Duplicate decision id: {key}')
        records[key] = item
        path = item.get('path')
        if not isinstance(path, str) or not path or Path(path).is_absolute() or not inside(root, root / path):
            errors.append(f'{key}: invalid repository-relative path')
        else:
            target = (root / path).resolve()
            if target in used_paths:
                errors.append(f'{key}: duplicate decision path')
            used_paths.add(target)
            if not target.is_file() or target.suffix.lower() != '.md':
                errors.append(f'{key}: missing Markdown decision file')
        if item.get('status') not in ('proposed', 'accepted', 'rejected', 'superseded'):
            errors.append(f'{key}: invalid lifecycle status')
        for field in ('topics', 'supersedes'):
            values = item.get(field)
            if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
                errors.append(f'{key}: {field} requires string array')
            elif len(set(values)) != len(values) or (field == 'topics' and not values):
                errors.append(f'{key}: {field} must be unique and topics nonempty')
    if errors:
        return errors, 'invalid'
    replaced = set()
    for key, item in records.items():
        for old in item['supersedes']:
            if old not in records:
                errors.append(f'{key}: missing predecessor {old}')
            else:
                replaced.add(old)
                if records[old]['status'] != 'superseded':
                    errors.append(f'{key}: predecessor {old} must be superseded')
                if item['status'] not in ('accepted', 'superseded'):
                    errors.append(f'{key}: unaccepted decision cannot supersede another')
    for key, item in records.items():
        if item['status'] == 'superseded' and key not in replaced:
            errors.append(f'{key}: superseded decision has no successor')
    # Iterative topological traversal avoids recursion failure on long histories.
    degree = {key: 0 for key in records}
    for item in records.values():
        for old in item['supersedes']:
            if old in degree:
                degree[old] += 1
    ready = [key for key, value in degree.items() if value == 0]
    visited = 0
    while ready:
        key = ready.pop()
        visited += 1
        for old in records[key]['supersedes']:
            if old in degree:
                degree[old] -= 1
                if degree[old] == 0:
                    ready.append(old)
    if visited != len(records):
        errors.append('Decision replacement cycle')
    return errors, 'checked'


def check(root, manifest):
    paths, capped = files(root)
    errors, unchecked = [], []
    count = 0
    for path in paths:
        if path.suffix.lower() != '.md':
            continue
        count += 1
        rel = str(path.relative_to(root))
        try:
            text = read_doc(path)
        except (ValueError, OSError, UnicodeError) as e:
            errors.append(f'{rel}: unreadable: {e}')
            continue
        for href in links(text):
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            if not parsed.path:
                unchecked.append(f'{rel}: anchor {href}')
                continue
            target = path.parent / unquote(parsed.path)
            if not inside(root, target):
                errors.append(f'{rel}: link escapes repository: {href}')
            elif not target.exists():
                errors.append(f'{rel}: missing link target: {href}')
            elif parsed.fragment:
                unchecked.append(f'{rel}: fragment {href}')
    issues, state = decisions(root, manifest)
    errors.extend(issues)
    if capped:
        errors.append('Scan truncated at 10000 files; narrow repository scope')
    return {'command': 'check', 'ok': not errors, 'documents_checked': count,
            'decision_index': state, 'errors': errors, 'unchecked_fragments': unchecked,
            'limits': ['Local file targets and optional decision relationships only.',
                       'No remote URLs, anchors, orphan detection or semantic verification.',
                       'Limited Markdown syntax; hidden paths and symlinks excluded.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('inventory', 'history', 'check'):
        child = sub.add_parser(command)
        child.add_argument('root', type=Path)
        if command != 'check':
            child.add_argument('--limit', type=int, default=100)
        if command == 'history':
            child.add_argument('--path', action='append', default=[])
        if command == 'check':
            child.add_argument('--decisions', default='docs/decisions/index.json')
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('Root must be a directory')
        if hasattr(args, 'limit') and not 1 <= args.limit <= 1000:
            raise ValueError('Limit must be between 1 and 1000')
        if args.command == 'inventory':
            result = inventory(root, args.limit)
        elif args.command == 'history':
            result = history(root, args.limit, args.path)
        else:
            result = check(root, args.decisions)
    except (ValueError, OSError, UnicodeError, subprocess.TimeoutExpired) as e:
        result = {'command': args.command, 'ok': False, 'errors': [str(e)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result.get('ok') is False else 0


if __name__ == '__main__':
    sys.exit(main())
