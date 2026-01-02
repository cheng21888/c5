import sys
import os
import pandas as pd

# Add parent dir to path so we can import logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import get_sector_ranking

def test_get_sector_ranking():
    print("Testing get_sector_ranking(top_n=5)...")
    try:
        df = get_sector_ranking(5)
        print("Result Head:")
        print(df)
        
        if df.empty:
            print("FAILED: Result is empty.")
            return

        cols = df.columns.tolist()
        expected = ['板块名称', '板块代码', '涨跌幅']
        
        # Check columns
        if not all(col in cols for col in expected):
            print(f"FAILED: Missing columns. Got {cols}, expected {expected}")
            return
            
        # Check length
        if len(df) != 5:
            print(f"FAILED: Expected 5 rows, got {len(df)}")
            return
            
        # Check sorting
        if not df['涨跌幅'].is_monotonic_decreasing:
             print("FAILED: Not sorted by Change % descending")
             return

        print("PASSED: get_sector_ranking")
        return df.iloc[0]['板块名称'] # Return top sector for next test

    except Exception as e:
        print(f"FAILED with error: {e}")

if __name__ == "__main__":
    test_get_sector_ranking()
