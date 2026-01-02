# Core Signals: The "Alpha Hunter" Factor Library

## 0. Design Philosophy: Quant x Hot Money
To capture "Sector Alpha" robustly, we combine two schools of thought:
1.  **Top Quant (e.g., High-Flyer - 幻方)**: Focus on **Relative Strength**, **Mean Reversion**, and **Abnormal Structure**. They ask: "Is this stock statistically dragging behind its peers unexpectedly?"
2.  **Top Hot Money (e.g., 游资 - 炒家)**: Focus on **Attention**, **Liquidity**, and **Sentiment Reversal**. They ask: "Is the Smart Money initiating a new wave here?"

**Robustness Check**: Single factors often fail (e.g., high volume can be selling). **Robustness comes from "Context" (The Sector is Strong) + "Resonance" (Multiple Factors Align).**

## 1. The Factor Library (Selectable Modules)

We design these as independent boolean filters or scoring components that can be toggled.

### Module A: Liquidity Awakening (The "Ignition")
*Low volatility turning into high volatility.*

- **[Default] Volume Ratio Anomaly (量比突变)**
    - **Logic**: `Volume Ratio > 1.5` (Mild) or `> 2.5` (Aggressive).
    - **Why**: Indicates new capital entering a quiet stock.
    - **Robustness**: High. The most direct proxy for "Change of State".
- **[Hot Money] Call Auction Explosion (竞价抢筹)**
    - **Logic**: `9:25-9:30 Volume` > `Yesterday Average 5min Volume` * 5.
    - **Why**: "The early bird gets the worm." Smart money acts first.
    - **Robustness**: Medium. Can be faked (fake orders), needs checking opening price stability.

### Module B: Relative Value (The "Catch-up")
*Statistical Arbitrage within the Sector.*

- **[Quant] Sector Deviation (板块背离度)**
    - **Logic**: `Sector Gain` - `Stock Gain` > 3%. (e.g., Sector +4%, Stock +0.5%).
    - **Why**: In a strong sector, correlation forces *all* boats to rise eventually. A heavy divergence implies a coiled spring.
    - **Robustness**: High (in Bull Market). Low (in Bear Market - weak stocks are just weak).
- **[Quant] Market Cap Z-Score (市值下沉)**
    - **Logic**: Rank stocks by Market Cap. Select bottom 20%.
    - **Why**: "Small implies High Elasticity". In a hot sector, 20cm (20%) limit-ups often come from the smallest names.

### Module C: Smart Money Flow (The "Confirmation")
*Real-money voting.*

- **[Pro] Main Force Net Inflow (主力净流入)**
    - **Logic**: `Super Large + Large Orders Net` > 10 Million RMB (or > 1% of Float).
    - **Why**: Retail traders don't buy in 10,000 lot clips.
    - **Robustness**: Very High. Hard to fake real-money direction.
- **[Pro] Panic Wash Divergence (恐慌盘背离)**
    - **Logic**: Price drops (-2%), but `Net Inflow` is Positive.
    - **Why**: "Chengjie" (Passing the torch). Institutions absorbing panic selling.

### Module D: Technical Structure (The "Layout")
*The chart preparation.*

- **[Trend] N-Day Consolidation Breakout (平台突破)**
    - **Logic**: High `Close` > `Max(Close of last 10 days)`.
    - **Why**: No "Overhead Supply" (Hold-up/Trapped chips).
- **[Trend] Moving Average Support (趋势借力)**
    - **Logic**: Low price touched MA10 or MA20 today and rebounded.

## 2. Signal Composability (The "Recipes")

Users should be able to "Check" boxes to combine these.

**Recipe 1: "Morning Ambush" (早盘潜伏)**
*   [x] Call Auction Explosion
*   [x] Sector Deviation
*   *(Goal: Catch the first movement of a laggard)*

**Recipe 2: "Mid-day Safety" (盘中稳健)**
*   [x] Volume Ratio Anomaly
*   [x] Main Force Net Inflow
*   [x] Moving Average Support
*   *(Goal: Buy confirmed strength that is safe)*

**Recipe 3: "20cm Lotto" (小票博弈)**
*   [x] Market Cap Z-Score (Smallest)
*   [x] Volume Ratio > 2.0
*   *(Goal: High risk/reward on ChiNext/Star market)*

## 3. Data Requirements
To support these, we need to upgrade `data_loader.py`:
- [x] Basic Price/Volume (Done)
- [ ] **Intraday Fund Flow**: `ak.stock_individual_fund_flow` (Crucial for Module C).
- [ ] **History Bars**: Need last N days for "Consolidation" and "MA" logic.
