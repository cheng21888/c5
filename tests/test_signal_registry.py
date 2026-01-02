import unittest
import pandas as pd
import sys
import os

# Add parent dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# We will import these after they are implemented, but for TDD we assume they exist or we import logic
import logic 

class TestSignalRegistry(unittest.TestCase):
    def test_registry_access(self):
        # 1. Register a dummy signal (mocking the registry mechanism)
        # Assuming SIGNAL_REGISTRY is a dict in logic.py
        
        def dummy_func(df):
            return pd.Series([True] * len(df), index=df.index)
            
        logic.SIGNAL_REGISTRY['test_dummy'] = {
            'id': 'test_dummy',
            'name': 'Dummy Signal',
            'func': dummy_func
        }
        
        # 2. Call get_active_signals
        active_signals = logic.get_active_signals(['test_dummy'])
        
        # 3. Validation
        self.assertEqual(len(active_signals), 1)
        self.assertEqual(active_signals[0]['id'], 'test_dummy')
        self.assertEqual(active_signals[0]['name'], 'Dummy Signal')
        
    def test_registry_missing_key(self):
        # Should return empty or handle gracefully
        active_signals = logic.get_active_signals(['non_existent_signal'])
        self.assertEqual(len(active_signals), 0)

if __name__ == '__main__':
    unittest.main()
