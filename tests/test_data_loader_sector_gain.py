import unittest
import pandas as pd
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import merge_stock_data

class TestDataLoaderSectorGain(unittest.TestCase):
    def test_sector_gain_injection(self):
        # 1. Mock Data
        cons_df = pd.DataFrame({'代码': ['000001', '000002']})
        spot_df = pd.DataFrame({
            '代码': ['000001', '000002'],
            '名称': ['A', 'B'],
            '最新价': [10, 20],
            '涨跌幅': [1.0, 2.0],
            '总市值': [100, 200],
            '量比': [1.1, 1.2],
            '换手率': [3, 4]
        })

        # 2. Call with sector_gain
        result = merge_stock_data(cons_df, spot_df, sector_gain=5.5)

        # 3. Validation
        self.assertIn('sector_pct_chg', result.columns)
        self.assertTrue((result['sector_pct_chg'] == 5.5).all())

if __name__ == '__main__':
    unittest.main()
