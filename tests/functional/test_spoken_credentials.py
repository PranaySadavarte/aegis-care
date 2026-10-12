import unittest
from backend.synthetic import SyntheticBackend
class SpokenCredentials(unittest.TestCase):
    def test_easy_and_legacy_variants(self):
        pairs=[("1001","4242"),("1 0 0 1","4 2 4 2"),("one zero zero one","four two four two"),
               ("hc 1001","demo 42"),("HC-1001","DEMO-42")]
        for patient,code in pairs:
            with self.subTest(patient=patient,code=code):
                self.assertTrue(SyntheticBackend().verify("s",patient,code))
    def test_wrong_values_never_fuzzy_match(self):
        for patient,code in [("1001","4243"),("1002","4242"),("100","4242"),("1001",""),("1001","4242!"),("1001","my code is 4242")]:
            with self.subTest(patient=patient,code=code):
                self.assertFalse(SyntheticBackend().verify("s",patient,code))
