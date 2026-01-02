import data_loader
import logic
import pandas as pd
import datetime

def test_export_logic():
    print("=== Testing Historical Export Logic ===")
    
    # 1. Test Valid Date (Last Friday 2025-12-19)
    valid_date = "20251219"
    print(f"\n[Test 1] Fetching for valid date: {valid_date}")
    df_valid = data_loader.get_limit_up_pool(date=valid_date)
    
    if not df_valid.empty:
        print(f"✅ Fetch Success. Rows: {len(df_valid)}")
        formatted_df = logic.format_limit_up_export(df_valid)
        print("Formatted Columns:", formatted_df.columns.tolist())
        
        # Check Critical Columns
        required = ['股票代码', '股票名称', '涨幅(%)', '连板高度']
        missing = [c for c in required if c not in formatted_df.columns]
        if not missing:
             print("✅ All critical columns present.")
        else:
             print(f"❌ Missing columns: {missing}")
             
        # Check conversion (Billions)
        if '流通市值(亿)' in formatted_df.columns:
            val = formatted_df['流通市值(亿)'].iloc[0]
            print(f"Sample Market Cap (Billions): {val}")
    else:
        print("❌ Fetch Failed for known valid date.")

    # 2. Test Weekend/Invalid Date (Sunday 2025-12-21)
    invalid_date = "20251221"
    print(f"\n[Test 2] Fetching for weekend date: {invalid_date}")
    df_invalid = data_loader.get_limit_up_pool(date=invalid_date)
    
    if df_invalid.empty:
        print("✅ Correctly returned empty for weekend.")
    else:
        print(f"⚠️ Warning: Returned {len(df_invalid)} rows for weekend? (Maybe API returns previous day or error message)")

if __name__ == "__main__":
    test_export_logic()
