# Progress Report

## 2024-12-22: Project Complete (MVP)

### Status
**MVP Delivered.** The project has successfully implemented all planned features, including a late-stage UI overhaul to meet modern aesthetic standards.

### Summary of Work
1.  **Architecture**: Established a clear 3-layer architecture (Data, Logic, UI).
    - **Data**: Solved the "Volume Ratio" missing data issue by merging global spot data with sector constituents.
    - **Logic**: Implemented robust screening for "Dragons" (Leaders) and "Laggards" (Followers) with Type Guarding.
    - **UI**: Iterated from a standard Streamlit layout to a custom "Linear-style" minimalist dashboard.

2.  **Key Features**:
    - Real-time Concept Sector Ranking.
    - Side-by-side view of limit-up stocks and potential catch-up stocks.
    - **Signal System**: Automatically flags low-position stocks with high Volume Ratio (>1.5).
    - **UX**: Compact single-page feel, "Yi" unit conversion throughout, clean typography.

3.  **Verification**:
    - Comprehensive unit tests for Data and Logic layers (`tests/`).
    - Manual verification of UI responsiveness and data accuracy.

### Artifacts Created
- `main.py`: The application.
- `logic.py`: Business logic library.
- `data_loader.py`: Data access library.
- `memory-bank/`: Full project documentation (Architecture, Design, Plan).
- `README.md`: Quick start guide.

### Future Improvements (Post-MVP)
- [x] **Multi-threading**: Improve data fetching speed for large sectors.
- **WebSocket**: Replace polling with push notifications (if API supports).
- **Push Notifications**: Integrate Feishu/DingTalk alerts for signals.

## 2024-12-22: Performance Refinement

### Status
**Optimized.** Addressed critical bottlenecks in data loading.

### Improvements
1.  **Parallel Data Fetching**: 
    - Replaced sequential sector scanning with concurrent fetching (`ThreadPoolExecutor`).
    - Reduced load time from ~15s to ~5s for 9 sectors.
2.  **Global Data Caching**:
    - Implemented "Fetch Once" strategy for market spot data, eliminating redundant API calls.
3.  **Refined UX**:
    - Detailed progress indicators during data loading phase.
4.  **New Feature (Export)**:
    - Added "Download Daily Limit-Up Data" to sidebar.
    - Exports clean CSV with Sector/Dragon Height/Volume data.
    - **Refinement**: Formatted CSV with 2-decimal precision and "Billions (亿)" units for readability.
## 2025-12-22: Signal System Refinement - Phase 1

### Status
**Infrastructure Ready.** Initiated the transition to a modular signal system.

### Improvements
1.  **Data Layer Upgrade**:
    - Modified `data_loader.merge_stock_data` to support **Context Injection**. It now accepts `sector_gain` and broadcasts it to all stock rows.
    - Enables "Relative Strength" signals (e.g., Stock vs Sector deviation) in the Logic layer.
2.  **Logic Layer Hardening**:
    - Enhanced `clean_data` to strictly enforce Float types for `Market Cap`.
    - Added strict validation to **drop rows** with invalid/NaN Market Cap (prevents false "Small Cap" signals caused by missing data).
    - Verified with new unit tests `tests/test_data_loader_sector_gain.py` and `tests/test_logic_dtypes.py`.

## 2025-12-22: Signal System Refinement - Phase 2

### Status
**Core Engine Operational.** The modular signal registry and composite filter logic are implemented and tested.

### Improvements
1.  **Signal Registry**: Implemented `SIGNAL_REGISTRY` in `logic.py` to manage modular signal definitions.
2.  **Composite Logic**: Added `apply_signals` function supporting **Strict AND** logic for combining multiple signals.
3.  **Validation**: Added unit tests `tests/test_signal_registry.py` and `tests/test_apply_signals.py` verifying the decoupling and filtering mechanics.

## 2025-12-22: Signal System Refinement - Phase 3

### Status
**Core Signals Implemented.** The first batch of selectable quantitative signals is now live in the engine (Logic Layer).

### New Signals
1.  **Volume Ratio Anomaly (`vol_ratio`)**:
    - Selects stocks with `Volume Ratio > 1.5`, indicating abnormal liquidity ignition.
2.  **Sector Deviation (`sector_divergence`)**:
    - Selects stocks where `Sector Gain - Stock Gain > 3.0%`. Identifies "coiled springs" in hot sectors.
3.  **Market Cap Z-Score (`small_cap`)**:
    - Selects the bottom 20% by Market Cap. Targets high-elasticity small-caps.

## 2025-12-23: Signal System Refinement - Phase 4 (UI Integration)

### Status
**Feature Complete.** The "Signal Lab" is now live in the Sidebar, allowing users to interactively compose strategies.

### Improvements
1.  **Sidebar Signal Lab**: Added an expander "🎯 信号工坊" with checkboxes for the 3 Phase 1 signals.
2.  **Dynamic Filtering**: Wired the UI checkboxes to `logic.apply_signals`. Selecting multiple signals applies a strict "AND" filter.
3.  **Context Injection**: Updated `main.py` loop to grab `sector_gain` from the Ranking DF and inject it into the Stock Data pipeline, enabling Relative Strength logic.
4.  **Cleanup**: Removed the deprecated `add_signals` function and hardcoded "Red Circle" logic. The tool now strictly filters laggards based on user criteria.

## 2025-12-23: Signal System Refinement - Phase 5 (Cleanup & Polish)

### Status
**Refinement Complete.** Codebase verified for cleanliness and architecture consistency.

### Improvements
1.  **Code Hygiene**: Verified removal of legacy functions (`add_signals`) and unused imports.
2.  **Documentation**: Updated Architecture and Progress detailed logs.
3.  **Final Verification**: valid UI and Logic separation confirmed.

## 2025-12-22: Historical Limit-Up Export Feature

### Status
**Completed.** Users can now download limit-up data for any historical date.

### Improvements
1.  **UI Interaction**: Added a "Use Historical Date" toggle and date picker in the sidebar.
2.  **Robust Data Fetching**: Updated `data_loader.get_limit_up_pool` to handle specific date requests securely.
3.  **Data Processing**: Rewrote `logic.format_limit_up_export` to be defensive against missing columns and handle unit conversions properly.
4.  **Verification**: Verified with `tests/verify_export_history.py` covering valid past dates and non-trading days.
