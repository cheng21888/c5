# Signal Refinement Plan: Modular Signal Architecture

## 1. Analysis & Assumptions
*   **Consistency**: The plan aligns with the "Hot Money" vision in `core_signals.md` but focuses on Phase 1 construction.
*   **Assumption - Logic**: We will implement **Strict AND** logic for the filter (intersection of selected signals).
*   **Assumption - Data**: We need to pass "Sector Gain" down to the stock logic to calculate deviation.
*   **Assumption - Scope**: "Market Cap Z-Score" is calculated relative to the **Sector**, not the entire market.

## 2. Phase 1: Data Layer Preparation
*Ensure all necessary raw data is available for the signals.*

### Step 1.1: Expose Sector Gain
*   **Context**: "Sector Deviation" requires `Sector Gain` - `Stock Gain`. Currently, `get_stocks_in_sector` only returns stock data.
*   **Action**: Modify `data_loader.py` -> `get_stocks_in_sector(sector_name, sector_gain=None)`.
    *   Allow passing an optional `sector_gain` float.
    *   If provided, broadcast this value to a new column `sector_pct_chg` in the returned DataFrame.
*   **Verification**:
    *   Test: `tests/test_data_loader_sector_gain.py`
    *   Run: Call `get_stocks_in_sector("Battery", sector_gain=5.0)`.
    *   Check: Verify new column `sector_pct_chg` exists and all values equal `5.0`.

### Step 1.2: Standardize Data Types
*   **Context**: Ensure `market_cap` is float (standardized units) for Z-Score calculation.
*   **Action**: In `logic.py` -> `clean_data`, ensure `总市值` is explicitly converted to numeric, coercing errors to NaN, and dropped if NaN.
*   **Verification**:
    *   Test: `tests/test_logic_dtypes.py`
    *   Run: Pass a DataFrame with string market caps.
    *   Check: Verify `df['总市值'].dtype` is float.

## 3. Phase 2: Signal Engine Architecture
*Build the "Plug-and-Play" infrastructure.*

### Step 2.1: Define Signal Protocol
*   **Action**: In `logic.py`, define a `Signal` TypedDict or Class structure:
    *   `id` (str): Unique key (e.g., 'sig_vol_ratio').
    *   `name` (str): Display name (e.g., '量比爆发').
    *   `func` (Callable): Function accepting `df` and returning `pd.Series(bool)`.
*   **Verification**:
    *   Test: None (Structure definition).

### Step 2.2: Implement Signal Registry
*   **Action**: In `logic.py`, create a dictionary `SIGNAL_REGISTRY` to hold all available signals.
*   **Action**: Create a helper function `get_active_signals(selected_ids: List[str])` that returns the list of signal objects.
*   **Verification**:
    *   Test: `tests/test_signal_registry.py`
    *   Run: Register a dummy signal. Call `get_active_signals` with its ID.
    *   Check: Verify the function object is returned correctly.

### Step 2.3: Implement Composite Filter Function
*   **Action**: In `logic.py`, create `apply_signals(df, selected_signal_ids)`.
    *   Start with a generic `mask = True`.
    *   Iterate through `selected_signal_ids`.
    *   Look up the function in `SIGNAL_REGISTRY`.
    *   Apply `mask = mask & func(df)`.
    *   Return `df[mask]`.
*   **Verification**:
    *   Test: `tests/test_apply_signals.py`
    *   Run: Create a generic DF with 10 rows. Create two dummy signals (Row < 5, Row > 2).
    *   Check: Verify result has rows 3 and 4 only (Intersection).

## 4. Phase 3: Signal Implementation (Phase 1 Pack)
*Implement the actual trading logic.*

### Step 3.1: Signal - Volume Ratio Anomaly (Base)
*   **Action**: Define `sig_vol_ratio(df)` in `logic.py`.
    *   Logic: `df['量比'] > 1.5`.
    *   Register as `vol_ratio`.
*   **Verification**:
    *   Test: `tests/test_sig_vol.py`
    *   Run: Pass DF with values 1.0 and 2.0.
    *   Check: Only 2.0 remains.

### Step 3.2: Signal - Sector Deviation (Catch-up)
*   **Action**: Define `sig_sector_divergence(df)` in `logic.py`.
    *   Logic: `(df['sector_pct_chg'] - df['涨跌幅']) > 3.0`.
    *   Prerequisite: Ensure `sector_pct_chg` column exists (from Step 1.1).
    *   Register as `sector_divergence`.
*   **Verification**:
    *   Test: `tests/test_sig_div.py`
    *   Run: Sector +5%. Stock A +1% (Diff 4 > 3), Stock B +4% (Diff 1 < 3).
    *   Check: Stock A is kept.

### Step 3.3: Signal - Market Cap Z-Score (Small Cap)
*   **Action**: Define `sig_small_cap(df)` in `logic.py`.
    *   Logic: Calculate quantile 0.2 of `总市值` within the current DF.
    *   Return `df['总市值'] <= quantile_0.2`.
    *   Register as `small_cap`.
*   **Verification**:
    *   Test: `tests/test_sig_cap.py`
    *   Run: Pass 10 stocks with Caps 10..100.
    *   Check: Verify only the smallest 2 are selected.

## 5. Phase 4: UI Integration
*Connect the engine to the dashboard.*

### Step 5.1: Add "Signal Lab" Sidebar
*   **Action**: In `main.py` Sidebar:
    *   Add `st.expander("🎯 信号工坊 (Signal Lab)")`.
    *   Inside, add `st.checkbox` for each signal in `SIGNAL_REGISTRY`.
    *   Default "Volume Ratio" to Checked.
*   **Verification**:
    *   Manual: Run app. Verify the expander and checkboxes appear.

### Step 5.2: Wire User Selection to Logic
*   **Action**: In `main.py` (Main Loop):
    *   Collect list of `selected_signal_ids` from checkboxes.
    *   Pass `sector_gain` (from the Ranking step) into `get_stocks_in_sector`.
    *   Replace the old `logic.add_signals` call with the new `logic.apply_signals(df, selected_signal_ids)`.
    *   *Note*: This changes the behavior from "Highlighting" to "Filtering".
*   **Verification**:
    *   Manual: Select "Small Cap" only. Verify the resulting table only shows small stocks. Select "Volume Ratio". Verify strict filtering.

## 6. Phase 5: Cleanup & Polish
*   **Step 6.1**: Remove the hardcoded `add_signals` function from `logic.py` once fully replaced.
*   **Step 6.2**: Ensure column names in the UI are clean (Remove any intermediate calc columns like `sector_pct_chg` from the final display).
