"""Failure-injection tests against disposable real Git checkouts; no network."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import glab


def command(*args,cwd=None):
    return subprocess.run(['git',*args],cwd=cwd,check=True,capture_output=True,text=True)


class WorkspaceManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_manifest = glab.MANIFEST.read_text()
        cls.template_dir = tempfile.TemporaryDirectory()
        cls.template = Path(cls.template_dir.name)/'template'
        command('init','-b','main',str(cls.template))
        command('config','user.email','reference@example.invalid',cwd=cls.template)
        command('config','user.name','Local fixture',cwd=cls.template)
        (cls.template/'README').write_text('initial fixture\n')
        command('add','README',cwd=cls.template)
        command('commit','-m','initial',cwd=cls.template)

    @classmethod
    def tearDownClass(cls):
        cls.template_dir.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        for name,value in (('BASE',self.base),('MANIFEST',self.base/'manifest.json'),('LOCK',self.base/'lock.json')):
            patcher = patch.object(glab,name,value)
            patcher.start()
            self.addCleanup(patcher.stop)
        glab.MANIFEST.write_text(self.source_manifest)
        (self.base/'workspaces').mkdir()
        for repo in glab.targets():
            self.clone(repo)
        self.stdout = contextlib.redirect_stdout(io.StringIO())
        self.stdout.__enter__()
        self.addCleanup(self.stdout.__exit__,None,None,None)

    def clone(self,repo):
        path = glab.folder(repo)
        command('clone','--quiet','--no-hardlinks',str(self.template),str(path))
        command('remote','set-url','origin',repo['git_url'],cwd=path)
        return path

    def test_lock_and_sync_repeat_without_mutating_existing_refs(self):
        self.assertEqual(glab.doctor(),0)
        self.assertEqual(glab.lock(),0)
        before = glab.LOCK.read_bytes()
        mtime = glab.LOCK.stat().st_mtime_ns
        for _ in range(2):
            self.assertEqual(glab.sync(require_lock=True),0)
            self.assertEqual(glab.lock(),0)
            self.assertEqual(glab.check_lock(),0)
        self.assertEqual(before,glab.LOCK.read_bytes())
        self.assertEqual(mtime,glab.LOCK.stat().st_mtime_ns)

    def test_dirty_checkout_blocks_all_operations_and_is_preserved(self):
        path = glab.folder(glab.targets()[0])/'user-work'
        path.write_text('keep me')
        for operation in (glab.doctor,glab.sync,glab.lock):
            with self.assertRaisesRegex(RuntimeError,'uncommitted'):
                operation()
        self.assertEqual(path.read_text(),'keep me')
        self.assertFalse(glab.LOCK.exists())

    def test_unknown_checkout_blocks_before_cloning(self):
        unknown = self.base/'workspaces/unrecognized'
        unknown.mkdir()
        with patch.object(glab,'git',wraps=glab.git) as spy:
            with self.assertRaisesRegex(RuntimeError,'unrecognized'):
                glab.sync()
            self.assertFalse(any(call.args[0]=='clone' for call in spy.call_args_list))

    def test_wrong_origin_and_parent_checkout_refused(self):
        repo = glab.targets()[0]
        path = glab.folder(repo)
        command('remote','set-url','origin','https://github.com/other/repository.git',cwd=path)
        with self.assertRaisesRegex(RuntimeError,'origin'):
            glab.collect_lock()
        command('remote','set-url','origin',repo['git_url'],cwd=path)
        shutil.rmtree(path/'.git')
        with self.assertRaisesRegex(RuntimeError,'independent Git'):
            glab.sync()

    def test_symlink_workspace_refused(self):
        repo = glab.targets()[0]
        path = glab.folder(repo)
        shutil.rmtree(path)
        path.symlink_to(self.template,target_is_directory=True)
        with self.assertRaises((ValueError,RuntimeError)):
            glab.sync()

    def test_lock_tampered_urls_schema_and_membership(self):
        glab.lock()
        baseline = json.loads(glab.LOCK.read_text())
        for mutate in (
            lambda d: d.update(schema='unknown'),
            lambda d: d['repositories'].pop(glab.NAMES[0]),
            lambda d: d['repositories'][glab.NAMES[0]].update(git_url='https://example.invalid/wrong'),
            lambda d: d['repositories'][glab.NAMES[0]].update(commit='not-a-sha')):
            data = json.loads(json.dumps(baseline))
            mutate(data)
            glab.LOCK.write_text(json.dumps(data))
            with self.assertRaises(RuntimeError): glab.check_lock()

    def test_new_commit_requires_explicit_lock_refresh(self):
        glab.lock()
        path = glab.folder(glab.targets()[0])
        command('config','user.email','reference@example.invalid',cwd=path)
        command('config','user.name','Local fixture',cwd=path)
        (path/'new').write_text('new commit')
        command('add','new',cwd=path)
        command('commit','-m','new',cwd=path)
        original = glab.LOCK.read_bytes()
        with self.assertRaises(RuntimeError): glab.check_lock()
        with self.assertRaises(RuntimeError): glab.sync()
        with self.assertRaisesRegex(RuntimeError,'refresh-lock'): glab.lock()
        self.assertEqual(glab.LOCK.read_bytes(),original)
        glab.lock(refresh=True)
        self.assertEqual(glab.check_lock(),0)

    def test_missing_clone_restored_to_pin_not_new_tip(self):
        glab.lock()
        repo = glab.targets()[0]
        sha = glab.read_lock()['repositories'][repo['name']]['commit']
        shutil.rmtree(glab.folder(repo))
        newer = self.base/'newer'
        command('clone','--quiet',str(self.template),str(newer))
        command('config','user.email','reference@example.invalid',cwd=newer)
        command('config','user.name','Local fixture',cwd=newer)
        (newer/'new').write_text('future main tip')
        command('add','new',cwd=newer)
        command('commit','-m','new tip',cwd=newer)
        original_git = glab.git

        def local_clone(*args,**kwargs):
            if args[0]=='clone':
                command('clone','--quiet',str(newer),args[-1])
                command('remote','set-url','origin',repo['git_url'],cwd=args[-1])
                return subprocess.CompletedProcess(args,0,'','')
            return original_git(*args,**kwargs)
        with patch.object(glab,'git',side_effect=local_clone):
            self.assertEqual(glab.sync(require_lock=True),0)
        self.assertEqual(glab.inspect(repo)['commit'],sha)
        self.assertEqual(glab.check_lock(),0)

    def test_missing_lock_and_unsafe_manifest_fail_closed(self):
        with self.assertRaises(RuntimeError): glab.sync(require_lock=True)
        data = json.loads(self.source_manifest)
        data['repositories'][0]['relative_path'] = '../escape'
        glab.MANIFEST.write_text(json.dumps(data))
        with self.assertRaises(ValueError): glab.manifest()


if __name__=='__main__':
    unittest.main()
