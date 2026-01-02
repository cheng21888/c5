import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import add_signals

def test_add_signals():
    print("Testing add_signals...")
    
    data = {
        '代码': ['001', '002', '003'],
        '量比': [1.6, 1.0, 2.0]
    }
    df = pd.DataFrame(data)
    
    result = add_signals(df)
    
    if '信号' not in result.columns:
        print("FAILED: '信号' column not created")
        return
        
    signals = result['信号'].tolist()
    expected = ['🔴', '', '🔴']
    
    if signals != expected:
        print(f"FAILED: Signals mismatch. Got {signals}, expected {expected}")
        return

    print("PASSED: add_signals")

if __name__ == "__main__":
    test_add_signals()
