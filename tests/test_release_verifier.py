"""Retain real child failure evidence without granting build acceptance."""
from pathlib import Path
import importlib.util
import copy
import errno
import json
import hashlib
import stat
import zipfile
import time
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release_verifier',ROOT/'tools/verify_release.py')
verifier=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class ReleaseVerifierEvidence(unittest.TestCase):
    def test_failed_child_retains_actual_inputs_and_output(self):
        with tempfile.TemporaryDirectory() as td:
            report={'checks':[]}
            with self.assertRaises(RuntimeError):
                with verifier.verification_workspace(report,Path(td)) as base:
                    (base/'input.tex').write_text('exact failed input',encoding='utf-8')
                    verifier.run_check([sys.executable,'-I','-c',
                        "print('actual build failure');raise SystemExit(7)"],base,os.environ.copy(),report,False)
            self.assertTrue(report['workspace']['retained'])
            self.assertEqual((base/'input.tex').read_text(),'exact failed input')
            self.assertEqual(report['checks'][0]['returncode'],7)
            self.assertIn('actual build failure',report['checks'][0]['stdout'])

    def test_success_cleanup_and_explicit_artifact_retention(self):
        with tempfile.TemporaryDirectory() as td:
            for keep in (False,True):
                report={'checks':[]}
                with verifier.verification_workspace(report,Path(td),keep) as base:
                    result=verifier.run_check([sys.executable,'-I','-c',
                        'print("{\\"status\\":\\"BUILT\\"}")'],base,os.environ.copy(),report)
                    self.assertEqual(result['status'],'BUILT')
                self.assertEqual(base.exists(),keep)

    def test_timeout_retains_partial_child_diagnostics(self):
        with tempfile.TemporaryDirectory() as td:
            report={'checks':[]}
            with self.assertRaises(subprocess.TimeoutExpired):
                with verifier.verification_workspace(report,Path(td)) as base:
                    verifier.run_check([sys.executable,'-I','-u','-c',
                        "import time;print('TeX still running',flush=True);time.sleep(30)"],
                        base,os.environ.copy(),report,False,timeout=3)
            self.assertTrue(base.exists())
            row=report['checks'][0]
            self.assertIsNone(row['returncode'])
            self.assertIn('TeX still running',row['stdout'])
            self.assertEqual(row['timeout_seconds'],3)


class MinimalVerifierContracts(unittest.TestCase):
    """Candidate identity, test evidence and process containment checks."""
    def valid_version(self):
        return {'version':'2.4.1-dev.2','schema_version':'2.0.0','output_schema_version':'2.2.0',
                'runtime_contract':verifier.EXPECTED_RUNTIME,
                'editorial_policy':verifier.EXPECTED_POLICY,
                'supported_output_contracts':[{'schema_version':s,'editorial_policy':p}
                                              for s,p in sorted(verifier.EXPECTED_CONTRACTS)]}

    def test_obsolete_extra_or_missing_contracts_cannot_pass_as_current(self):
        actual=self.valid_version()
        verifier.assert_installed_contract(actual)
        for key,value in (('editorial_policy','four-modes-2026-10-12-rc2'),
                          ('runtime_contract','legacy'),
                          ('version','2.2.0'),('schema_version','2.1.0'),
                          ('supported_output_contracts',[]),
                          ('supported_output_contracts',actual['supported_output_contracts']+[
                              {'schema_version':'2.0.0','editorial_policy':'legacy-2.0.0'}]),
                          ('supported_output_contracts',[
                              {'schema_version':'2.2.0','editorial_policy':'four-modes-2026-10-12-r3'}])):
            wrong=copy.deepcopy(actual);wrong[key]=value
            with self.subTest(key=key),self.assertRaises(AssertionError):verifier.assert_installed_contract(wrong)

    @staticmethod
    def installed_lines(platform='posix'):
        """Synthetic verbose log with all mandatory regressions, never a real run."""
        lines=[f'test_case ({name}.Current.test_case) ... ok'
               for name in verifier.REQUIRED_SUITES]
        for identity,required_os in sorted(verifier.PLATFORM_ONLY_TESTS.items()):
            outcome='ok' if platform==required_os else "skipped 'another-platform only'"
            lines.append(f'{identity.rsplit(".",1)[-1]} ({identity}) ... {outcome}')
        for identity in sorted(verifier.CAPABILITY_REQUIRED_TESTS):
            lines.append(f'{identity.rsplit(".",1)[-1]} ({identity}) ... ok')
        return lines

    @staticmethod
    def installed_log(lines, python310=False):
        # Actual Python 3.10 unittest -v omits the method in parentheses.
        # Python 3.12 repeats it. Keep the same canonical test identity.
        if python310:
            lines=[re.sub(r'\((test_\w+\.\w+)\.(test\w+)\) \.\.\.',
                          r'(\1) ...', line) for line in lines]
        skips=sum(' ... skipped ' in line for line in lines)
        return ('\n'.join(lines)+f'\nRan {len(lines)} tests in 2s\n'
                +(f'OK (skipped={skips})' if skips else 'OK'))

    def test_current_suites_must_really_execute_without_skips_or_failures(self):
        with patch.object(verifier.os,'name','posix'):
            with self.assertRaises(AssertionError):
                verifier.installed_regression_summary('Ran 189 tests in 2s\nOK')
            lines=self.installed_lines()
            for name in verifier.REQUIRED_SUITES:
                bad=[line for line in lines if f'({name}.' not in line]
                with self.subTest(missing_suite=name),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))
            for name in verifier.REQUIRED_SUITES:
                index=next(i for i,line in enumerate(lines) if f'({name}.' in line)
                for outcome in ("skipped 'unavailable'",'FAIL','ERROR'):
                    bad=lines.copy();bad[index]=bad[index].replace('... ok',f'... {outcome}')
                    with self.subTest(suite=name,outcome=outcome):
                        if outcome.startswith('skipped ') and name in {'test_v2', 'test_minimal_runtime'}:
                            # These suites still have other required test cases.
                            # A skipped companion must be INCOMPLETE, not an
                            # exception or a PASS, despite other tests being ok.
                            result=verifier.installed_regression_summary(self.installed_log(bad))
                            self.assertEqual(result['status'],'INCOMPLETE')
                            self.assertIn(bad[index],result['unexpected_skip_tests'])
                        else:
                            # Missing a required suite execution, or any real
                            # failure/error, is a broken regression run.
                            with self.assertRaises(AssertionError):
                                verifier.installed_regression_summary(self.installed_log(bad))
            summary=verifier.installed_regression_summary(self.installed_log(lines))
        self.assertEqual(summary['tests'],len(lines))
        self.assertEqual(summary['required_suites'],
                         {name:sum(f'({name}.' in line for line in lines)
                          for name in verifier.REQUIRED_SUITES})
        self.assertEqual(summary['status'],'PASS')
        self.assertEqual(len(summary['not_applicable_tests']),3)
        self.assertEqual(summary['unverified_tests'],[])
        self.assertEqual(summary['executed'],len(lines)-3)

    def test_real_python_310_and_312_verbose_formats_normalize_to_same_identity(self):
        for platform in ('posix','nt'):
            lines=self.installed_lines(platform)
            with patch.object(verifier.os,'name',platform):
                for old_format in (True,False):
                    with self.subTest(platform=platform,python310=old_format):
                        report=verifier.installed_regression_summary(
                            self.installed_log(lines,python310=old_format))
                        self.assertEqual(report['status'],'PASS')
                        self.assertEqual(report['tests'],len(lines))
                        self.assertEqual(len(report['not_applicable_tests']),
                                         3 if platform=='posix' else 0)
                        self.assertEqual(report['unverified_tests'],[])
                        # A skipped required symlink is not N/A under either
                        # unittest format, even when its skip reason says so.
                        capability=next(iter(sorted(verifier.CAPABILITY_REQUIRED_TESTS)))
                        bad=lines.copy()
                        index=next(i for i,line in enumerate(bad) if f'({capability})' in line)
                        bad[index]=bad[index].replace('... ok',"... skipped 'unavailable'")
                        report=verifier.installed_regression_summary(
                            self.installed_log(bad,python310=old_format))
                        self.assertEqual(report['status'],'INCOMPLETE')
                        self.assertEqual(len(report['unverified_capability_tests']),1)
    def test_windows_symlink_permission_skip_is_incomplete_never_pass(self):
        lines=self.installed_lines('nt')
        identity='test_v2.Contracts.test_H21_actual_symlink_rejected_when_available'
        index=next(i for i,line in enumerate(lines) if f'({identity})' in line)
        unavailable=(lines[index].replace('... ok',
            '... skipped "OS did not authorize directory symlink creation: [WinError 1314] denied"'))
        lines[index]=unavailable
        with patch.object(verifier.os,'name','nt'):
            result=verifier.installed_regression_summary(self.installed_log(lines))
            self.assertEqual(result['status'],'INCOMPLETE')
            self.assertEqual(result['not_applicable_tests'],[])
            self.assertEqual(result['unverified_capability_tests'],[unavailable])
            self.assertEqual(result['unverified_tests'],[unavailable])
            # Even a misleading or unfamiliar reason may never reclassify this
            # current-platform symlink check as NOT_APPLICABLE.
            for reason in ('WinError 5','Windows path syntax','arbitrary'):
                bad=lines.copy();bad[index]=unavailable.replace(
                    'OS did not authorize directory symlink creation: [WinError 1314] denied',reason)
                self.assertEqual(verifier.installed_regression_summary(
                    self.installed_log(bad))['status'],'INCOMPLETE')
            for outcome in ('FAIL','ERROR'):
                bad=lines.copy();bad[index]=unavailable.split('... skipped ')[0]+'... '+outcome
                with self.subTest(outcome=outcome),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))
        with patch.object(verifier.os,'name','posix'),self.assertRaises(AssertionError):
            verifier.installed_regression_summary(self.installed_log(lines))

    def test_nonrequired_skipped_test_also_prevents_regression_pass(self):
        lines=self.installed_lines()
        skipped="test_optional (test_other.Optional.test_optional) ... skipped 'unavailable'"
        with patch.object(verifier.os,'name','posix'):
            result=verifier.installed_regression_summary(self.installed_log(lines+[skipped]))
        self.assertEqual(result['status'],'INCOMPLETE')
        self.assertEqual(result['unexpected_skip_tests'],[skipped])
        self.assertEqual(result['unverified_tests'],[skipped])

    def test_linux_symlinks_and_windows_only_cases_are_distinct(self):
        lines=self.installed_lines()
        with patch.object(verifier.os,'name','posix'):
            result=verifier.installed_regression_summary(self.installed_log(lines))
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(len(result['not_applicable_tests']),3)
            self.assertEqual(result['unverified_capability_tests'],[])
            for identity in verifier.CAPABILITY_REQUIRED_TESTS:
                index=next(i for i,line in enumerate(lines) if f'({identity})' in line)
                bad=lines.copy()
                bad[index]=bad[index].replace('... ok',"... skipped 'capability unavailable'")
                summary=verifier.installed_regression_summary(self.installed_log(bad))
                self.assertEqual(summary['status'],'INCOMPLETE')
                self.assertEqual(len(summary['unverified_capability_tests']),1)

    def test_platform_required_and_missing_checks_never_pass(self):
        linux=self.installed_lines()
        win=self.installed_lines('nt')
        with patch.object(verifier.os,'name','nt'):
            self.assertEqual(verifier.installed_regression_summary(
                self.installed_log(win))['status'],'PASS')
            for identity in verifier.PLATFORM_ONLY_TESTS:
                index=next(i for i,line in enumerate(win) if f'({identity})' in line)
                bad=win.copy();bad[index]=bad[index].replace('... ok',
                    "... skipped 'permission or implementation missing'")
                self.assertEqual(verifier.installed_regression_summary(
                    self.installed_log(bad))['status'],'INCOMPLETE')
        with patch.object(verifier.os,'name','posix'):
            for identity in verifier.PLATFORM_ONLY_TESTS:
                index=next(i for i,line in enumerate(linux) if f'({identity})' in line)
                bad=linux.copy();bad[index]=bad[index].replace(
                    "... skipped 'another-platform only'",'... ok')
                with self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))
            for identity in [*verifier.PLATFORM_ONLY_TESTS,
                             *verifier.CAPABILITY_REQUIRED_TESTS]:
                bad=[line for line in linux if f'({identity})' not in line]
                with self.subTest(missing=identity),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))

    def test_unittest_totals_duplicate_and_partial_logs_cannot_pass(self):
        lines=self.installed_lines()
        with patch.object(verifier.os,'name','posix'):
            good=self.installed_log(lines)
            for log in (good.replace(f'Ran {len(lines)} tests', 'Ran 999 tests'),
                        good.replace('OK (skipped=3)','OK (skipped=2)'),
                        good.replace('OK (skipped=3)','FAILED (failures=1)'),
                        self.installed_log(lines+[lines[0]]),
                        good.replace('(test_build_layout.Current.', '(test_other.Current.')):
                with self.subTest(log=log[-100:]),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(log)

    def test_omitted_build_is_incomplete(self):
        self.assertEqual(verifier.verification_completion(True)[0], 'INCOMPLETE')
        self.assertEqual(verifier.verification_completion(False), ('PASS', []))

    def test_historical_manifest_is_never_discovered(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = root / 'examples/r4/verification-manifest.json'
            manifest.parent.mkdir(parents=True)
            manifest.write_text('Deliberately unreadable historical input')
            stdout = StringIO()
            with patch.object(verifier, 'ROOT', root), patch.object(sys, 'argv',
                    ['verify_release', 'missing.zip']), redirect_stdout(stdout):
                self.assertEqual(verifier.main(), 1)
            report = json.loads(stdout.getvalue())
            self.assertNotIn('manifest', report)
            self.assertNotIn('outputs', report)
            self.assertNotIn('manifest', report['failure'])

    def test_explicit_historical_manifest_is_rejected(self):
        stderr = StringIO()
        with patch.object(sys, 'argv', ['verify_release', 'missing.zip',
                '--manifest', 'explicit.json']), redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as caught:
                verifier.main()
        self.assertEqual(caught.exception.code, 2)
        self.assertIn('Historical output manifests are unsupported', stderr.getvalue())

    def _assert_posix_process_terminated(self,pid):
        try:
            state=Path(f'/proc/{pid}/stat').read_text()
        except (FileNotFoundError,ProcessLookupError):
            # procfs can disappear during open/read; confirm the PID is gone too.
            with self.assertRaises(ProcessLookupError):os.kill(pid,0)
        else:
            self.assertEqual(state.split()[2],'Z','Descendant is still running after timeout cleanup')

    def test_disappearing_procfs_requires_missing_pid(self):
        for error in (FileNotFoundError(errno.ENOENT,'process disappeared'),
                      ProcessLookupError(errno.ESRCH,'process disappeared')):
            with self.subTest(error=type(error).__name__), \
                    patch.object(Path,'read_text',autospec=True,side_effect=error) as read, \
                    patch.object(os,'kill',side_effect=ProcessLookupError(errno.ESRCH,'no such process')) as kill:
                self._assert_posix_process_terminated(12345)
                read.assert_called_once_with(Path('/proc/12345/stat'))
                kill.assert_called_once_with(12345,0)

    def test_disappearing_procfs_does_not_accept_live_pid(self):
        for error in (FileNotFoundError(errno.ENOENT,'process disappeared'),
                      ProcessLookupError(errno.ESRCH,'process disappeared')):
            with self.subTest(error=type(error).__name__), \
                    patch.object(Path,'read_text',side_effect=error), \
                    patch.object(os,'kill',return_value=None) as kill:
                with self.assertRaises(AssertionError):self._assert_posix_process_terminated(12345)
                kill.assert_called_once_with(12345,0)

    def test_procfs_requires_zombie_state(self):
        for state in ('Z','R','S','D','T','I'):
            with self.subTest(state=state), \
                    patch.object(Path,'read_text',return_value=f'12345 (python) {state} 1'), \
                    patch.object(os,'kill') as kill:
                if state=='Z':self._assert_posix_process_terminated(12345)
                else:
                    with self.assertRaises(AssertionError):self._assert_posix_process_terminated(12345)
                kill.assert_not_called()

    def test_procfs_unexpected_read_errors_propagate(self):
        for error in (PermissionError(errno.EACCES,'permission denied'),
                      OSError(errno.EIO,'unexpected read failure')):
            with self.subTest(error=type(error).__name__), \
                    patch.object(Path,'read_text',side_effect=error), \
                    patch.object(os,'kill') as kill:
                with self.assertRaises(type(error)) as caught:self._assert_posix_process_terminated(12345)
                self.assertIs(caught.exception,error)
                kill.assert_not_called()

    def test_procfs_unexpected_pid_probe_errors_propagate(self):
        for error in (PermissionError(errno.EPERM,'permission denied'),
                      OSError(errno.EIO,'unexpected probe failure')):
            with self.subTest(error=type(error).__name__), \
                    patch.object(Path,'read_text',side_effect=FileNotFoundError(errno.ENOENT,'process disappeared')), \
                    patch.object(os,'kill',side_effect=error) as kill:
                with self.assertRaises(type(error)) as caught:self._assert_posix_process_terminated(12345)
                self.assertIs(caught.exception,error)
                kill.assert_called_once_with(12345,0)

    def test_timeout_terminates_descendants_not_only_the_python_parent(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);pid_file=base/'child.pid'
            child="import time;time.sleep(30)"
            parent=("import pathlib,subprocess,sys,time;p=subprocess.Popen([sys.executable,'-c',"+repr(child)+"]);"
                    "pathlib.Path("+repr(str(pid_file))+").write_text(str(p.pid));"
                    "print('child spawned',flush=True);time.sleep(30)")
            report={'checks':[]}
            with self.assertRaises(subprocess.TimeoutExpired):
                verifier.run_check([sys.executable,'-I','-u','-c',parent],base,os.environ.copy(),report,False,timeout=3)
            pid=int(pid_file.read_text())
            if os.name=='nt':
                import ctypes
                from ctypes import wintypes
                kernel=ctypes.WinDLL('kernel32',use_last_error=True)
                kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
                kernel.OpenProcess.restype=wintypes.HANDLE
                kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
                kernel.CloseHandle.argtypes=[wintypes.HANDLE]
                handle=kernel.OpenProcess(0x1000,False,pid)
                if handle:
                    try:
                        code=wintypes.DWORD()
                        self.assertTrue(kernel.GetExitCodeProcess(handle,ctypes.byref(code)))
                        self.assertNotEqual(code.value,259,'Descendant is STILL_ACTIVE after timeout cleanup')
                    finally:kernel.CloseHandle(handle)
                else:self.assertEqual(ctypes.get_last_error(),87,'Unable to confirm child process termination')
            else:
                self._assert_posix_process_terminated(pid)
            self.assertEqual(report['checks'][0]['termination']['returncode'],0)
            self.assertIn('child spawned',report['checks'][0]['stdout'])

    @unittest.skipUnless(os.name=='nt','Windows Job Object lifetime contract')
    def test_exited_parent_inherited_pipe_is_bounded_and_external_process_survives(self):
        import ctypes
        from ctypes import wintypes as w
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);pidfile=base/'orphan.pid'
            child="import time;print('child holds pipe',flush=True);time.sleep(30)"
            parent=("import pathlib,subprocess,sys;p=subprocess.Popen([sys.executable,'-I','-u','-c',"+repr(child)+"]);"
                    "pathlib.Path("+repr(str(pidfile))+").write_text(str(p.pid));print('parent exits',flush=True)")
            unrelated=subprocess.Popen([sys.executable,'-I','-c','import time;time.sleep(30)'])
            try:
                report={'checks':[]};started=time.monotonic()
                with self.assertRaises(subprocess.TimeoutExpired):
                    verifier.run_check([sys.executable,'-I','-u','-c',parent],base,os.environ.copy(),report,False,timeout=3)
                self.assertLess(time.monotonic()-started,10)
                self.assertIsNone(unrelated.poll(),'An unrelated process was terminated')
                self.assertIn('parent exits',report['checks'][0]['stdout'])
                self.assertIn('child holds pipe',report['checks'][0]['stdout'])
                self.assertEqual(report['checks'][0]['termination']['method'],'TerminateJobObject')
                kernel=ctypes.WinDLL('kernel32',use_last_error=True)
                kernel.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];kernel.OpenProcess.restype=w.HANDLE
                kernel.GetExitCodeProcess.argtypes=[w.HANDLE,ctypes.POINTER(w.DWORD)]
                kernel.CloseHandle.argtypes=[w.HANDLE]
                handle=kernel.OpenProcess(0x1000,False,int(pidfile.read_text()))
                if handle:
                    try:
                        code=w.DWORD();self.assertTrue(kernel.GetExitCodeProcess(handle,ctypes.byref(code)))
                        self.assertNotEqual(code.value,259)
                    finally:kernel.CloseHandle(handle)
                else:self.assertEqual(ctypes.get_last_error(),87)
            finally:
                unrelated.terminate();unrelated.wait(timeout=10)


class InstallerArchiveSafety(unittest.TestCase):
    def setUp(self):
        from package_release import REQUIRED_FILES
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.skill = self.base / 'skill'
        for name in REQUIRED_FILES:
            path = self.skill / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'Isolated package safety fixture.\n')

    def tearDown(self):
        self.temp.cleanup()

    def test_historical_source_is_excluded_and_unknown_source_is_rejected(self):
        from package_release import package, selected_files
        for name in ('references/dispatch.md', 'references/output-review.md',
                     'assets/templates/profile-paper.tex', 'scripts/dispatch_ledger.py'):
            path = self.skill / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Historical instructions must not ship.')
        archive = self.base / 'skill.zip'
        package(self.skill, archive)
        with zipfile.ZipFile(archive) as z:
            self.assertIn('pure-math-survey/references/minimal-runtime.md', z.namelist())
            self.assertFalse(any('dispatch' in name or 'output-review' in name or
                                 'profile-paper' in name for name in z.namelist()))
        (self.skill / 'unexpected.txt').write_text('Do not silently distribute.')
        with self.assertRaisesRegex(ValueError, 'Unsupported file'):
            selected_files(self.skill)
        (self.skill / 'unexpected.txt').unlink()
        (self.skill / 'font.ttf').write_bytes(b'Not a redistributable font.')
        with self.assertRaisesRegex(ValueError, 'Font file'):
            selected_files(self.skill)

    def test_archive_rejects_traversal_symlink_tamper_and_historical_injection(self):
        from package_release import package, verify_archive
        good = self.base / 'good.zip'
        package(self.skill, good)
        with zipfile.ZipFile(good) as z:
            original = {name: z.read(name) for name in z.namelist()}
        for kind in ('traversal', 'symlink', 'tamper', 'historical'):
            members = original.copy()
            if kind == 'traversal':
                members['pure-math-survey/../escape.txt'] = b'outside'
            elif kind == 'tamper':
                members['pure-math-survey/SKILL.md'] += b'changed'
            elif kind == 'historical':
                relative = 'references/dispatch.md'
                content = b'Old runtime dispatch instructions'
                members['pure-math-survey/' + relative] = content
                members['pure-math-survey/artifact-checksums.txt'] += (
                    hashlib.sha256(content).hexdigest() + '  ' + relative + '\n').encode()
            damaged = self.base / (kind + '.zip')
            with zipfile.ZipFile(damaged, 'w') as z:
                for name, data in members.items():
                    if kind == 'symlink' and name == 'pure-math-survey/SKILL.md':
                        info = zipfile.ZipInfo(name)
                        info.create_system = 3
                        info.external_attr = (stat.S_IFLNK | 0o777) << 16
                        z.writestr(info, data)
                    else:
                        z.writestr(name, data)
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                verify_archive(damaged)


if __name__ == '__main__':
    unittest.main()
