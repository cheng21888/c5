import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import filter_dragons

def test_filter_dragons():
    print("Testing filter_dragons...")
    
    data = {
        '名称': ['DragonA', 'WeakB', 'ST_Dragon', 'DragonC'],
        '涨跌幅': [9.5, 3.0, 10.0, 20.0], # 20.0 for ChiNext
        '总市值': [100, 50, 200, 500]
    }
    df = pd.DataFrame(data)
    
    result = filter_dragons(df)
    
    names = result['名称'].tolist()
    
    # DragonA: Pass (>9, no ST)
    # WeakB: Fail (<9)
    # ST_Dragon: Fail (ST)
    # DragonC: Pass (>9)
    
    expected = ['DragonC', 'DragonA'] # Sorted by market cap desc
    
    if names != expected:
        # Note: Sorting order check
        if set(names) == set(expected):
            if names[0] != 'DragonC': # 500 > 100
                 print(f"FAILED: Sorting incorrect. Got {names}")
                 return
        else:
            print(f"FAILED: filtering incorrect. Got {names}, expected {expected}")
            return

    print("PASSED: filter_dragons")

if __name__ == "__main__":
    test_filter_dragons()
