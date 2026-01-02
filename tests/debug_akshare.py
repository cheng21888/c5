import akshare as ak
import pandas as pd

print("Fetching All Spot Data (stock_zh_a_spot_em)...")
try:
    spot_df = ak.stock_zh_a_spot_em()
    print("Columns:", spot_df.columns.tolist())
    print(spot_df.head(3))
    
    # Check for Volume Ratio
    possible_names = ['量比', 'volume_ratio', 'Volume Ratio']
    found = [col for col in spot_df.columns if any(p in col for p in possible_names)]
    if found:
        print(f"\nSUCCESS: Found Volume Ratio column(s): {found}")
        print(spot_df[['名称', '代码'] + found].head())
    else:
        print("\nWARNING: Volume Ratio NOT found in spot data either!")

except Exception as e:
    print(f"Error: {e}")
