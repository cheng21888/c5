import akshare as ak
import datetime

def test_historical_zt_pool():
    # Last Friday was 2025-12-19 (Today is 2025-12-22 Monday)
    target_date = "20251219"
    print(f"Testing for date: {target_date}")
    try:
        df = ak.stock_zt_pool_em(date=target_date)
        if df.empty:
            print("Received empty DataFrame")
        else:
            print(f"Found {len(df)} limit-up stocks")
            print(df.head())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_historical_zt_pool()
