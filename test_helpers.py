"""Offline behavior tests for the self-contained Reel skill."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import beats
import detect
import hookscore
import humanize

ROOT=Path(__file__).resolve().parent

class Helpers(unittest.TestCase):
    def test_unicode_words(self):
        self.assertEqual(hookscore.words('Ședințele și încrederea schimbă relațiile.'),['Ședințele','și','încrederea','schimbă','relațiile'])
        self.assertEqual(beats.words('Încearcă să-mi scrii.'),['Încearcă','să-mi','scrii'])

    def test_romanian_specificity(self):
        self.assertGreater(hookscore.check_specificity('Am pierdut cinci ore.')[0],hookscore.check_specificity('Am pierdut timp.')[0])

    def test_romanian_address(self):
        self.assertEqual(hookscore.check_address('Tu pierzi cinci ore.')[0],100)

    def test_bilingual_preamble_flags(self):
        for text in ('Salut, în acest videoclip vreau să vorbesc.','Hey guys, in this video I will show you something.'):
            self.assertTrue(hookscore.run(text)[3])

    def test_timing_and_rate(self):
        result=beats.analyse('Ședințele și încrederea schimbă relațiile.\nCinci oameni verifică 3 idei.',wpm=60)
        self.assertEqual(result['total_words'],10)
        self.assertEqual(result['total_seconds'],10)
        self.assertEqual(result['beats'][1]['start'],5)

    def test_rate_validation(self):
        with self.assertRaises(ValueError): beats.analyse('Un text.',wpm=0)
        with self.assertRaises(ValueError): beats.analyse('Un text.',target=-1)

    def test_cleanup_preserves_voice_and_urls(self):
        text='Ședințe\u200b — „încredere”.\n\n👩\u200d💻 https://example.com/delve\n'
        clean,report=humanize.humanize(text,humanize.load_lexicon())
        self.assertEqual(clean,text.replace('\u200b',''))
        self.assertTrue(report['invisible'])

    def test_lexical_editing_is_opt_in(self):
        text='În peisajul actual lucrăm împreună.'
        clean,report=humanize.humanize(text,humanize.load_lexicon())
        self.assertEqual(clean,text)
        self.assertTrue(report['lexical'])
        edited,_=humanize.humanize(text,humanize.load_lexicon(),apply_lexical=True)
        self.assertEqual(edited,'Astăzi lucrăm împreună.')

    def test_short_text_reports_insufficient_data(self):
        result=detect.run('Mulțumesc, exemplul acesta ajută.',humanize.load_lexicon())
        self.assertEqual(result['verdict'],'INSUFFICIENT_DATA')
        self.assertIsNone(result['style_score'])
        self.assertEqual(len(result['checks']),5)

    def test_punctuation_is_not_authorship_evidence(self):
        result=detect.run('„Da” — încrederea contează… 👩\u200d💻',humanize.load_lexicon())
        self.assertEqual(result['checks']['FORMATTING']['score'],100)

    def test_all_formulas_and_lexicons_load(self):
        formulas=json.loads((ROOT/'hooks.json').read_text(encoding='utf-8'))
        self.assertEqual([h['id'] for h in formulas['hooks']],list(range(1,27)))
        for hook in formulas['hooks']:
            self.assertTrue(hook['template'])
            self.assertTrue(hook['template_ro'])
        for name in ('slop.json','slop-ro.json','slop-en.json'):
            self.assertIn('structures',humanize.load_lexicon(ROOT/name))

    def test_cli_works_from_another_directory(self):
        cases=[('hookscore.py',['--hook','Tu pierzi cinci ore fără acest model.','--json'],None),
               ('beats.py',['--json'],'Ședințele și încrederea schimbă relațiile.'),
               ('humanize.py',['--json'],'Ședințe\u200b și 👩\u200d💻.'),
               ('detect.py',['--json'],'Un exemplu scurt.')]
        with tempfile.TemporaryDirectory() as temporary:
            for script,args,text in cases:
                result=subprocess.run([sys.executable,'-B',str(ROOT/script),*args],input=text,text=True,capture_output=True,cwd=temporary)
                self.assertIn(result.returncode,(0,1),result.stderr)
                self.assertTrue(json.loads(result.stdout))

if __name__=='__main__': unittest.main(verbosity=2)
