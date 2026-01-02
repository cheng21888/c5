import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import clean_data

class TestLogicDtypes(unittest.TestCase):
    def test_market_cap_float_and_drop_nan(self):
        # 1. Mock Data with Dirty Values
        # '000001': Valid
        # '000002': String Number
        # '000003': NaN Market Cap
        # '000004': Garbage String
        df = pd.DataFrame({
            '代码': ['000001', '000002', '000003', '000004'],
            '最新价': [10, 10, 10, 10],
            '涨跌幅': [1, 1, 1, 1],
            '总市值': [100, '200', np.nan, 'invalid'],
            '量比': [1, 1, 1, 1],
            '换手率': [1, 1, 1, 1]
        })

        # 2. Call clean_data
        result = clean_data(df)

        # 3. Validation
        # Should drop row 3 (NaN) and row 4 (Invalid became NaN)
        # Should keep row 1 and 2
        # Row 2 '200' should be float 200.0
        
        # Check dtype
        self.assertTrue(pd.api.types.is_float_dtype(result['总市值']))
        
        # Check values
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result.loc[1, '总市值'], 200.0)

if __name__ == '__main__':
    unittest.main()
