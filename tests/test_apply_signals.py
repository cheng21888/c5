import unittest
import pandas as pd
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logic

class TestApplySignals(unittest.TestCase):
    def setUp(self):
        # Setup dummy registry for testing
        self.original_registry = logic.SIGNAL_REGISTRY.copy() if hasattr(logic, 'SIGNAL_REGISTRY') else {}
        
        # Mock signals
        def sig_gt_5(df):
            return df['value'] > 5
            
        def sig_even(df):
            return df['value'] % 2 == 0
            
        logic.SIGNAL_REGISTRY['gt_5'] = {'id': 'gt_5', 'func': sig_gt_5}
        logic.SIGNAL_REGISTRY['even'] = {'id': 'even', 'func': sig_even}
        
    def tearDown(self):
        # Restore registry
        logic.SIGNAL_REGISTRY = self.original_registry

    def test_apply_signals_and_logic(self):
        # Mock Data: 1..10
        df = pd.DataFrame({'value': range(1, 11)}) # 1,2,3,4,5,6,7,8,9,10
        
        # Apply strict AND: > 5 AND Even
        # Candidates > 5: 6, 7, 8, 9, 10
        # Candidates Even: 2, 4, 6, 8, 10
        # Intersection: 6, 8, 10
        
        selected_ids = ['gt_5', 'even']
        result = logic.apply_signals(df, selected_ids)
        
        self.assertEqual(len(result), 3)
        self.assertListEqual(result['value'].tolist(), [6, 8, 10])

    def test_apply_no_signals(self):
        df = pd.DataFrame({'value': [1, 2, 3]})
        result = logic.apply_signals(df, [])
        # Should return original df (no filter)
        self.assertEqual(len(result), 3)

if __name__ == '__main__':
    unittest.main()
