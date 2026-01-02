import akshare as ak
import pandas as pd
import streamlit as st
from datetime import date, datetime
import os
import sys

# 只需要每天执行一次，获取成交量分时比例
@st.cache_data(ttl=42000)
def get_amount_curve(ndays):
    """
    获取指定天数的成交量曲线。

    参数:
    ndays (int): 要获取的天数。

    返回:
    list: 包含每15分钟成交量百分比的列表。

    异常:
    如果在获取或处理数据时发生错误，将记录错误并抛出异常。

    功能描述:
    1. 从 akshare 获取上证和深证的分钟数据。
    2. 合并数据并计算总成交量。
    3. 过滤掉当天的数据，只保留指定天数的数据。
    4. 计算每15分钟的成交量占当天总成交量的百分比。
    5. 生成并返回成交量曲线。

    日志:
    - 记录获取数据的开始和成功信息。
    - 记录数据处理完成的信息。
    - 记录百分比数据计算成功的信息。
    - 记录生成成交量曲线的信息。
    - 记录任何发生的错误。
    """
    try:
        stock_zh_a_minute_df_sh = ak.stock_zh_a_minute(
            symbol="sh000001", period="15", adjust="qfq"
        )
        stock_zh_a_minute_df_sz = ak.stock_zh_a_minute(
            symbol="sz399001", period="15", adjust="qfq"
        )
        df = pd.concat([stock_zh_a_minute_df_sh, stock_zh_a_minute_df_sz], axis=1)
        df2 = df.iloc[:, [0, 5, 11]].copy(deep=True)
        df2.columns = ["day", "amount_sh", "amount_sz"]
        df2["amount_sh"] = pd.to_numeric(df2["amount_sh"])
        df2["amount_sz"] = pd.to_numeric(df2["amount_sz"])
        df2["date"] = pd.to_datetime(df2["day"])  # format='%Y-%m-%d %H:%M:%S'
        df2["totalamount"] = df2.apply(
            lambda x: (x["amount_sh"] + x["amount_sz"]), axis=1
        )
        df2.drop(["day"], axis=1, inplace=True)
        df2 = df2[
            df2["date"] < datetime.combine(date.today(), datetime.min.time())
        ]  # 获取本日之前15分钟数据，当日不要。
        df2 = df2.tail(ndays * 16)  # 取n天的数据，一天16个数据。
        df_all = pd.DataFrame()
        for i in range(ndays):
            df_range = df2.iloc[i * 16 : (i + 1) * 16].copy()  # 创建副本
            day_amount = df_range.totalamount.sum()
            df_range.loc[:, "pct"] = df_range.apply(
                lambda x: (x["totalamount"] / day_amount), axis=1
            )
            df_all = pd.concat([df_all, df_range])
        df_all = df_all.reset_index()
        curve = []
        for j in range(16):
            curve.append(df_all[df_all.index % 16 - j == 0].pct.mean())
        return curve
    except Exception as e:
        raise


@st.cache_data(ttl=300)
def get_estimate_amount(minutes, vol=None):
    """
    估算成交量。

    参数：
    minutes (int): 已交易的分钟数。
    vol (int, 可选): 指定的成交量。如果未提供，将自动获取。

    返回：
    int: 估算的成交量。如果发生错误，返回0。

    异常：
    KeyError: 当计算累计比例时发生键错误。
    ZeroDivisionError: 当估算成交量时发生除零错误。

    日志：
    - 记录开始估算成交量的信息。
    - 记录计算得到的累计比例。
    - 记录自动获取的成交量（如果未指定）。
    - 记录估算的成交量。
    - 记录计算累计比例时的键错误警告。
    - 记录估算成交量时的除零错误。
    """
    curve = get_amount_curve(3)
    df = pd.DataFrame(curve, columns=["amount"])
    t = minutes // 15
    if t > 15:
        t = 15
    remaining_minutes = minutes % 15

    try:
        a = df[0:t]["amount"].sum() + df.loc[t] * remaining_minutes / 15
    except KeyError:
        a = df[0:t]["amount"].sum()
        raise

    if not vol:
        total_amount = get_a_amount()
        vol = total_amount[0] + total_amount[1]
    try:
        estimated_amount = int(vol / a.iloc[0]) if vol > 0 else 0
        return estimated_amount
    except ZeroDivisionError:
        return 0


@st.cache_data(ttl=300)
def get_n_day_avg_amount(n):
    """
    获取上证和深证指数最近 n 个交易日的平均成交额。

    参数:
        n (int): 要计算的交易日天数。

    返回:
        tuple: 包含上证和深证指数平均成交额的元组，格式为 (sh_avg_amount, sz_avg_amount)。
    """
    try:
        stock_zh_a_daily_df_sh = ak.stock_zh_index_daily_em(symbol="sh000001")
        stock_zh_a_daily_df_sz = ak.stock_zh_index_daily_em(symbol="sz399001")

        sh_amount = int(stock_zh_a_daily_df_sh["amount"].iloc[-6:-1].mean())
        sz_amount = int(stock_zh_a_daily_df_sz["amount"].iloc[-6:-1].mean())
        return sh_amount + sz_amount
    except Exception as e:
        return 0, 0


@st.cache_data(ttl=300)
def get_index_price(symbol):
    try:
        index_data = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
        index_value = int(index_data[index_data["代码"] == symbol]["最新价"].values[0])
        return index_value
    except Exception as e:
        exc_type, exc_obj, tb = sys.exc_info()
        fname = os.path.split(tb.tb_frame.f_code.co_filename)[1]
        return 0


def get_index_amount(symbol):
    try:
        df_sh = ak.stock_zh_index_spot_em(symbol="上证系列指数")
        df_sz = ak.stock_zh_index_spot_em(symbol="深证系列指数")
        df_csi = ak.stock_zh_index_spot_em(symbol="中证系列指数")
        df_vip = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
        df = pd.concat([df_sh, df_sz, df_csi, df_vip], axis=0)

        index_value = int(df[df["代码"] == symbol]["成交额"].values[0])
        return index_value
    except Exception as e:
        raise


# 获取当前成交额
@st.cache_data(ttl=300)
def get_a_amount() -> tuple[float, float]:
    """
    获取上证和深证指数的成交量。

    该函数使用 akshare 库获取当前上证指数和深证指数的成交量。
    如果当前时间不在交易时间内，则将全局的 TTL 变量设置为 3600 秒。

    返回:
        tuple: 包含上证和深证指数成交量的元组，格式为 (sh_amount, sz_amount)。

    异常:
        KeyError: 如果在获取的数据中未找到预期的股票代码（上证为 "000001"，深证为 "399001"）。
    """

    try:
        spot_df = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
    except Exception as e:
        return 0, 0

    # 检查是否存在对应的指数代码
    sh_mask = spot_df["代码"] == "000001"
    sz_mask = spot_df["代码"] == "399001"

    if not sh_mask.any() or not sz_mask.any():
        return 0, 0

    sh_amount = spot_df[sh_mask]["成交额"].iloc[0]  # 使用iloc[0]代替values[0]
    sz_amount = spot_df[sz_mask]["成交额"].iloc[0]  # 深证成交额
    if pd.isna(sh_amount) or pd.isna(sz_amount):
        return 0, 0

    return sh_amount, sz_amount


@st.cache_data(ttl=300)
def middle_price_change():
    """
    计算所有股票的中位数涨幅。

    该函数获取A股的实时交易数据，并计算所有股票的中间涨幅（即按涨幅排序后位于中间的股票涨幅）。

    返回:
        float: 中间股票涨幅。如果数据为空，则返回0。
    """
    df = ak.stock_zh_a_spot_em()
    if df.empty:
        return 0

    # 按涨幅排序
    df_sorted = df.sort_values("涨跌幅")

    # 计算中间位置
    middle_index = len(df_sorted) // 2

    # 获取中间涨幅
    middle_price_change = df_sorted.iloc[middle_index]["涨跌幅"]
    return middle_price_change


@st.cache_data(ttl=300)
def count_limit_up_stocks():
    """
    计算涨停板股票的数量。

    该函数获取A股的实时交易数据，并计算涨停板（涨幅达到10%或以上）的股票数量。

    返回:
        int: 涨停板股票的数量。如果数据为空，则返回0。
    """
    df = ak.stock_zh_a_spot_em()
    if df.empty:
        return 0

    # 计算涨停板股票的数量，30 开头和 68 开头的是 20% 涨停，其他是 10% 涨停
    df["涨停板"] = df.apply(
        lambda row: (
            row["涨跌幅"] >= 19.9
            if row["代码"].startswith(("30", "68"))
            else row["涨跌幅"] >= 29
            if row["代码"].startswith("8")
            else row["涨跌幅"] >= 9.9
        ),
        axis=1,
    )
    limit_up_stocks = df[df["涨停板"] & ~df["代码"].str.startswith("8")].shape[0]
    return limit_up_stocks


@st.cache_data(ttl=300)
def count_limit_down_stocks():
    """
    计算跌停板股票的数量。

    该函数获取A股的实时交易数据，并计算跌停板（跌幅达到10%或以上）的股票数量。

    返回:
        int: 跌停板股票的数量。如果数据为空，则返回0。
    """
    df = ak.stock_zh_a_spot_em()
    if df.empty:
        return 0

    # 计算跌停板股票的数量，30 开头和 68 开头的是 20% 跌停，其他是 10% 跌停
    df["跌停板"] = df.apply(
        lambda row: (
            row["涨跌幅"] <= -19.9
            if row["代码"].startswith(("30", "68"))
            else row["涨跌幅"] <= -29
            if row["代码"].startswith("8")
            else row["涨跌幅"] <= -9.9
        ),
        axis=1,
    )
    limit_down_stocks = df[df["跌停板"] & ~df["代码"].str.startswith("8")].shape[0]
    return limit_down_stocks


@st.cache_data(ttl=300)
def stock_up_down_ratio():
    """
    计算股票的涨跌比。

    该函数获取A股的实时交易数据，并计算上涨股票数量与下跌股票数量的比值。

    返回:
        float: 股票的涨跌比。如果数据为空，则返回0。
    """
    df = ak.stock_zh_a_spot_em()
    if df.empty:
        return 0

    # 计算股票总数
    num_stocks = len(df)

    # 计算上涨和下跌股票的数量
    up_stocks = df[df["涨跌幅"] >= 0].shape[0]
    down_stocks = df[df["涨跌幅"] < 0].shape[0]
    if down_stocks == 0:
        return float("inf")

    up_down_ratio = (up_stocks / num_stocks) * 100
    return up_down_ratio


@st.cache_data(ttl=300)
def top_n_stock_avg_price_change(n):
    """
    计算前 n% 成交金额的股票的平均涨幅。

    该函数获取A股的实时交易数据，将股票按成交金额降序排序，并计算总成交金额。
    然后确定构成前 n% 成交金额的股票数量，并计算这些股票的平均涨幅。

    参数:
        n (float): 要计算的股票百分比。

    返回:
        float: 前 n% 成交金额的股票的平均涨幅。如果数据为空，则返回0。
    """
    # 获取 A 股实时行情数据
    # 序号	代码	名称	最新价	涨跌幅	涨跌额	成交量	成交额	振幅	最高	...	量比	换手率	市盈率-动态	市净率	总市值	流通市值	涨速	5分钟涨跌	60日涨跌幅	年初至今涨跌幅
    df = ak.stock_zh_a_spot_em()
    if df.empty:
        return 0

    # 按成交金额降序排序
    df_sorted = df.sort_values("成交额", ascending=False)

    # 计算前 n% 的股票数量
    num_stocks = len(df)
    top_n_percent = int(num_stocks * (n / 100))

    # 计算前 n% 股票的加权平均涨幅
    top_n_weighted_avg_price_change = (
        df_sorted["涨跌幅"].head(top_n_percent)
        * df_sorted["总市值"].head(top_n_percent)
    ).sum() / df_sorted["总市值"].head(top_n_percent).sum()

    # 计算前 n% 股票的算数平均涨幅，去除涨幅超过31%的股票
    top_n_avg_price_change = (
        df_sorted[df_sorted["涨跌幅"] < 31]["涨跌幅"].head(top_n_percent).mean()
    )
    return top_n_weighted_avg_price_change, top_n_avg_price_change


@st.cache_data(ttl=300)
def top_n_stock_amount_percent(n):
    """
    计算前 n% 的股票对总成交量的贡献百分比。

    该函数获取A股的实时交易数据，将股票按成交量降序排序，并计算总成交量。
    然后确定构成前 n% 成交量的股票数量，并计算这些股票的总成交量。
    最后，计算前 n% 的股票对总成交量的贡献百分比。

    参数:
        n (float): 要计算的股票百分比。

    返回:
        float: 前 n% 的股票对总成交量的贡献百分比。如果总成交量为零，则返回0。
    """

    # 获取 A 股实时行情数据
    df = ak.stock_zh_a_spot_em()
    # 按成交量降序排序
    df_sorted = df.sort_values("成交量", ascending=False)

    # 计算前 n% 的股票数量
    num_stocks = len(df)
    top_n_percent = int(num_stocks * (n / 100))

    # 计算总成交量
    total_amount = df["成交量"].sum()

    if total_amount == 0:
        return 0

    # 计算前 n% 股票的成交量总和
    top_n_percent_amount = df_sorted["成交量"].head(top_n_percent).sum()

    # 计算拥挤度
    crowdedness = top_n_percent_amount / total_amount
    return crowdedness

@st.cache_data(ttl=300)
def get_top_n_popular_stocks(n):
    """
    获取成交额前 N 的股票详细信息和统计数据。

    参数:
        n (int): 获取前 N 只股票的信息

    返回:
        df: 包含前 N 只股票的详细信息和统计数据的 DataFrame。
    """
    try:
        # 获取 A 股实时行情数据
        df = ak.stock_zh_a_spot_em()
        if df.empty:
            return None

        # 按成交额降序排序
        df_sorted = df.sort_values("成交额", ascending=False)

        # 获取前 N 只股票
        top_n_stocks = df_sorted.head(n).copy()

        # 选择需要的列并重命名
        result_df = top_n_stocks[
            ["代码", "名称", "最新价", "涨跌幅", "成交额", "总市值", "换手率"]
        ].copy()

        # 格式化数值
        result_df["涨跌幅"] = result_df["涨跌幅"].apply(lambda x: f"{x:.2f}%")
        result_df["换手率"] = result_df["换手率"].apply(lambda x: f"{x:.2f}%")
        result_df["成交额"] = (result_df["成交额"] / 1e8).apply(lambda x: f"{int(x)}亿")
        result_df["总市值"] = (result_df["总市值"] / 1e8).apply(lambda x: f"{int(x)}亿")
        result_df["最新价"] = result_df["最新价"].apply(lambda x: f"{x:.2f}")

        # 设置索引为名称，但不显示索引名
        result_df.set_index("名称", inplace=True)

        return result_df

    except Exception as e:
        return None


@st.cache_data(ttl=300)
def calculate_top_n_stocks_avg_market_value(n):
    """
    计算成交额前N的股票的平均市值。

    参数:
        n (int): 要计算的股票数量

    返回:
        tuple: (avg_market_value, total_market_value, stocks_count)
        - avg_market_value: 平均市值（亿元）
        - total_market_value: 总市值（亿元）
        - stocks_count: 实际统计的股票数量
    """
    try:
        df = ak.stock_zh_a_spot_em()

        if df.empty:
            return 0, 0, 0

        # 按成交额降序排序并获取前N只
        df_sorted = df.sort_values("成交额", ascending=False).head(n)

        # 计算市值（转换为亿元）
        total_market_value = df_sorted["总市值"].sum() / 1e8
        avg_market_value = df_sorted["总市值"].mean() / 1e8
        stocks_count = len(df_sorted)

        return avg_market_value, total_market_value, stocks_count
    except Exception as e:
        return 0, 0, 0

def get_market_heat():
    # Streamlit 页面设置

    # 获取当前成交额
    sh_amount, sz_amount = get_a_amount()

    # 计算总成交额和预测总成交额
    total_amount = sh_amount + sz_amount or 1  # Use 1 if total_amount is 0
    # 创业板成交占比（散户跟风指标）
    cyb_amount = get_index_amount("399006")

    # 计算创业板成交占总成交比例
    cyb_ratio = cyb_amount / total_amount * 100

    # 沪深 300 成交占比
    hs300_amount = get_index_amount("000300")
    hs300_ratio = hs300_amount / total_amount * 100

    # 中证 1000 成交占比
    zz1000_amount = get_index_amount("000852")
    zz1000_ratio = zz1000_amount / total_amount * 100

    # 中证 2000 成交占比
    zz2000_amount = get_index_amount("932000")
    zz2000_ratio = zz2000_amount / total_amount * 100

    # 获取5日均值
    avg_5_day = get_n_day_avg_amount(5)

    # 拥挤度，算法参见https://legulegu.com/stockdata/ashares-congestion
    crowdedness = top_n_stock_amount_percent(5) * 100

    # 中间股票涨幅
    middle_price_change_value = middle_price_change()

    # top5 成交额股票平均涨幅和加权平均涨幅
    top5_weighted_avg_price_change, top5_avg_price_change = (
        top_n_stock_avg_price_change(5)
    )
    # 股票涨跌比
    up_down_ratio = stock_up_down_ratio()

    # 涨停数量
    limit_up_count = count_limit_up_stocks()
    # 跌停数量
    limit_down_count = count_limit_down_stocks()

    # 计算前10只股票的平均市值
    avg_market_value, total_market_value, stocks_count = (
        calculate_top_n_stocks_avg_market_value(10)
    )
    # 显示前10只活跃股票的详细信息
    top_stocks = get_top_n_popular_stocks(10)

    # 创建数据字典
    data = {
        "指标": [
            "上证成交额",
            "深证成交额",
            "创业板成交额",
            "当前总成交额",
            "创业板成交占总成交比例",
            "中证 1000 成交占总成交比例",
            "中证 2000 成交占总成交比例",
            "沪深 300 成交占总成交比例",
            "5日均值",
            "交易拥挤度",
            "中位数股票涨幅",
            "前 5% 成交加权涨幅",
            "前 5% 成交算数涨幅",
            "股票上涨百分比",
            "涨停板股票数量",
            "跌停板股票数量",
            f"前{stocks_count}大成交额股票平均市值",
            f"前{stocks_count}大成交额股票活跃度",
        ],
        "数值": [
            int(sh_amount / 1e8),  # 上证成交额（亿）
            int(sz_amount / 1e8),  # 深证成交额（亿）
            int(cyb_amount / 1e8),  # 创业板成交额（亿）
            int(total_amount / 1e8),  # 当前总成交额（亿）
            round(cyb_ratio, 2),  # 创业板成交占比（%）
            round(zz1000_ratio, 2),  # 中证1000成交占比（%）
            round(zz2000_ratio, 2),  # 中证2000成交占比（%）
            round(hs300_ratio, 2),  # 沪深300成交占比（%）
            # 预计今日总成交额（亿）
            int(avg_5_day / 1e8),  # 5日均值（亿）
            round(crowdedness, 2),  # 交易拥挤度
            round(middle_price_change_value, 2),  # 中位数股票涨幅（%）
            round(top5_weighted_avg_price_change, 2),  # 前5%成交加权涨幅（%）
            round(top5_avg_price_change, 2),  # 前5%成交算数涨幅（%）
            round(up_down_ratio, 2),  # 股票上涨百分比（%）
            limit_up_count,  # 涨停板股票数量
            limit_down_count,  # 跌停板股票数量
            int(avg_market_value),  # 前N大成交额股票平均市值（亿）
            top_stocks,  # 前N大成交额股票活跃度
        ],
    }

    return data


placeholder = st.empty()  # 创建一个空白区域


def color_negative_red(val):
    try:
        val = float(val.rstrip("%"))
    except ValueError:
        return ""
    color = "red" if val > 0 else "green"
    return f"color: {color}"


def streamlit_market_heat():
    data = get_market_heat()

    # 成交额指标
    st.header("成交额")
    for item, value in zip(data["指标"][0:10], data["数值"][0:10]):
        st.write(f"{item}: {value}")

    # 情绪指标
    st.header("情绪指标")
    for item, value in zip(data["指标"][10:17], data["数值"][10:17]):
        st.write(f"{item}: {value}")

    # 清除缓存按钮
    if st.button("清除缓存"):
        st.cache_data.clear()
        ak.clear_cache()
        st.success("缓存已清除")
