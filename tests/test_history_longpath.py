"""Actual filesystem history checks; no mathematical acceptance is created."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/pure-math-survey/scripts'))
from survey_core.common import SurveyError, canonical, sha
from survey_core.history import _history_path, save_record, verify_record, verify_history, archive_current


class HistoryPaths(unittest.TestCase):
    def setUp(self):
        self.base=Path(tempfile.mkdtemp(prefix='pms-history-'))
        self.project=self.base/('project-'+('p'*70))
        self.out=self.project/'outputs'/'lichnerowicz-minimal-r3'
        self.member='inputs/materials/evidence/reviews/author-N-Q-lich-coverage-origin-r2.json'
        self.data={self.member:b'original immutable bytes\r\n'}

    def tearDown(self):
        self.assertEqual(self.base.resolve().parent,Path(tempfile.gettempdir()).resolve())
        shutil.rmtree(_history_path(self.base))

    def failcode(self,code,callback,*args):
        with self.assertRaises(SurveyError) as caught:callback(*args)
        self.assertEqual(caught.exception.diagnostic['code'],code)

    def record(self):
        manifest=save_record(self.out,'build',self.data)
        return manifest,self.out/'history/build'/manifest['history_id']

    def test_long_history_creation_rename_read_and_reuse_preserve_identity(self):
        manifest,folder=self.record()
        member=folder/'files'/self.member
        self.assertGreater(len(str(member)),260)
        expected={'format':'survey-artifact-history-1','kind':'build','files':[
            {'path':self.member,'sha256':sha(self.data[self.member]),'bytes':len(self.data[self.member])}]}
        self.assertEqual(manifest['history_id'],'H-'+sha(canonical(expected)))
        io_folder=_history_path(folder)
        before={p.relative_to(io_folder).as_posix():p.read_bytes() for p in io_folder.rglob('*') if p.is_file()}
        stamp=(io_folder/'manifest.json').stat().st_mtime_ns
        self.assertEqual(verify_record(folder),manifest)
        self.assertEqual(verify_history(self.project,self.out.name)['artifacts']['records'],[
            {'history_id':manifest['history_id'],'kind':'build','files':1}])
        self.assertEqual(save_record(self.out,'build',self.data),manifest)
        self.assertEqual((io_folder/'manifest.json').stat().st_mtime_ns,stamp)
        self.assertEqual(before,{p.relative_to(io_folder).as_posix():p.read_bytes() for p in io_folder.rglob('*') if p.is_file()})

    def test_same_size_tamper_and_real_membership_changes_are_rejected(self):
        manifest,folder=self.record();member=_history_path(folder)/'files'/self.member
        original=member.read_bytes();member.write_bytes(b'x'*len(original))
        self.failcode('HISTORY_TAMPERED',verify_record,folder)
        member.write_bytes(original)
        extra=_history_path(folder)/'files/extra.txt';extra.write_bytes(b'not in manifest')
        self.failcode('HISTORY_TAMPERED',verify_record,folder)
        extra.unlink();member.unlink()
        self.failcode('HISTORY_TAMPERED',verify_record,folder)

    def test_traversal_absolute_and_device_member_names_remain_rejected(self):
        for value in ('../escape.txt','inputs/../../escape.txt','/escape.txt','C:/escape.txt',r'inputs\escape.txt'):
            with self.subTest(value=value):
                self.failcode('UNSAFE_PATH',save_record,self.out,'build',{value:b'not written'})
        self.assertFalse((self.base/'escape.txt').exists())

    def test_archiving_long_current_paths_preserves_bytes(self):
        current=_history_path(self.out)/'evidence'/self.member
        current.parent.mkdir(parents=True);current.write_bytes(b'long current evidence')
        manifest=archive_current(self.out,'previous-build')
        folder=self.out/'history/previous-build'/manifest['history_id']
        self.assertEqual(verify_record(folder),manifest)
        self.assertEqual(current.read_bytes(),b'long current evidence')

    @unittest.skipUnless(os.name=='nt','Windows junction containment check')
    def test_real_junction_outside_project_is_rejected(self):
        self.project.mkdir(parents=True)
        outside=self.base/'outside';outside.mkdir()
        link=self.project/'outputs'
        command=['cmd','/c','mklink','/J',str(link),str(outside)]
        created=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(created.returncode,0,created.stdout+created.stderr)
        try:self.failcode('UNSAFE_PATH',verify_history,self.project,'escape')
        finally:os.rmdir(link)
        self.assertTrue(outside.is_dir())

    @unittest.skipUnless(os.name=='nt','Windows path syntax')
    def test_extended_prefix_is_idempotent_and_unc_is_preserved(self):
        for path in (self.out,Path(r'\\server\share\folder')):
            normalized=_history_path(path)
            self.assertEqual(_history_path(normalized),normalized)
            self.assertTrue(str(normalized).startswith('\\\\?\\'))
        self.assertEqual(str(_history_path(Path(r'\\server\share\folder'))),r'\\?\UNC\server\share\folder')


if __name__=='__main__':unittest.main()
