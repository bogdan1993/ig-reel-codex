"""Behavior checks: no network, no account access, no external side effects."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT/'skills'
sys.dont_write_bytecode = True
for name in ('ig-reel','ig-human','ig-caption','ig-viral','ig-audit'):
    sys.path.insert(0,str(SKILLS/name))
import hookscore
import beats
import caption
import humanize
import detect
import swipe
import audit


class Helpers(unittest.TestCase):
    def test_romanian_words_remain_whole(self):
        text = 'Ședințele și încrederea schimbă relațiile.'
        self.assertEqual(hookscore.words(text),['Ședințele','și','încrederea','schimbă','relațiile'])
        self.assertEqual(beats.words(text),hookscore.words(text))

    def test_hyphenated_words_remain_whole(self):
        self.assertIn('scrie-mi',hookscore.words('Poți să îmi scrie-mi un mesaj'))

    def test_romanian_number_specificity(self):
        self.assertGreater(hookscore.check_specificity('Am pierdut cinci ore.')[0],hookscore.check_specificity('Am pierdut timp.')[0])

    def test_romanian_viewer_address(self):
        self.assertEqual(hookscore.check_address('Tu pierzi cinci ore pe săptămână.')[0],100)

    def test_bilingual_bad_hook_flags(self):
        for text in ('Salut, în acest videoclip vreau să vorbesc despre ceva.','Hey guys, in this video I will show you something.'):
            self.assertTrue(hookscore.run(text)[3])

    def test_timings_from_words_and_rate(self):
        result = beats.analyse('Ședințele și încrederea schimbă relațiile.\nCinci oameni verifică 3 idei.',wpm=60)
        self.assertEqual(result['total_words'],10)
        self.assertEqual(result['total_seconds'],10)
        self.assertEqual(result['beats'][1]['start'],5)

    def test_invalid_speaking_rate(self):
        with self.assertRaises(ValueError):
            beats.analyse('Un text',wpm=0)

    def test_caption_unicode_tags_and_cta(self):
        result = caption.analyse('Am economisit 5 ore.\nSalvează postarea.\n#ședințe #încredere')
        self.assertEqual(result['hashtags'],['#ședințe','#încredere'])
        self.assertEqual(result['asks'],['salvează'])

    def test_caption_english_cta(self):
        self.assertEqual(caption.analyse('Save this for your next meeting.')['asks'],['save this'])

    def test_caption_hashtag_override_and_preview(self):
        result = caption.analyse('A'*140+'\n#unu #doi',cut=125,hashtag_limit=1)
        self.assertEqual(len(result['visible']),125)
        self.assertTrue(result['truncated'])
        self.assertEqual(next(c for c in result['checks'] if c['check']=='HASHTAGS')['status'],'FAIL')

    def test_cleanup_preserves_semantic_content_and_emoji(self):
        text = 'Ședințe\u200b — „încredere”.\n\n👩\u200d💻 https://example.com/delve?q=important\n'
        clean,report = humanize.humanize(text,humanize.load_lexicon())
        self.assertEqual(clean,text.replace('\u200b',''))
        self.assertTrue(report['invisible'])

    def test_lexical_suggestions_are_not_automatic(self):
        text = 'Este important de menționat că avem dovezi.'
        clean,report = humanize.humanize(text,humanize.load_lexicon())
        self.assertEqual(clean,text)
        self.assertTrue(report['lexical'])
        self.assertFalse(report['lexical'][0]['applied'])

    def test_lexical_opt_in(self):
        text = 'În peisajul actual lucrăm împreună.'
        clean,_ = humanize.humanize(text,humanize.load_lexicon(),apply_lexical=True)
        self.assertEqual(clean,'Astăzi lucrăm împreună.')

    def test_short_style_panel_is_not_failed_authorship_test(self):
        result = detect.run('Mulțumesc, exemplul acesta ajută.',humanize.load_lexicon())
        self.assertEqual(result['verdict'],'INSUFFICIENT_DATA')
        self.assertIsNone(result['style_score'])
        self.assertEqual(len(result['checks']),5)

    def test_typography_does_not_prove_ai(self):
        result=detect.run('„Da” — încrederea contează… 👩\u200d💻',humanize.load_lexicon())
        self.assertEqual(result['checks']['FORMATTING']['score'],100)

    def test_formula_ids_preserved_and_bilingual(self):
        data=json.loads((SKILLS/'ig-reel/hooks.json').read_text())
        self.assertEqual([h['id'] for h in data['hooks']],list(range(1,27)))
        formulas=swipe.load_formulas(SKILLS/'ig-reel/hooks.json')
        self.assertEqual(swipe.classify('Nobody tells you your first 30 reels flop.',formulas)[0],3)
        self.assertEqual(swipe.classify('Nimeni nu îți spune cât costă.',formulas)[0],3)

    def test_no_follower_baseline_fallback(self):
        rows=[{'account':'@a','median':100,'views':1000,'followers':10,'hook':'Am pierdut cinci ore.'},
              {'account':'@b','median':None,'views':10000,'followers':10,'hook':'Am pierdut șase ore.'},
              {'account':'@c','median':0,'views':10000,'followers':10,'hook':'Am pierdut șapte ore.'}]
        result=swipe.analyse(rows,[])
        self.assertEqual(result['ranked_n'],1)
        self.assertEqual(result['reels'][0]['outlier'],10)
        self.assertIsNone(result['reels'][1]['outlier'])
        self.assertIsNone(result['reels'][2]['outlier'])
        self.assertIsNone(result['top_hook_score'])

    def test_zero_view_post_is_retained(self):
        result=swipe.analyse([{'account':'@a','median':100,'views':0,'hook':'Un început.'}],[])
        self.assertEqual(result['ranked_n'],1)
        self.assertEqual(result['reels'][0]['outlier'],0)

    def test_abbreviated_numbers_rejected(self):
        for number in ('12k','1.2M','-5','1,000'):
            with self.assertRaises(ValueError):
                swipe.number(number,'views')

    def test_provenance_survives_markdown(self):
        row={'account':'@a','median':100,'views':1000,'hook':'O idee.','url':'https://example.com/reel','observed_at':'2026-11-01'}
        text=swipe.to_markdown(swipe.analyse([row],[]))
        self.assertIn(row['url'],text)
        self.assertIn(row['observed_at'],text)

    def test_audit_missing_values_zero_denominators_and_shares(self):
        result=audit.analyse([{'id':'a','views':'100','reach':'0','shares':'5'},
                              {'id':'b','views':'300','reach':'100','sends':'5','shares':'12','follows':'2'}])
        a,b=result['posts']
        self.assertEqual(a['median_views'],200)
        self.assertIsNone(a['sends_per_reach'])
        self.assertIsNone(a['shares_per_reach'])
        self.assertEqual(b['sends_per_reach'],.05)
        self.assertEqual(b['shares_per_reach'],.12)
        self.assertEqual(b['follows_per_reach'],.02)

    def test_audit_separates_accounts_and_formats(self):
        result=audit.analyse([{'views':'100','account':'a','format':'reel'}, {'views':'500','account':'a','format':'carousel'}, {'views':'1000','account':'b','format':'reel'}])
        self.assertEqual([r['median_views'] for r in result['posts']],[100,500,1000])

    def test_audit_rejects_nonfinite_negative(self):
        for value in ('nan','inf','-1','1.2'):
            with self.assertRaises(ValueError):
                audit.numeric(value,'views')

    def test_cli_helpers_run_from_unrelated_working_directory(self):
        cases=[('ig-reel/hookscore.py',['--hook','Tu pierzi cinci ore fără acest model.','--json'],None),
               ('ig-reel/beats.py',['--json'],'Ședințele și încrederea schimbă relațiile.'),
               ('ig-caption/caption.py',['--json'],'Salvează 3 idei pentru mâine.'),
               ('ig-human/humanize.py',['--json'],'Ședințe\u200b și 👩\u200d💻.'),
               ('ig-human/detect.py',['--json'],'O idee scurtă.'),
               ('ig-viral/swipe.py',['--json'],'account\tmedian\tviews\thook\n@a\t100\t300\tNimeni nu îți spune cât costă.\n'),
               ('ig-audit/audit.py',['--json'],'id,views,reach,sends\na,100,50,5\n')]
        with tempfile.TemporaryDirectory() as temporary:
            for script,args,text in cases:
                run=subprocess.run([sys.executable,'-B',str(SKILLS/script),*args],input=text,text=True,capture_output=True,cwd=temporary)
                self.assertIn(run.returncode,(0,1),(script,run.stderr))
                self.assertTrue(json.loads(run.stdout),(script,run.stdout))


if __name__=='__main__':
    unittest.main(verbosity=2)
