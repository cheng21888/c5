import unittest
import pandas as pd
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logic

class TestSigCap(unittest.TestCase):
    def test_small_cap_quantile(self):
        if not hasattr(logic, 'sig_small_cap'):
            self.skipTest("sig_small_cap not implemented yet")

        # Logic: Bottom 20% (quantile 0.2)
        # Create 10 rows: 10, 20, ..., 100
        df = pd.DataFrame({'总市值': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
        
        # Quantile 0.2 of 1..10 is roughly 2.8? 
        # Pandas quantile defaults to 'linear'.
        # 10 data points. 0.2 quantile should capture bottom 2.
        
        result = logic.sig_small_cap(df)
        
        # Should select 10 and 20.
        self.assertTrue(result[0])
        self.assertTrue(result[1])
        self.assertFalse(result[2]) # 30 might be on the edge depending on exact quantile algo, usually false logic says <= q0.2

if __name__ == '__main__':
    unittest.main()
