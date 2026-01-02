# Implementation Plan: Historical Daily Limit-Up Export

## Goal
Enable users to export "Limit-Up" (ZhangTing) stock data for any specific historical date via the UI.

## User Review Required
> [!NOTE]
> Ensure AkShare's `stock_zt_pool_em` interface is stable for historical dates (verified for 20251219).

## Proposed Changes

### Data Layer (`data_loader.py`)
No major changes needed as `get_limit_up_pool(date)` already exists.
#### [MODIFY] [data_loader.py](file:///Users/lewisliu/Dev/playground/sector-alpha-hunter/data_loader.py)
- Ensure `get_limit_up_pool` properly handles `date` string format `YYYYMMDD`.
- Ensure caching key includes the `date` parameter.

### Logic Layer (`logic.py`)
#### [MODIFY] [logic.py](file:///Users/lewisliu/Dev/playground/sector-alpha-hunter/logic.py)
- Ensure `format_limit_up_export` works robustly even if some columns (like "Sector") are missing in historical data (defensive coding).

### UI Layer (`main.py`)
#### [MODIFY] [main.py](file:///Users/lewisliu/Dev/playground/sector-alpha-hunter/main.py)
- **Sidebar Update**:
    - Replace the simple button with a **Date Input** (`st.date_input`).
    - Default properly to today (or last trading day logic if possible, but today is simpler).
- **Export Logic**:
    - Convert user selected date `datetime.date` -> `YYYYMMDD` string.
    - Call `data_loader.get_limit_up_pool(date=formatted_date)`.
    - Generate CSV filename dynamically: `limit_up_{YYYYMMDD}.csv`.

## Verification Plan

### Automated Tests
- **Script**: `tests/verify_export_history.py`
    - **Step 1**: Fetch data for `20251219` (Known trading day). Assert `len(df) > 0`.
    - **Step 2**: Fetch data for `20251221` (Sunday). Assert `df.empty` or handled gracefully.
    - **Step 3**: Verify column existence in the returned DataFrame.

### Manual Verification
- **Run App**: `streamlit run main.py`
- **Action**: Select "Last Friday" in the date picker.
- **Action**: Click "Export".
- **Check**: Open CSV, verify date in filename and content accuracy.
