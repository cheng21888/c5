import sys
import os
import pandas as pd
import numpy as np

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import clean_data

def test_clean_data():
    print("Testing clean_data...")
    
    # Create dirty data with strings
    data = {
        '代码': ['001', '002'],
        '名称': ['StockA', 'StockB'],
        '最新价': ['10.5', 12.0],
        '涨跌幅': ['9.9', 'nan'],
        '总市值': ['100000', 200000],
        '量比': ['1.2', 'bad_data'],
        '换手率': [5.5, None]
    }
    
    df = pd.DataFrame(data)
    cleaned = clean_data(df)
    
    # Check types
    numeric_cols = ['最新价', '涨跌幅', '总市值', '量比', '换手率']
    for col in numeric_cols:
        if not pd.api.types.is_float_dtype(cleaned[col]):
            print(f"FAILED: {col} is not float. Type: {cleaned[col].dtype}")
            return

    # Check values
    if cleaned.loc[0, '涨跌幅'] != 9.9:
        print(f"FAILED: Value mismatch. Expected 9.9, got {cleaned.loc[0, '涨跌幅']}")
        return
        
    if cleaned.loc[1, '涨跌幅'] != 0.0: # NaN should be 0
        print(f"FAILED: NaN handling. Expected 0.0, got {cleaned.loc[1, '涨跌幅']}")
        return

    if cleaned.loc[1, '量比'] != 0.0: # 'bad_data' should be 0
        print(f"FAILED: Bad string handling. Expected 0.0, got {cleaned.loc[1, '量比']}")
        return

    print("PASSED: clean_data")

if __name__ == "__main__":
    test_clean_data()
