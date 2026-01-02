# Sector Alpha Hunter (MVP) - Project Context

## Project Overview
**Sector Alpha Hunter** is a Python-based tool designed to assist quantitative traders and short-term investors in identifying daily market hotspots in the A-share market. It automates the screening of "leading" (Dragon) and "catch-up" (Laggard) stocks within trending sectors.

**Core Value:**
*   **Visual Dashboard:** Web-based interface via Streamlit for real-time monitoring.
*   **Clear Signals:** Highlights high-potential catch-up stocks using "Volume Ratio" and "Market Cap" factors.
*   **Objective:** Removes emotional bias by strictly adhering to quantitative logic.

## Technology Stack
*   **Language:** Python 3.9+
*   **Data Source:** `AkShare` (Eastmoney real-time APIs)
*   **Data Processing:** `Pandas`
*   **UI/Frontend:** `Streamlit`
*   **Deployment:** Local execution (Stateless, No-Database)

## Architecture & Logic
1.  **Data Layer:** Fetches real-time sector and stock data using AkShare.
2.  **Logic Layer:**
    *   **Sector Scan:** Ranks sectors by % change.
    *   **Stock Screening:**
        *   **Dragons:** High % change (>=9%), large market cap.
        *   **Laggards:** Low % change (0-4%), small market cap (<100亿), active turnover.
    *   **Signal Generation:** Flags stocks with Volume Ratio > 1.5 in strong sectors (>2.5%).
3.  **UI Layer:** Displays data in a Streamlit dashboard with interactive tables and CSV export.

## Proposed Directory Structure
```
sector-alpha-hunter/
├── main.py              # Entry point (Streamlit App)
├── logic.py             # Core strategy logic (Cleaning, Factors)
├── data_loader.py       # Data fetching (AkShare wrapper with caching)
├── requirements.txt     # Dependencies
├── design-document.md   # Design details
├── tech-stack.md        # Tech stack details
└── README.md            # Documentation
```

## Building and Running
*   **Prerequisites:** Python 3.9+
*   **Setup:**
    ```bash
    pip install -r requirements.txt
    ```
*   **Run:**
    ```bash
    streamlit run main.py
    ```

## Development Status
*   **Current Phase:** Design & Planning
*   **Next Steps:**
    1.  Initialize project environment.
    2.  Implement `data_loader.py` to fetch Eastmoney data.
    3.  Implement `logic.py` for screening algorithms.
    4.  Build `main.py` with Streamlit UI.

# IMPORTANT:
# Always read memory-bank/@architecture.md before writing any code. Include entire database schema.
# Always read memory-bank/@design-document.md before writing any code.
# After adding a major feature or completing a milestone, update memory-bank/@architecture.md and memory-bank/@progress.md.
# I already create a venv for you under: /Users/lewisliu/Dev/playground/sector-alpha-hunter/venv/, use this venv.