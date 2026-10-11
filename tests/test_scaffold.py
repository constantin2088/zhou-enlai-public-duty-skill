import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from new_skill import create,validate_slug
from check_skill import check

class ScaffoldTests(unittest.TestCase):
    def test_reject_bad_slug(self):
        with self.assertRaises(ValueError):
            validate_slug('../x')
    def test_generate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=create('chen-yinke-research-skill','陈寅恪','深度研究',tmp)
            self.assertTrue((p/'SKILL.md').exists())
            self.assertEqual(check(p),[])
    def test_release_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=create('test-thinker','测试人物','研究',tmp)
            self.assertTrue(check(p,release=True))
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            create('test-thinker','测试人物','研究',tmp)
            with self.assertRaises(FileExistsError):
                create('test-thinker','测试人物','研究',tmp)
    def test_generated_evaluation_plan_meets_case_gate_but_remains_pending(self):
        import re
        with tempfile.TemporaryDirectory() as tmp:
            p=create('new-thinker','新人物','研究',tmp)
            evaluation=(p/'evals/test-cases.md').read_text(encoding='utf-8')
            headings=re.findall(r'^## Case \d+.*$',evaluation,re.M)
            self.assertGreaterEqual(len(headings),10)
            self.assertGreaterEqual(sum('negative' in h or 'adversarial' in h for h in headings),3)
            self.assertIn('all cases are pending',evaluation)
            self.assertTrue(check(p,release=True),'Generating a plan must not silently publish a finished Skill')

if __name__=='__main__':
    unittest.main()

class SeriesScaffoldTests(unittest.TestCase):
    def test_new_person_has_series_and_refresh_workflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=create('new-thinker','新人物','研究',tmp)
            text=(p/'README.md').read_text(encoding='utf-8')
            self.assertIn('Chinese Thinkers as Skills',text)
            self.assertIn('liang-qichao-skill',text)
            self.assertTrue((p/'scripts/sync_series.py').exists())
            self.assertTrue((p/'.github/workflows/series-links.yml').exists())
    def test_release_rejects_unfinished_secondary_example(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=create('new-thinker','新人物','研究',tmp)
            for file in p.rglob('*.md'):
                file.write_text(file.read_text(encoding='utf-8').replace('TODO','Complete').replace('DRAFT','Ready'),encoding='utf-8')
            (p/'examples/unfinished.md').write_text('TODO: research this claim',encoding='utf-8')
            self.assertIn('unfinished examples/unfinished.md',check(p,release=True))
