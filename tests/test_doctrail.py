import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/doctrail/scripts/doctrail.py'
spec = importlib.util.spec_from_file_location('doctrail', SCRIPT)
dt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dt)


class DocTrailTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout

    def init_git(self):
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')

    def commit(self, subject):
        self.git('add', '.')
        self.git('commit', '-qm', subject)

    def index(self, records):
        self.put('docs/decisions/index.json', json.dumps({'version': 1, 'records': records}))

    def record(self, key, status='accepted', supersedes=None):
        path = f'docs/decisions/{key}.md'
        self.put(path, '# Decision\n')
        return dict(id=key, path=path, status=status, topics=['replay'], supersedes=supersedes or [])

    def test_plain_directory_inventory_is_bounded_and_read_only(self):
        self.put('README.md', 'manual content')
        self.put('docs/use.md', '# Use')
        self.put('node_modules/a.md', 'excluded')
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = dt.inventory(self.root, 1)
        self.assertIsNone(result['head'])
        self.assertEqual(result['documents_found'], 2)
        self.assertTrue(result['documents_truncated'])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_history_recovers_reversal_without_fabricating_reason(self):
        self.init_git()
        self.put('engine.py', 'mode = "B"\n')
        self.commit('Baseline')
        self.put('engine.py', 'mode = "A"\n')
        self.commit('Try A')
        self.put('engine.py', 'mode = "B"\n')
        self.commit('Return to B')
        before = self.git('status', '--porcelain')
        result = dt.history(self.root, 2, ['engine.py'])
        self.assertEqual([r['subject'] for r in result['commits']], ['Return to B', 'Try A'])
        self.assertTrue(result['truncated'])
        self.assertNotIn('reason', result['commits'][0])
        self.assertEqual(before, self.git('status', '--porcelain'))

    def test_path_selection_is_literal(self):
        self.init_git()
        self.put('a[1].py', 'one')
        self.commit('Literal path')
        self.put('a1.py', 'two')
        self.commit('Other path')
        result = dt.history(self.root, 10, ['a[1].py'])
        self.assertEqual(len(result['commits']), 1)
        self.assertEqual(result['commits'][0]['subject'], 'Literal path')

    def test_empty_git_history_fails_honestly(self):
        self.init_git()
        result = subprocess.run(['python3', str(SCRIPT), 'history', str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)['ok'])

    def test_local_links_code_fences_and_reference_links(self):
        self.put('README.md', '[Guide](docs/usage.md)\n[Ref][r]\n[r]: docs/a%20b.md\n'
                 '```md\n[example](not-real.md)\n```\n`[example](also-not-real.md)`\n')
        self.put('docs/usage.md', '# Usage')
        self.put('docs/a b.md', '# Other')
        result = dt.check(self.root, 'docs/decisions/index.json')
        self.assertTrue(result['ok'], result)
        self.assertIn('absent', result['decision_index'])
        (self.root / 'docs/usage.md').unlink()
        self.assertFalse(dt.check(self.root, 'docs/decisions/index.json')['ok'])

    def test_anchors_are_explicitly_unchecked(self):
        self.put('README.md', '[Topic](#unknown)')
        result = dt.check(self.root, 'docs/decisions/index.json')
        self.assertTrue(result['ok'])
        self.assertEqual(len(result['unchecked_fragments']), 1)

    def test_escape_and_symlink_do_not_read_outside(self):
        self.put('README.md', '[outside](../outside.md)')
        (self.root / 'outside').symlink_to(self.root.parent, target_is_directory=True)
        result = dt.check(self.root, 'docs/decisions/index.json')
        self.assertFalse(result['ok'])
        self.assertEqual(dt.inventory(self.root, 10)['documents_found'], 1)
        with self.assertRaises(ValueError):
            dt.history(self.root, 10, ['outside/anything'])

    def test_valid_replacement_chain(self):
        self.index([self.record('D-1', 'superseded'), self.record('D-2', supersedes=['D-1'])])
        result = dt.check(self.root, 'docs/decisions/index.json')
        self.assertTrue(result['ok'], result)

    def test_missing_predecessor_and_dangling_superseded(self):
        self.index([self.record('D-1', 'superseded'), self.record('D-2', supersedes=['missing'])])
        errors, _ = dt.decisions(self.root, 'docs/decisions/index.json')
        self.assertTrue(any('missing predecessor' in e for e in errors))
        self.assertTrue(any('no successor' in e for e in errors))

    def test_cycle_rejected(self):
        self.index([self.record('D-1', 'superseded', ['D-2']), self.record('D-2', 'superseded', ['D-1'])])
        errors, _ = dt.decisions(self.root, 'docs/decisions/index.json')
        self.assertIn('Decision replacement cycle', errors)

    def test_invalid_status_duplicate_and_path(self):
        for records in ([self.record('D-1', 'invented')],
                        [self.record('D-1'), self.record('D-1')],
                        [dict(self.record('D-2'), path='../private.md')],
                        [dict(self.record('D-3'), supersedes='D-1')]):
            with self.subTest(records=records):
                self.index(records)
                self.assertTrue(dt.decisions(self.root, 'docs/decisions/index.json')[0])

    def test_proposed_cannot_replace_accepted_history(self):
        self.index([self.record('D-1', 'superseded'), self.record('D-2', 'proposed', ['D-1'])])
        self.assertTrue(dt.decisions(self.root, 'docs/decisions/index.json')[0])

    def test_cli_invalid_input_and_malformed_index(self):
        for args in (['inventory', str(self.root), '--limit', '0'],
                     ['check', str(self.root / 'missing')]):
            result = subprocess.run(['python3', str(SCRIPT), *args], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stdout)['ok'])
        self.put('docs/decisions/index.json', 'not json')
        self.assertFalse(dt.check(self.root, 'docs/decisions/index.json')['ok'])


if __name__ == '__main__':
    unittest.main()
