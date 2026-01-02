# Tech Stack Recommendation: Sector Alpha Hunter

> 核心理念: "All in Python". 利用 Python 强大的数据处理能力 + Streamlit 的快速交互能力，实现 低代码 (Low-Code) 但 高性能 (High-Performance) 的量化看板。
> 

## 1. 核心技术栈 (The Core Stack)

### 💻 编程语言: **Python 3.9+**

- **理由**: 量化金融的通用语言。生态极其丰富，从数据获取到清洗再到展示，全链路打通。
- **健壮性建议**: 使用 `Type Hinting` (类型提示) 编写代码，确保数据流转清晰。

### 📡 数据源接口: **AkShare**

- **角色**: 数据搬运工。
- **理由**:
    - **免费开源**: 社区维护极度活跃（Github Star 数千+），修复Bug速度快。
    - **覆盖全**: 完美支持东方财富（Eastmoney）的实时板块和个股资金流数据。
- **替代方案**: `Tushare Pro` (付费/积分制)，但在游资打板策略上，AkShare 对接的东财接口更贴近实战。

### ⚙️ 计算与逻辑引擎: **Pandas**

- **角色**: 数据清洗、排序、筛选、因子计算。
- **理由**:
    - **向量化计算**: 处理 5000 只股票的涨跌幅排序只需几毫秒。
    - **健壮性**: 极其成熟，处理 `NaN` (空值) 和异常数据非常方便。

### 🖥️ 前端交互 UI: **Streamlit**

- **角色**: 唯一的界面展示层。
- **理由**:
    - **最简单**: 不需要写一行 HTML/CSS/JavaScript。所有的 UI 组件（按钮、表格、侧边栏）都是 Python 函数。
    - **最健壮**: 自带数据缓存装饰器 (`@st.cache_data`)，完美解决重复请求导致 API 封号或页面卡顿的问题。
    - **可视化**: 原生支持 DataFrame 表格渲染，支持高亮、排序、下载 CSV。

## 2. 辅助工具与环境 (Utilities & Env)

### 📊 图表库 (可选): **Plotly Express**

- 如果不满足于 Streamlit 原生的图表，Plotly 可以提供交互式的 K 线图或散点图。
- *MVP阶段建议直接使用 Streamlit 原生表格和指标卡片即可，保持极简。*

### 📦 依赖管理: **requirements.txt**

不需要复杂的 Poetry 或 Docker (MVP阶段)，简单的 pip 即可。
核心依赖列表：

```
streamlit>=1.30.0
akshare>=1.12.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0  # 用于Excel导出支持(如果需要)

```

## 3. 为什么这套架构最“健壮”？

### A. 无状态架构 (Stateless)

- **传统Web开发**: 需要管理数据库连接池、Session、Cookies。
- **本方案**: Streamlit 是脚本式运行。每次用户交互（点击按钮），脚本从头运行一遍（配合缓存跳过耗时步骤）。这意味着**没有复杂的“状态同步”Bug**，重启即重置，非常适合高频迭代的量化工具。

### B. 无数据库依赖 (No-Database)

- **MVP策略**: 既然是“日内交易”或“盘中监控”，数据主要存于内存 (RAM)。
- **优势**: 只要你的电脑内存大于 4GB，Pandas 就可以轻松吞吐全市场数据。不需要维护 MySQL/Redis，极大降低了系统崩溃的概率。
- **持久化**: 仅需导出 CSV 留档即可。

### C. 接口容错 (API Fault Tolerance)

- 在代码层面，我们将封装一个 `Retrying` 机制。因为网络请求是最不可控的，我们将使用简单的 `try-except` 配合 `time.sleep` 来处理 AkShare 的网络波动，这是保证系统“不死”的关键。

## 4. 推荐的项目目录结构

```
sector-alpha-hunter/
├── main.py              # 🚀 启动入口 (Streamlit App)
├── logic.py             # 🧠 核心策略逻辑 (数据清洗、因子计算)
├── data_loader.py       # 📡 数据获取层 (封装 AkShare，含缓存机制)
├── requirements.txt     # 📦 依赖列表
├── design-document.md   # 📄 设计文档
└── README.md            # 📖 说明书

```

## 5. 总结

| 维度 | 你的选择 | 优势 |
| --- | --- | --- |
| **开发难度** | ⭐ | 极低，仅需 Python 基础 |
| **维护成本** | ⭐ | 无需运维数据库和前端服务器 |
| **扩展性** | ⭐⭐⭐ | 逻辑层与UI层解耦，后续可接入更多因子 |
| **稳定性** | ⭐⭐⭐⭐ | 依赖成熟大库，缓存机制保障流畅度 |

**结论**: 不要去碰 Flask/Django + React/Vue。对于量化工程师和游资工具，**Streamlit + Pandas** 是目前的**版本答案**。