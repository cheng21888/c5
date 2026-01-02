# A-Share Sector Alpha Hunter (A股板块轮动猎手)
📝 [中文文档](./README_CN.md)
**Sector Alpha Hunter** allows quantitative traders to identify daily A-share market hotspots and potential catch-up stocks ("Laggards") in real-time.


## Disclaimer

> - ⚠️ **Stock market investment carries risks, please invest with caution.**
> - ⚠️ **This project is for learning purposes only, please do not use it for actual trading.**
> - 🧪 **Vibe Coding Alert**: This project was built through "Vibe Coding". Use with curiosity and care.


## Demo
![demo](public/demo.png)

## Features

- **Real-time Sector Scan**: Fetches top performing concept boards from Eastmoney.
- **Dragon vs Laggard**: Automatically separates stocks into "Leaders" (Limit-up) and "Followers" (Low gain, high activity).
- **Signal Lab (Advanced Filtering)**: Selectable quantitative factors to narrow down the best candidates:
    - **Volume Ratio (>1.5)**: Detects abnormal liquidity ignition.
    - **Sector Deviation**: Identifies "coiled springs" that have lagged behind the hot sector's move.
    - **Small Cap (Bottom 20%)**: Targets high-elasticity small-caps within the sector pool.
- **Historical Export**: Download daily limit-up (涨停) data for any historical date in a clean, Excel-friendly CSV format.
- **Modern UI**: Clean, single-page dashboard inspired by Linear/OpenAI aesthetics.

## Installation

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

Run the Streamlit dashboard:

```bash
streamlit run main.py
```

### 1. Market Monitoring
- The top metrics bar shows the current leading sectors.
- Each tab contains the constituents of that sector, split into **Dragons** (high performers) and **Laggards** (potential catch-ups).

### 2. Signal Lab (Sidebar)
Use the **Signal Lab** in the sidebar to apply strict quantitative filters:
- **Strict "AND" Logic**: If multiple signals are selected, only stocks satisfying **ALL** criteria will be displayed.
- **Dynamic Filtering**: Adjust filters in real-time to find higher-probability entries.

### 3. Historical Export
- Toggle "Use Historical Date" in the sidebar.
- Pick a date and click "Export Limit-Up Data".
- Download a formatted CSV containing ticker, price, height (number of limit-ups), and logic for the limit-up.

### Parameters
- **Top N**: Number of hot sectors to scan (1-10).
- **Market Cap Limit**: Max market cap for laggard candidates (default 200亿).

## Project Structure

- `main.py`: UI Entry point (Streamlit).
- `logic.py`: Signal Engine and Core Algorithms.
- `data_loader.py`: Data fetching (AkShare) with caching & concurrency.
- `memory-bank/`: Full documentation system (Architecture, Progress, Signal Logic).
