import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class Installer(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base=Path(self.temporary.name)
        self.package=self.base/'package'
        self.package.mkdir()
        shutil.copy2(ROOT/'install.py',self.package/'install.py')
        self.names=['ig-reel','ig-caption']
        files={}
        for name in self.names:
            path=self.package/'skills'/name/'SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text(f'name: {name}\n')
            files[str(path.relative_to(self.package))]=hashlib.sha256(path.read_bytes()).hexdigest()
        (self.package/'manifest.json').write_text(json.dumps({'skills':self.names,'files':files}))
        self.dest=self.base/'installed'

    def run_install(self,*args):
        return subprocess.run([sys.executable,'-B',str(self.package/'install.py'),'--dest',str(self.dest),*args],text=True,capture_output=True)

    def test_check_is_read_only(self):
        result=self.run_install('--check')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertFalse(self.dest.exists())

    def test_install_is_idempotent_and_exact(self):
        for _ in range(2):
            result=self.run_install()
            self.assertEqual(result.returncode,0,result.stderr)
        for name in self.names:
            self.assertEqual((self.dest/name/'SKILL.md').read_bytes(),(self.package/'skills'/name/'SKILL.md').read_bytes())

    def test_conflict_preserves_existing_and_does_not_partially_install(self):
        target=self.dest/'ig-caption'/'SKILL.md'
        target.parent.mkdir(parents=True)
        target.write_text('existing user skill')
        result=self.run_install()
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(target.read_text(),'existing user skill')
        self.assertFalse((self.dest/'ig-reel').exists())

    def test_modified_source_is_rejected(self):
        (self.package/'skills/ig-reel/SKILL.md').write_text('modified')
        result=self.run_install()
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(self.dest.exists())


if __name__=='__main__':
    unittest.main(verbosity=2)
