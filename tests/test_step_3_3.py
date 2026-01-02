import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import filter_laggards

def test_filter_laggards():
    print("Testing filter_laggards...")
    
    # 10 Billion = 10 * 10^8 = 1,000,000,000
    # Threshold default is 100 Billion
    
    data = {
        '名称': ['GoodLaggard', 'HighGain', 'HugeCap', 'DeadStock', 'Negative'],
        '涨跌幅': [2.5, 5.0, 1.0, 2.0, -1.0],
        '总市值': [50e8, 50e8, 200e9, 50e8, 50e8], # 50亿, 50亿, 2000亿, 50亿, 50亿
        '换手率': [5.0, 5.0, 5.0, 1.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    # filter_laggards(df, max_cap_billion=100)
    result = filter_laggards(df, max_cap_billion=100)
    names = result['名称'].tolist()
    
    # GoodLaggard: Pass (2.5%, 50亿, 5% TO)
    # HighGain: Fail (5% > 4%)
    # HugeCap: Fail (2000亿 > 100亿)
    # DeadStock: Fail (1% TO < 3%)
    # Negative: Fail (-1% < 0%)
    
    expected = ['GoodLaggard']
    
    if names != expected:
        print(f"FAILED: Got {names}, expected {expected}")
        return

    print("PASSED: filter_laggards")

if __name__ == "__main__":
    test_filter_laggards()
