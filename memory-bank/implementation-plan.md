# Implementation Plan - Sector Alpha Hunter (MVP)

This document outlines the step-by-step instructions for building the **Sector Alpha Hunter**.
**Objective:** Build a Python-based real-time A-share market hotspot tracking tool.
**UI Language:** Simplified Chinese (简体中文).

## User Review Required

> [!IMPORTANT]  
> **Data Strategy Strategy**: `Volume Ratio (量比)` is **not** available in the sector stock list API.
> **Solution**: We will implemented a "Merge Strategy":
> 1. Fetch Sector Stocks (Code, Name, Price).
> 2. Fetch **Global Spot Data** (`ak.stock_zh_a_spot_em`) which contains Volume Ratio.
> 3. Merge both datasets on `Stock Code`.

## Phase 1: Environment & Project Structure

- [ ] **Step 1.1: Initialize Project Files**
    - **Action**: Create the following empty files:
        - `main.py` (Streamlit Entry)
        - `logic.py` (Business Logic)
        - `data_loader.py` (Data Access Object)
        - `requirements.txt` (Dependencies)
    - **Validation**: Run `ls -R` to verify file creation.

- [ ] **Step 1.2: Define Dependencies**
    - **Action**: Create `requirements.txt` with:
        - `streamlit`
        - `akshare`
        - `pandas`
        - `numpy`
    - **Validation**: Run `pip install -r requirements.txt` and ensure "Successfully installed".

## Phase 2: Data Layer (`data_loader.py`)

- [ ] **Step 2.1: Implement Sector Ranking Fetcher**
    - **Action**: In `data_loader.py`, define `get_sector_ranking(top_n=5)`.
        - call `ak.stock_board_concept_name_em()`.
        - Sort by `涨跌幅` (descending).
        - Return top `n` rows with columns: `板块名称`, `板块代码`, `涨跌幅`.
    - **Validation**: Create `tests/test_step_2_1.py`. Call the function. Assert returned object is a DataFrame and `len(df) == top_n`.

- [ ] **Step 2.2: Implement Sector Stocks Fetcher**
    - **Action**: In `data_loader.py`, define `get_stocks_in_sector(sector_name)`.
        - Call `ak.stock_board_concept_cons_em(symbol=sector_name)` to get stock codes.
        - **Data Merge**: Call `ak.stock_zh_a_spot_em()` to get spot data (including `量比`).
        - Merge the two DataFrames on `代码`.
        - Return cleaned DataFrame with columns: `代码`, `名称`, `最新价`, `涨跌幅`, `总市值`, `量比`, `换手率`.
    - **Validation**: Create `tests/test_step_2_2.py`. Call with a known hot sector (e.g., "锂电池"). Assert `量比` column exists and is not all NaN.

## Phase 3: Logic Layer (`logic.py`)

- [ ] **Step 3.1: Data Cleaning Utility**
    - **Action**: In `logic.py`, define `clean_data(df)`.
        - Ensure numeric columns (`最新价`, `涨跌幅`, `量比`, `总市值`, `换手率`) are float type.
        - Handle any parsing errors (coerce strings to numbers).
    - **Validation**: Create `tests/test_step_3_1.py`. Pass a DataFrame with string numbers ("10.5"). Assert dtypes are float.

- [ ] **Step 3.2: Implement Dragon Screener (龙头筛选)**
    - **Action**: In `logic.py`, define `filter_dragons(df)`.
        - Filter: `涨跌幅` >= 9.0.
        - Filter: `名称` does not contain "ST".
        - Sort: Descending by `总市值`.
    - **Validation**: Create `tests/test_step_3_2.py`. Pass a mock DataFrame with a mix of limit-up stocks and ST stocks. Assert result only contains valid limit-up stocks.

- [ ] **Step 3.3: Implement Laggard Screener (补涨筛选)**
    - **Action**: In `logic.py`, define `filter_laggards(df, max_cap_billion=100)`.
        - Filter: 0 <= `涨跌幅` <= 4.0.
        - Filter: `总市值` < `max_cap_billion` * 100,000,000 (Convert billions to unit).
        - Filter: `换手率` > 3.0.
    - **Validation**: Create `tests/test_step_3_3.py`. Pass mock data. Verify only small-cap, low-gain, high-turnover stocks remain.

- [ ] **Step 3.4: Signal Generator**
    - **Action**: In `logic.py`, define `add_signals(df)`.
        - Add column `信号`.
        - Logic: If `量比` > 1.5, set `信号` = "🔴". Else empty.
    - **Validation**: Create `tests/test_step_3_4.py`. Pass mock laggards. Verify confirmed rows have the red circle.

## Phase 4: UI Layer (`main.py`)

- [ ] **Step 4.1: Basic Streamlit Layout**
    - **Action**: In `main.py`:
        - Set Page Title: "板块轮动猎手".
        - Add Sidebar with:
            - Slider: "板块数量" (Key: `top_n`, Default: 3).
            - Number Input: "市值上限(亿)" (Key: `max_cap`, Default: 100).
            - Button: "刷新数据".
    - **Validation**: Run `streamlit run main.py`. Verify sidebar inputs appear and labels are in Chinese.

- [ ] **Step 4.2: Display Sector Ranking**
    - **Action**: In `main.py`:
        - Call `data_loader.get_sector_ranking(top_n)`.
        - Display result as a Metric Row or DataFrame at the top.
    - **Validation**: Run app. Change slider from 3 to 5. Verify the list grows.

- [ ] **Step 4.3: Implement Sector Tabs**
    - **Action**: In `main.py`:
        - Create tabs using `st.tabs()` for each top sector.
        - Inside each tab:
            - Call `data_loader.get_stocks_in_sector`.
            - Apply `logic.clean_data`.
            - Apply `logic.filter_dragons` -> Display "🔥 龙头梯队" table.
            - Apply `logic.filter_laggards` -> Apply `logic.add_signals`.
            - Sort Laggards: Rows with "🔴" signal first.
            - Display "🚀 补涨挖掘" table.
    - **Validation**: Run app. Click different tabs. Verify tables load with data.

- [ ] **Step 4.4: CSV Export Feature**
    - **Action**: In `main.py` inside the Laggards section:
        - Add `st.download_button` to download the Laggard DataFrame as `laggards.csv`.
    - **Validation**: Run app. Click download. Open CSV to verify content matches UI.

## Phase 5: Documentation & Handover

- [ ] **Step 5.1: Finalize Documentation**
    - **Action**: Update `README.md` with usage instructions.
    - **Action**: Update `architecture.md` with the final data flow diagram.
    - **Validation**: visual check of markdown files.