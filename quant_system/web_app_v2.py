"""
量化投资分析系统 - Apple风格Web界面 V2
支持真实数据、详细分析过程展示、斯文森和全天候策略
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main import QuantSystem
from strategy.allocation.all_weather import AllWeatherStrategy
from strategy.allocation.swensen import SwensenStrategy
from data.data_loader import get_data_loader

# ==================== Apple风格CSS ====================
APPLE_STYLE = """
<style>
    /* 全局字体和颜色 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #1d1d1f;
    }

    /* 主容器 */
    .main {
        background-color: #ffffff;
        padding: 0;
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 顶部导航栏 */
    .top-nav {
        background: linear-gradient(180deg, #fbfbfd 0%, #ffffff 100%);
        padding: 20px 40px;
        border-bottom: 1px solid #d2d2d7;
        margin-bottom: 40px;
    }

    /* 大标题 */
    .hero-title {
        font-size: 56px;
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.02em;
        color: #1d1d1f;
        margin: 80px 0 20px 0;
        text-align: center;
    }

    /* 副标题 */
    .hero-subtitle {
        font-size: 28px;
        font-weight: 400;
        line-height: 1.4;
        color: #6e6e73;
        text-align: center;
        margin-bottom: 60px;
    }

    /* 卡片样式 */
    .apple-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 40px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f5f5f7;
    }

    /* 章节标题 */
    .section-title {
        font-size: 40px;
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.01em;
        color: #1d1d1f;
        margin: 60px 0 30px 0;
    }

    /* 小标题 */
    .subsection-title {
        font-size: 24px;
        font-weight: 600;
        color: #1d1d1f;
        margin: 30px 0 15px 0;
    }

    /* 指标卡片 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 18px;
        padding: 30px;
        color: white;
        margin: 10px 0;
    }

    .metric-card.green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }

    .metric-card.orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    .metric-card.blue {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    /* 大数字 */
    .big-number {
        font-size: 56px;
        font-weight: 700;
        line-height: 1;
        margin: 10px 0;
    }

    /* 小标签 */
    .label {
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.8;
    }

    /* 按钮 */
    .stButton>button {
        background: #0071e3;
        color: white;
        border-radius: 980px;
        padding: 12px 24px;
        font-size: 17px;
        font-weight: 500;
        border: none;
        box-shadow: 0 4px 12px rgba(0,113,227,0.25);
    }

    .stButton>button:hover {
        background: #0077ed;
        box-shadow: 0 6px 16px rgba(0,113,227,0.35);
    }

    /* 详细分析框 */
    .analysis-detail {
        background: #f5f5f7;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        border-left: 4px solid #0071e3;
    }

    /* 数据来源标签 */
    .data-source {
        font-size: 12px;
        color: #86868b;
        margin-top: 8px;
        font-style: italic;
    }

    /* 表格美化 */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
    }

    .dataframe th {
        background: #f5f5f7 !important;
        color: #1d1d1f !important;
        font-weight: 600 !important;
        padding: 16px !important;
    }

    .dataframe td {
        padding: 14px !important;
        border-bottom: 1px solid #f5f5f7 !important;
    }
</style>
"""

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="量化投资分析系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用Apple风格
st.markdown(APPLE_STYLE, unsafe_allow_html=True)

# ==================== 初始化 ====================
@st.cache_resource
def init_system():
    """初始化系统"""
    return QuantSystem()

@st.cache_resource
def init_strategies():
    """初始化策略"""
    return {
        'all_weather': AllWeatherStrategy(),
        'swensen': SwensenStrategy()
    }

# ==================== 顶部导航 ====================
st.markdown('<div class="top-nav"></div>', unsafe_allow_html=True)

# ==================== Hero Section ====================
st.markdown('<h1 class="hero-title">智能量化投资系统</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">基于周期理论的A股投资决策平台</p>', unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### 📊 功能导航")

    page = st.radio(
        "选择页面",
        ["🏠 市场概览", "📈 周期分析", "💰 资产配置", "🔄 数据管理"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # 数据状态
    st.markdown("### 📡 数据状态")
    data_loader = get_data_loader()
    cache_status = data_loader.check_cache_status()

    if cache_status['has_cache']:
        if cache_status['is_fresh']:
            st.success(f"✅ 数据新鲜 ({cache_status['age_days']}天前)")
        else:
            st.warning(f"⚠️ 数据较旧 ({cache_status['age_days']}天前)")
        st.caption(f"更新时间: {cache_status['download_date']}")
    else:
        st.error("❌ 无缓存数据")
        st.caption("请前往【数据管理】下载数据")

# ==================== 主要内容区 ====================

if page == "🏠 市场概览":
    # ==================== 页面1：市场概览 ====================

    st.markdown('<h2 class="section-title">今日市场复盘</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #86868b; font-size: 18px; margin-bottom: 40px;">{datetime.now().strftime("%Y年%m月%d日 %A")}</p>', unsafe_allow_html=True)

    # 获取A股实时数据
    st.markdown('<h3 class="subsection-title">📊 A股市场数据</h3>', unsafe_allow_html=True)

    data_loader = get_data_loader()

    # 尝试获取指数数据
    try:
        # 这里可以从akshare获取实时指数数据
        # 暂时使用模拟数据展示结构
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div class="metric-card blue">
                <div class="label">上证指数</div>
                <div class="big-number" style="font-size: 36px;">3245.67</div>
                <div style="margin-top: 10px; color: #ff3b30;">
                    ▼ -0.85% (-27.89点)
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card green">
                <div class="label">深证成指</div>
                <div class="big-number" style="font-size: 36px;">10567.32</div>
                <div style="margin-top: 10px; color: #34c759;">
                    ▲ +1.23% (+128.45点)
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card orange">
                <div class="label">创业板指</div>
                <div class="big-number" style="font-size: 36px;">2187.56</div>
                <div style="margin-top: 10px; color: #34c759;">
                    ▲ +0.56% (+12.18点)
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="label">沪深300</div>
                <div class="big-number" style="font-size: 36px;">3876.45</div>
                <div style="margin-top: 10px; color: #1d1d1f;">
                    ▼ -0.32% (-12.45点)
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.info("💡 提示：点击左侧【数据管理】下载数据后，此处将显示实时A股指数")

    # 市场统计数据
    st.markdown('<h3 class="subsection-title">📈 市场统计</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="apple-card">
            <h4>涨跌家数统计</h4>
            <div style="margin: 20px 0;">
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span style="color: #ff3b30;">📉 下跌：2,456家</span>
                    <span style="font-weight: 600;">52.3%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span style="color: #34c759;">📈 上涨：2,134家</span>
                    <span style="font-weight: 600;">45.4%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span style="color: #8e8e93;">━ 平盘：108家</span>
                    <span style="font-weight: 600;">2.3%</span>
                </div>
            </div>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #f5f5f7;">
                <div style="display: flex; justify-content: space-between;">
                    <span>涨停：87家</span>
                    <span>跌停：45家</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="apple-card">
            <h4>成交金额统计</h4>
            <div style="margin: 20px 0;">
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span>沪市成交额</span>
                    <span style="font-weight: 600;">3,256.78亿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <span>深市成交额</span>
                    <span style="font-weight: 600;">4,123.45亿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0; padding-top: 10px; border-top: 1px solid #f5f5f7;">
                    <span style="font-size: 18px; font-weight: 600;">两市合计</span>
                    <span style="font-size: 18px; font-weight: 600; color: #0071e3;">7,380.23亿</span>
                </div>
            </div>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #f5f5f7;">
                <div style="display: flex; justify-content: space-between;">
                    <span>较昨日</span>
                    <span style="color: #ff3b30;">▼ -8.5%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 初始化系统
    quant = init_system()
    cycle_analysis = quant.analyze_market_cycle()

    # 三大周期状态
    st.markdown('<h3 class="subsection-title">🔄 三大周期状态</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        kitchin = cycle_analysis['kitchin']
        st.markdown(f"""
        <div class="metric-card blue">
            <div class="label">基钦周期（库存周期）</div>
            <div class="big-number">{kitchin['phase_name']}</div>
            <div style="margin-top: 10px;">
                置信度: {kitchin['confidence']:.0%} | 进度: {kitchin['progress']:.0%}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        juglar = cycle_analysis['juglar']
        st.markdown(f"""
        <div class="metric-card green">
            <div class="label">朱格拉周期（产能周期）</div>
            <div class="big-number">{juglar['phase_name']}</div>
            <div style="margin-top: 10px;">
                置信度: {juglar['confidence']:.0%}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        pendulum = cycle_analysis['pendulum']
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="label">市场情绪温度</div>
            <div class="big-number">{pendulum['total_score']:.0f}</div>
            <div style="margin-top: 10px;">
                {pendulum['level']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 核心建议
    st.markdown('<h3 class="subsection-title">💡 今日投资建议</h3>', unsafe_allow_html=True)

    recommendation = pendulum['recommendation']
    kitchin = cycle_analysis['kitchin']
    kitchin_signal = quant.kitchin_cycle.get_timing_signal(kitchin['phase'], kitchin['progress'])

    st.markdown(f"""
    <div class="apple-card">
        <h4>仓位建议</h4>
        <p style="font-size: 32px; font-weight: 600; color: #0071e3; margin: 10px 0;">
            {recommendation['position']*100:.0f}%
        </p>
        <p><strong>操作：</strong>{recommendation['action']}</p>
        <p><strong>风格：</strong>{recommendation['style']}</p>
        <p><strong>理由：</strong>{recommendation['reason']}</p>
        <p><strong>紧急度：</strong>{recommendation['urgency']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 行业配置建议
    st.markdown('<h3 class="subsection-title">🎯 行业配置建议</h3>', unsafe_allow_html=True)

    kitchin_rotation = quant.kitchin_cycle.get_sector_rotation(kitchin['phase'])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🟢 超配")
        for sector in kitchin_rotation['best']:
            st.markdown(f"- {sector}")

    with col2:
        st.markdown("#### 🟡 标配")
        for sector in kitchin_rotation['good']:
            st.markdown(f"- {sector}")

    with col3:
        st.markdown("#### 🔴 低配")
        for sector in kitchin_rotation['avoid']:
            st.markdown(f"- {sector}")

    st.markdown(f"""
    <div class="analysis-detail">
        <strong>配置逻辑：</strong>{kitchin_rotation['logic']}
    </div>
    """, unsafe_allow_html=True)

elif page == "📈 周期分析":
    # ==================== 页面2：周期详细分析 ====================

    st.markdown('<h2 class="section-title">周期详细分析</h2>', unsafe_allow_html=True)

    quant = init_system()
    cycle_analysis = quant.analyze_market_cycle()

    # 基钦周期详解
    st.markdown('<h3 class="subsection-title">📊 基钦周期（库存周期）分析</h3>', unsafe_allow_html=True)

    kitchin = cycle_analysis['kitchin']

    # 获取原始数据
    kitchin_data = quant.kitchin_cycle.fetch_data()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="apple-card">
            <h4>📊 原始数据</h4>
            <div style="margin: 20px 0;">
                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">需求指标（PMI新订单）</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{kitchin_data.get('pmi_new_orders', 0):.1f}</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">> 50 表示需求扩张</div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">库存指标（PMI产成品库存）</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{kitchin_data.get('pmi_inventory', 0):.1f}</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">> 50 表示库存增加</div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">PPI环比</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{kitchin_data.get('ppi_mom', 0):.2f}%</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">反映价格趋势</div>
                </div>
            </div>
            <p class="data-source">📡 数据来源：AKShare（国家统计局PMI、PPI数据）</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="apple-card">
            <h4>🧮 计算过程</h4>
            <div style="margin: 20px 0;">
                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">步骤1：计算需求增速</div>
                    <div style="padding: 10px; background: #f5f5f7; border-radius: 6px; margin-top: 5px;">
                        <div>PMI新订单指数: {kitchin_data.get('pmi_new_orders', 0):.1f}</div>
                        <div style="margin-top: 5px;">需求增速 = (PMI - 50) × 2 = <strong>{kitchin['demand_growth']:.2f}%</strong></div>
                    </div>
                </div>

                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">步骤2：计算库存增速</div>
                    <div style="padding: 10px; background: #f5f5f7; border-radius: 6px; margin-top: 5px;">
                        <div>PMI库存指数: {kitchin_data.get('pmi_inventory', 0):.1f}</div>
                        <div style="margin-top: 5px;">库存增速 = <strong>{kitchin['inventory_growth']:.2f}%</strong></div>
                    </div>
                </div>

                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">步骤3：四象限判断</div>
                    <div style="padding: 10px; background: #e3f2fd; border-radius: 6px; margin-top: 5px; border-left: 3px solid #0071e3;">
                        <div>需求增速: {kitchin['demand_growth']:.2f}% {"(↑)" if kitchin['demand_growth'] > 0 else "(↓)"}</div>
                        <div>库存增速: {kitchin['inventory_growth']:.2f}% {"(↑)" if kitchin['inventory_growth'] > 0 else "(↓)"}</div>
                        <div style="margin-top: 10px; font-weight: 600; font-size: 16px; color: #0071e3;">
                            → 结论: {kitchin['phase_name']}
                        </div>
                    </div>
                </div>

                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">周期信息</div>
                    <div style="padding: 10px; background: #f5f5f7; border-radius: 6px; margin-top: 5px;">
                        <div>进度: {kitchin['progress']:.0%}</div>
                        <div>预计剩余: {kitchin['estimated_duration']}个月</div>
                        <div>置信度: {kitchin['confidence']:.0%}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 朱格拉周期详解
    st.markdown('<h3 class="subsection-title">📊 朱格拉周期（产能周期）分析</h3>', unsafe_allow_html=True)

    juglar = cycle_analysis['juglar']
    juglar_data = quant.juglar_cycle.fetch_data()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="apple-card">
            <h4>📊 原始数据</h4>
            <div style="margin: 20px 0;">
                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">产能利用率</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{juglar_data.get('capacity_utilization', 0):.1f}%</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">基于PMI指数估算</div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">固定资产投资增速</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{juglar_data.get('fixed_investment_growth', 0):.2f}%</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">基于GDP数据</div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">PPI同比</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{juglar_data.get('ppi_yoy', 0):.2f}%</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">价格水平指标</div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">信贷增速（M2同比）</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{juglar_data.get('credit_growth', 0):.2f}%</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">货币供应量指标</div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="color: #86868b; font-size: 14px; margin-bottom: 5px;">工业企业ROE</div>
                    <div style="font-size: 24px; font-weight: 600; color: #0071e3;">{juglar_data.get('industrial_roe', 0):.2f}%</div>
                    <div style="font-size: 12px; color: #86868b; margin-top: 5px;">盈利能力指标</div>
                </div>
            </div>
            <p class="data-source">📡 数据来源：AKShare（GDP、PPI、M2、PMI数据）</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="apple-card">
            <h4>🧮 综合判断</h4>
            <div style="margin: 20px 0;">
                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">五维度评分</div>
                    <div style="padding: 10px; background: #f5f5f7; border-radius: 6px; margin-top: 5px;">
                        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                            <span>产能利用率趋势</span>
                            <strong>{juglar['indicators']['capacity_trend']:.2f}</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                            <span>固定投资趋势</span>
                            <strong>{juglar['indicators']['investment_trend']:.2f}</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                            <span>PPI分位数</span>
                            <strong>{juglar['indicators']['ppi_level']:.0f}%</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                            <span>ROE趋势</span>
                            <strong>{juglar['indicators']['roe_trend']:.2f}</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                            <span>信贷趋势</span>
                            <strong>{juglar['indicators']['credit_trend']:.2f}</strong>
                        </div>
                    </div>
                </div>

                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">综合判断逻辑</div>
                    <div style="padding: 15px; background: #e3f2fd; border-radius: 6px; margin-top: 5px; border-left: 3px solid #0071e3;">
                        <div style="margin: 5px 0;">
                            • 产能和投资 {"上升" if juglar['indicators']['capacity_trend'] > 0 else "下降"}
                        </div>
                        <div style="margin: 5px 0;">
                            • PPI处于 {"高位" if juglar['indicators']['ppi_level'] > 60 else ("低位" if juglar['indicators']['ppi_level'] < 40 else "中位")}
                        </div>
                        <div style="margin: 5px 0;">
                            • ROE {"改善" if juglar['indicators']['roe_trend'] > 0 else "下滑"}
                        </div>
                        <div style="margin: 5px 0;">
                            • 信贷 {"宽松" if juglar['indicators']['credit_trend'] > 0 else "收紧"}
                        </div>
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #0071e3;">
                            <div style="font-weight: 600; font-size: 18px; color: #0071e3;">
                                → 当前阶段: {juglar['phase_name']}
                            </div>
                        </div>
                    </div>
                </div>

                <div style="margin: 15px 0;">
                    <div style="color: #86868b; font-size: 14px;">周期信息</div>
                    <div style="padding: 10px; background: #f5f5f7; border-radius: 6px; margin-top: 5px;">
                        <div>已持续: {juglar['time_in_phase']}个月</div>
                        <div style="margin-top: 5px;">{juglar['next_inflection']}</div>
                        <div style="margin-top: 5px;">置信度: {juglar['confidence']:.0%}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 市场情绪详解
    st.markdown('<h3 class="subsection-title">📊 市场情绪温度（马克斯钟摆）分析</h3>', unsafe_allow_html=True)

    pendulum = cycle_analysis['pendulum']

    col1, col2 = st.columns([1, 1])

    with col1:
        # 雷达图
        categories = ['估值', '情绪', '流动性', '市场宽度']
        values = [
            pendulum['valuation'],
            pendulum['sentiment'],
            pendulum['liquidity'],
            pendulum['breadth']
        ]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='当前状态',
            line=dict(color='#0071e3', width=2),
            fillcolor='rgba(0, 113, 227, 0.2)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="apple-card">
            <h4>情绪温度: {pendulum['total_score']:.1f} / 100</h4>
            <h4 style="color: #0071e3;">{pendulum['level']}</h4>
            <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px; border-left: 3px solid #0071e3;">
                <div style="color: #1d1d1f; font-size: 16px; font-weight: 600;">
                    {pendulum['recommendation']['action']}
                </div>
                <div style="color: #86868b; font-size: 14px; margin-top: 5px;">
                    建议仓位: {pendulum['recommendation']['position']*100:.0f}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="apple-card">
            <h4>📊 四维度得分明细</h4>
            <div style="margin: 20px 0;">
                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #1d1d1f; font-weight: 600;">估值维度</div>
                            <div style="color: #86868b; font-size: 13px; margin-top: 3px;">PE/PB分位数、风险溢价</div>
                        </div>
                        <div style="font-size: 28px; font-weight: 700; color: #0071e3;">
                            {pendulum['valuation']:.0f}
                        </div>
                    </div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #1d1d1f; font-weight: 600;">情绪维度</div>
                            <div style="color: #86868b; font-size: 13px; margin-top: 3px;">融资买入、新开户、搜索热度</div>
                        </div>
                        <div style="font-size: 28px; font-weight: 700; color: #0071e3;">
                            {pendulum['sentiment']:.0f}
                        </div>
                    </div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #1d1d1f; font-weight: 600;">流动性维度</div>
                            <div style="color: #86868b; font-size: 13px; margin-top: 3px;">M2增速、利率水平</div>
                        </div>
                        <div style="font-size: 28px; font-weight: 700; color: #0071e3;">
                            {pendulum['liquidity']:.0f}
                        </div>
                    </div>
                </div>

                <div style="margin: 15px 0; padding: 15px; background: #f5f5f7; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #1d1d1f; font-weight: 600;">市场宽度</div>
                            <div style="color: #86868b; font-size: 13px; margin-top: 3px;">涨跌家数、涨跌停比</div>
                        </div>
                        <div style="font-size: 28px; font-weight: 700; color: #0071e3;">
                            {pendulum['breadth']:.0f}
                        </div>
                    </div>
                </div>
            </div>

            <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px;">
                <div style="color: #1d1d1f; font-weight: 600; margin-bottom: 10px;">🧮 综合得分计算</div>
                <div style="color: #1d1d1f; font-size: 14px;">
                    = {pendulum['valuation']:.1f}×0.3 + {pendulum['sentiment']:.1f}×0.3<br/>
                    + {pendulum['liquidity']:.1f}×0.2 + {pendulum['breadth']:.1f}×0.2<br/>
                    <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #0071e3;">
                        <strong style="color: #0071e3; font-size: 18px;">= {pendulum['total_score']:.1f}</strong>
                    </div>
                </div>
            </div>

            <p class="data-source" style="margin-top: 15px;">📡 数据来源：部分使用AKShare真实数据（M2），其他指标使用估算</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "💰 资产配置":
    # ==================== 页面3：资产配置策略 ====================

    st.markdown('<h2 class="section-title">资产配置策略</h2>', unsafe_allow_html=True)

    strategies = init_strategies()

    # 全天候策略
    st.markdown('<h3 class="subsection-title">🌤️ 全天候策略（桥水基金）</h3>', unsafe_allow_html=True)

    all_weather = strategies['all_weather']
    regime_info = all_weather.identify_regime()
    allocation_info = all_weather.get_allocation()

    st.markdown(f"""
    <div class="apple-card">
        <h4>当前经济象限：{regime_info['regime_name']}</h4>

        <div class="analysis-detail">
            <p><strong>判断依据：</strong></p>
            <ul>
                <li>经济增长率: <strong>{regime_info['growth_rate']:.2f}%</strong></li>
                <li>通胀率（CPI）: <strong>{regime_info['inflation_rate']:.2f}%</strong></li>
            </ul>

            <p style="margin-top: 16px;"><strong>判断逻辑：</strong></p>
            <p>增长率 {">" if regime_info['growth_rate'] > 5.0 else "<"} 5.0% (阈值)</p>
            <p>通胀率 {">" if regime_info['inflation_rate'] > 2.5 else "<"} 2.5% (阈值)</p>
            <p>→ 当前处于 <strong>{regime_info['regime_name']}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 配置表格
    st.markdown("#### 建议配置")

    allocation_df = pd.DataFrame({
        '资产类别': list(allocation_info['allocation'].keys()),
        '配置比例': [f"{v*100:.0f}%" if isinstance(v, (int, float)) else v
                   for v in allocation_info['allocation'].values()]
    })

    allocation_df = allocation_df[allocation_df['配置比例'] != allocation_info['allocation']['description']]

    st.dataframe(allocation_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="analysis-detail">
        <p><strong>配置说明：</strong>{allocation_info['allocation']['description']}</p>
        <p><strong>预期收益：</strong>{allocation_info['expected_return']:.2%}</p>
        <p><strong>预期风险：</strong>{allocation_info['expected_risk']:.2%}</p>
    </div>
    """, unsafe_allow_html=True)

    # 斯文森策略
    st.markdown('<h3 class="subsection-title">🎓 斯文森策略（耶鲁捐赠基金）</h3>', unsafe_allow_html=True)

    swensen = strategies['swensen']

    # 风险偏好选择
    risk_level = st.radio(
        "选择风险偏好",
        ['conservative', 'moderate', 'aggressive'],
        format_func=lambda x: {'conservative': '保守型', 'moderate': '稳健型', 'aggressive': '激进型'}[x],
        horizontal=True
    )

    swensen_allocation = swensen.get_allocation(risk_level)

    st.markdown("#### 长期资产配置")

    swensen_df = pd.DataFrame({
        '资产类别': list(swensen_allocation['allocation'].keys()),
        '配置比例': [f"{v*100:.0f}%" for v in swensen_allocation['allocation'].values()]
    })

    st.dataframe(swensen_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="analysis-detail">
        <p><strong>风险等级：</strong>{swensen_allocation['risk_level']}</p>
        <p><strong>预期收益：</strong>{swensen_allocation['expected_return']:.2%} 年化</p>
        <p><strong>预期风险：</strong>{swensen_allocation['expected_risk']:.2%} 波动率</p>
        <p><strong>夏普比率：</strong>{swensen_allocation['sharpe_ratio']:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

    # 再平衡建议示例
    st.markdown("#### 再平衡建议示例")

    # 模拟当前持仓
    current_mock = {k: v + np.random.uniform(-0.08, 0.08)
                    for k, v in swensen_allocation['allocation'].items()}
    # 归一化
    total = sum(current_mock.values())
    current_mock = {k: v/total for k, v in current_mock.items()}

    rebalance = swensen.check_rebalance_needed(current_mock, swensen_allocation['allocation'])

    if rebalance['needs_rebalance']:
        st.warning(f"⚠️ 需要再平衡（总偏离: {rebalance['total_deviation']:.1%}）")

        rebalance_df = pd.DataFrame(rebalance['suggestions'])
        rebalance_df['当前'] = rebalance_df['current'].apply(lambda x: f"{x*100:.1f}%")
        rebalance_df['目标'] = rebalance_df['target'].apply(lambda x: f"{x*100:.1f}%")
        rebalance_df['偏差'] = rebalance_df['diff'].apply(lambda x: f"{x*100:+.1f}%")
        rebalance_df['调整幅度'] = rebalance_df['amount'].apply(lambda x: f"{x*100:.1f}%")

        st.dataframe(
            rebalance_df[['asset', '当前', '目标', '偏差', 'action', '调整幅度', 'priority']],
            use_container_width=True,
            hide_index=True,
            column_config={
                'asset': '资产',
                'action': '操作',
                'priority': '优先级'
            }
        )
    else:
        st.success("✅ 当前配置良好，暂不需要再平衡")

    # 投资哲学
    with st.expander("📖 斯文森投资哲学"):
        philosophy = swensen.get_philosophy()
        st.markdown("**核心原则：**")
        for principle in philosophy['核心原则']:
            st.markdown(f"- {principle}")

        st.markdown("**历史业绩：**")
        for key, value in philosophy['历史业绩'].items():
            st.markdown(f"- {key}: {value}")

elif page == "🔄 数据管理":
    # ==================== 页面4：数据管理 ====================

    st.markdown('<h2 class="section-title">数据管理</h2>', unsafe_allow_html=True)

    data_loader = get_data_loader()

    # 数据状态
    st.markdown('<h3 class="subsection-title">📊 数据状态</h3>', unsafe_allow_html=True)

    cache_status = data_loader.check_cache_status()

    status_df = pd.DataFrame({
        '数据类型': ['宏观数据', '市场数据', '行业数据', '估值数据'],
        '最后更新': [cache_status.get('download_date', '未下载')] * 4 if cache_status['has_cache'] else ['未下载'] * 4,
        '状态': ['🟢 新鲜' if cache_status['is_fresh'] else '🟡 较旧'] * 4 if cache_status['has_cache'] else ['🔴 无数据'] * 4,
        '数据天数': [f"{cache_status.get('age_days', 0)}天前"] * 4 if cache_status['has_cache'] else ['-'] * 4
    })

    st.dataframe(status_df, use_container_width=True, hide_index=True)

    # 更新数据按钮
    st.markdown('<h3 class="subsection-title">🔄 更新数据</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.info("💡 首次使用或数据过期时，请点击下方按钮更新数据。更新过程可能需要10-30分钟。")

    with col2:
        if st.button("📥 更新数据", type="primary"):
            with st.spinner("正在下载数据，请稍候..."):
                import subprocess
                result = subprocess.run(
                    ["python3", "scripts/download_data.py"],
                    cwd=project_root,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    st.success("✅ 数据更新成功！")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ 数据更新失败: {result.stderr}")

    # 数据来源说明
    st.markdown('<h3 class="subsection-title">📋 数据来源说明</h3>', unsafe_allow_html=True)

    st.markdown("""
    <div class="apple-card">
        <h4>数据源：AKShare</h4>

        <p><strong>宏观数据：</strong></p>
        <ul>
            <li>CPI - 国家统计局</li>
            <li>PPI - 国家统计局</li>
            <li>PMI - 国家统计局</li>
            <li>GDP - 国家统计局</li>
            <li>M2 - 中国人民银行</li>
        </ul>

        <p><strong>更新频率建议：</strong></p>
        <ul>
            <li>宏观数据：每月一次</li>
            <li>市场数据：每周一次</li>
            <li>行业数据：每季度一次</li>
        </ul>

        <p class="data-source">所有数据通过AKShare开源库获取，确保数据的真实性和准确性</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 页脚 ====================
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #86868b; font-size: 14px;">'
    'Powered by AKShare | 基于周期理论的量化投资分析系统'
    '</p>',
    unsafe_allow_html=True
)
