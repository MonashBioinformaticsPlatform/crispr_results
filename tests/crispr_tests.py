import os
import unittest

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'crispr'))
import crispr

class CrisprTestCase(unittest.TestCase):

    def setUp(self):
        self.app = crispr.app.test_client()

    def tearDown(self):
        pass
    
    def test_root(self):
        rv = self.app.get('/')
        assert b'Report body' in rv.data    

if __name__ == '__main__':
    unittest.main()