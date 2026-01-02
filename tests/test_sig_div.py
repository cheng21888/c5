import unittest
import pandas as pd
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logic

class TestSigDiv(unittest.TestCase):
    def test_sector_divergence(self):
        if not hasattr(logic, 'sig_sector_divergence'):
            self.skipTest("sig_sector_divergence not implemented yet")

        # Logic: (sector_gain - stock_gain) > 3.0
        df = pd.DataFrame({
            'sector_pct_chg': [5.0, 5.0, 5.0],
            '涨跌幅': [1.0, 2.0, 4.0]
        })
        # 1: 5 - 1 = 4 (> 3) -> True
        # 2: 5 - 2 = 3 (Not > 3) -> False
        # 3: 5 - 4 = 1 (Not > 3) -> False
        
        result = logic.sig_sector_divergence(df)
        
        self.assertTrue(result[0])
        self.assertFalse(result[1])
        self.assertFalse(result[2])

if __name__ == '__main__':
    unittest.main()
