import sys
import time
import pandas as pd
from unittest.mock import MagicMock

# 1. Mock Streamlit BEFORE importing data_loader
# Because data_loader uses @st.cache_data decorator at import time
mock_st = MagicMock()
def mock_cache(ttl=None):
    def decorator(func):
        return func
    return decorator
mock_st.cache_data = mock_cache
sys.modules['streamlit'] = mock_st

# Now we can import
import data_loader

def verify_performance():
    print("--- Starting Verification ---")
    start_time = time.time()
    
    print("[1] Fetching Sector Ranking...")
    t0 = time.time()
    sector_df = data_loader.get_sector_ranking(top_n=3) # Test with 3
    t1 = time.time()
    print(f"    Got {len(sector_df)} sectors. Time: {t1-t0:.2f}s")
    
    if sector_df.empty:
        print("!!! Failed to get sectors. Aborting.")
        return

    print("[2] Fetching Global Spot Data (Once)...")
    t0 = time.time()
    spot_data = data_loader.get_all_market_spot_data()
    t1 = time.time()
    print(f"    Got {len(spot_data)} rows. Time: {t1-t0:.2f}s")
    
    if spot_data.empty:
        print("!!! Failed to get spot data. Aborting.")
        return

    print("[3] Fetching Constituents (Parallel)...")
    sector_names = sector_df['板块名称'].tolist()
    print(f"    Sectors: {sector_names}")
    
    t0 = time.time()
    cons_map = data_loader.get_multiple_sector_cons(sector_names)
    t1 = time.time()
    print(f"    Got {len(cons_map)} sector dataframes. Time: {t1-t0:.2f}s")
    
    print("[4] Merging Data...")
    for name in sector_names:
        cons = cons_map.get(name)
        merged = data_loader.merge_stock_data(cons, spot_data)
        print(f"    {name}: {len(merged)} stocks.")
        
    total_time = time.time() - start_time
    print(f"--- Verification Complete. Total Time: {total_time:.2f}s ---")

if __name__ == "__main__":
    verify_performance()
