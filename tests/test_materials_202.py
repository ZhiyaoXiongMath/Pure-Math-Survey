"""Authoring-input regressions; synthetic records do not certify mathematics."""
from pathlib import Path
import tempfile
import unittest
from test_v2 import fixture, plan, authored_toy, read_json, SurveyError, SCRIPTS
from survey_core.exports import prepare_output, verify_generated, validate_structure
from survey_core.build import build_output
from survey_core.release import package_output
from survey_core.migration import migrate_v1


class AuthoringMaterials(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.base=Path(self.tmp.name)
        self.root=fixture(self.base/'project',reviewed=True)
        self.plan_path=plan(self.root)
        authored_toy(self.root)
        self.out=self.plan_path.parent
        self.node=self.out/'materials/knowledge/nodes/N-main.md'

    def tearDown(self):
        self.tmp.cleanup()

    def verify(self):
        return verify_generated(self.root,read_json(self.plan_path))

    def refused(self,fn=None):
        with self.assertRaises(SurveyError) as caught:
            (fn or self.verify)()
        self.assertEqual(caught.exception.diagnostic['code'],'MATERIALS_CHANGED')
        return caught.exception.diagnostic

    def test_M01_unchanged_materials_validate_without_original_source_copy(self):
        self.assertFalse((self.out/'materials/knowledge/material.txt').exists())
        self.verify()
        self.assertEqual(validate_structure(self.root,'mini')['status'],'STRUCTURALLY_VALID')

    def test_M02_modified_explanation_is_rejected_with_its_path(self):
        self.node.write_bytes(self.node.read_bytes()+b'\nChanged explanation.\n')
        self.assertIn('materials/knowledge/nodes/N-main.md',str(self.refused()))

    def test_M03_missing_material_is_rejected(self):
        self.node.unlink()
        self.refused()

    def test_M04_extra_material_is_rejected(self):
        (self.out/'materials/unaudited.md').write_text('Unexpected authority.',encoding='utf-8')
        self.refused()

    def test_M05_stale_material_manifest_is_rejected(self):
        manifest=self.out/'materials/materials-manifest.json'
        manifest.write_text('{}\n',encoding='utf-8')
        self.refused()

    def test_M06_copied_review_must_match_its_frozen_original(self):
        review=self.out/'materials/evidence/reviews/mathematical-N-main.json'
        self.assertTrue(review.is_file())
        review.write_bytes(review.read_bytes()+b'\nChanged review.')
        self.refused()

    def test_M07_source_and_reading_note_are_bound(self):
        for name in ['knowledge/sources/S-test.json','evidence/source-checks/test.md']:
            with self.subTest(name=name):
                p=self.out/'materials'/name;old=p.read_bytes()
                p.write_bytes(old+b'\nChanged provenance.')
                self.refused()
                p.write_bytes(old)

    def test_M08_structure_build_and_release_refuse_before_use(self):
        self.node.write_bytes(self.node.read_bytes()+b'\nChanged material.')
        checks=[lambda:validate_structure(self.root,'mini'),lambda:build_output(self.root,'mini'),
                lambda:package_output(self.root,'mini',self.base/'not-created.zip')]
        for fn in checks:
            with self.subTest(check=checks.index(fn)):
                self.refused(fn)
        self.assertFalse((self.out/'build').exists())
        self.assertFalse((self.base/'not-created.zip').exists())

    def test_M09_explicit_reprepare_restores_materials_preserves_authoring(self):
        main=self.out/'manuscript/main.tex';main.write_bytes(main.read_bytes()+b'\n% author edits\n')
        original=main.read_bytes()
        outline=self.out/'outline.md';outline.write_text('Author outline\n',encoding='utf-8')
        self.node.unlink()
        prepare_output(self.root,self.plan_path)
        self.verify()
        self.assertEqual(main.read_bytes(),original)
        self.assertEqual(outline.read_text(encoding='utf-8'),'Author outline\n')

    def test_M10_editable_notes_outside_materials_are_not_authority(self):
        notes=self.out/'author-notes.md';notes.write_text('Ideas still to check.\n',encoding='utf-8')
        self.verify()

    def test_M11_unicode_legacy_scope_is_preserved(self):
        old=self.base/'旧项目';old.mkdir()
        text='# Scope\n\n范围：比较 α 与 β；保留原始假设。\n'
        (old/'scope.md').write_text(text,encoding='utf-8')
        (old/'main.tex').write_text(r'\begin{theorem}$0=0$.\end{theorem}',encoding='utf-8')
        new=self.base/'迁移'
        migrate_v1(old,new)
        self.assertEqual((new/'legacy/original/scope.md').read_text(encoding='utf-8'),text)
        self.assertIn(text,(new/'scope.md').read_text(encoding='utf-8'))

    def test_M12_legacy_entry_points_bootstrap_under_isolated_python(self):
        import subprocess, sys
        for name in ['validate_project.py','check_problem_formulation.py','check_survey_selection.py',
                     'check_mathematical_structure.py','check_reading_budget.py','bibliography.py']:
            with self.subTest(entry=name):
                p=subprocess.run([sys.executable,'-I',str(SCRIPTS/name),'--help'],capture_output=True,text=True)
                self.assertEqual(p.returncode,0,p.stderr)
