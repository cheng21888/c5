import sys
import os
import pandas as pd

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import get_stocks_in_sector, get_sector_ranking

def test_get_stocks_in_sector():
    # 1. Get a valid sector first
    print("Fetching top sector to test...")
    ranking = get_sector_ranking(1)
    if ranking.empty:
        print("SKIPPED: Could not fetch ranking.")
        return
        
    top_sector = ranking.iloc[0]['板块名称']
    print(f"Testing get_stocks_in_sector('{top_sector}')...")
    
    try:
        df = get_stocks_in_sector(top_sector)
        print("Result Head:")
        print(df.head())
        
        if df.empty:
            print("FAILED: Result is empty.")
            return

        # Check Columns
        expected_cols = ['代码', '名称', '最新价', '涨跌幅', '总市值', '量比', '换手率']
        if not all(col in df.columns for col in expected_cols):
             print(f"FAILED: Missing columns. Got {df.columns.tolist()}")
             return
             
        # Check content of Volume Ratio
        if df['量比'].isna().all():
            print("FAILED: All '量比' values are NaN!")
            return
            
        print(f"PASSED: get_stocks_in_sector. Rows: {len(df)}")
        print(f"Sample Volume Ratio: {df['量比'].iloc[0]}")

    except Exception as e:
        print(f"FAILED with error: {e}")

if __name__ == "__main__":
    test_get_stocks_in_sector()
