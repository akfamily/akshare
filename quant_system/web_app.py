#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股量化系统 - Web可视化界面
使用Streamlit构建交互式Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import QuantSystem
from analysis.cycle.kitchin import KitchinCycle
from analysis.cycle.juglar import JuglarCycle
from analysis.cycle.marks_pendulum import MarksPendulum

# 页面配置
st.set_page_config(
    page_title="A股量化分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .cycle-indicator {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 0.3rem;
        text-align: center;
    }
    .bullish {
        background-color: #d4edda;
        color: #155724;
    }
    .bearish {
        background-color: #f8d7da;
        color: #721c24;
    }
    .neutral {
        background-color: #fff3cd;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_system():
    """初始化系统（缓存）"""
    return QuantSystem()


@st.cache_data(ttl=3600)  # 缓存1小时
def get_market_analysis():
    """获取市场分析（缓存）"""
    system = init_system()
    return system.analyze_market_cycle()


@st.cache_data(ttl=3600)
def get_investment_advice():
    """获取投资建议（缓存）"""
    system = init_system()
    return system.get_investment_advice()


def render_header():
    """渲染页面头部"""
    st.markdown('<div class="main-header">📊 A股量化分析系统</div>', unsafe_allow_html=True)
    st.markdown(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")


def render_cycle_dashboard(cycle_analysis):
    """渲染周期分析仪表盘"""
    st.header("🔄 市场周期分析")

    col1, col2, col3 = st.columns(3)

    # 基钦周期
    with col1:
        kitchin = cycle_analysis['kitchin']
        phase_color = get_phase_color(kitchin['phase'])

        st.markdown(f"""
        <div class="cycle-indicator {phase_color}">
            基钦周期（库存周期）<br>
            {kitchin['phase_name']}
        </div>
        """, unsafe_allow_html=True)

        st.metric("阶段进度", f"{kitchin['progress']:.1%}")
        st.metric("需求增速", f"{kitchin['demand_growth']:.2f}%")
        st.metric("库存增速", f"{kitchin['inventory_growth']:.2f}%")
        st.metric("置信度", f"{kitchin['confidence']:.1%}")

    # 朱格拉周期
    with col2:
        juglar = cycle_analysis['juglar']
        phase_color = get_phase_color(juglar['phase'])

        st.markdown(f"""
        <div class="cycle-indicator {phase_color}">
            朱格拉周期（产能周期）<br>
            {juglar['phase_name']}
        </div>
        """, unsafe_allow_html=True)

        st.metric("置信度", f"{juglar['confidence']:.1%}")
        st.info(juglar['next_inflection'])

    # 马克斯钟摆
    with col3:
        pendulum = cycle_analysis['pendulum']
        temp_color = get_temperature_color(pendulum['total_score'])

        st.markdown(f"""
        <div class="cycle-indicator {temp_color}">
            市场情绪温度<br>
            {pendulum['total_score']:.1f}/100
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**状态**: {pendulum['level']}")
        st.metric("估值", f"{pendulum['valuation']:.1f}")
        st.metric("情绪", f"{pendulum['sentiment']:.1f}")
        st.metric("流动性", f"{pendulum['liquidity']:.1f}")
        st.metric("市场宽度", f"{pendulum['breadth']:.1f}")


def render_investment_advice(advice):
    """渲染投资建议"""
    st.header("💡 投资建议")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("核心建议")

        # 建议仓位
        position = advice['recommended_position']
        st.metric("建议仓位", f"{position:.1%}", delta=None)

        # 进度条
        st.progress(position)

        # 择时信号
        signal_color = {
            'STRONG_BUY': '🟢',
            'BUY': '🟢',
            'HOLD': '🟡',
            'REDUCE': '🟠',
            'DEFENSIVE': '🔴'
        }
        signal = advice['timing_signal']
        st.markdown(f"**择时信号**: {signal_color.get(signal, '⚪')} {signal}")

        # 情绪策略
        st.markdown(f"**情绪策略**: {advice['sentiment_action']}")

        # 风险等级
        st.markdown(f"**风险等级**: {advice['risk_level']}")

    with col2:
        st.subheader("行业配置建议")

        # 创建行业配置表格
        sector_rec = advice['sector_advice']['combined_recommendation']

        sectors_df = pd.DataFrame({
            '配置建议': ['超配'] * len(sector_rec['overweight'][:5]) +
                       ['标配'] * len(sector_rec['neutral'][:3]) +
                       ['低配'] * len(sector_rec['underweight'][:3]),
            '行业': sector_rec['overweight'][:5] +
                   sector_rec['neutral'][:3] +
                   sector_rec['underweight'][:3]
        })

        # 显示表格
        st.dataframe(
            sectors_df,
            use_container_width=True,
            hide_index=True
        )


def render_key_points(advice):
    """渲染关键要点"""
    st.header("📌 关键要点")

    for i, point in enumerate(advice['key_points'], 1):
        st.markdown(f"{i}. {point}")


def render_charts():
    """渲染图表"""
    st.header("📈 数据可视化")

    tab1, tab2, tab3 = st.tabs(["周期趋势", "情绪温度", "行业轮动"])

    with tab1:
        render_cycle_trend_chart()

    with tab2:
        render_sentiment_chart()

    with tab3:
        render_sector_rotation_chart()


def render_cycle_trend_chart():
    """渲染周期趋势图"""
    # 模拟历史数据
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    kitchin_phases = np.random.choice([1, 2, 3, 4], 100)
    sentiment_scores = np.random.uniform(20, 80, 100)

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("基钦周期阶段", "市场情绪温度"),
        vertical_spacing=0.15
    )

    # 基钦周期
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=kitchin_phases,
            mode='lines+markers',
            name='基钦周期',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )

    # 情绪温度
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=sentiment_scores,
            mode='lines',
            name='情绪温度',
            line=dict(color='red', width=2),
            fill='tozeroy'
        ),
        row=2, col=1
    )

    # 添加阈值线
    fig.add_hline(y=20, line_dash="dash", line_color="green", row=2, col=1)
    fig.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)

    fig.update_layout(height=600, showlegend=True)
    fig.update_yaxes(title_text="阶段", row=1, col=1)
    fig.update_yaxes(title_text="温度", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)


def render_sentiment_chart():
    """渲染情绪分析图"""
    cycle_analysis = get_market_analysis()
    pendulum = cycle_analysis['pendulum']

    # 创建雷达图
    categories = ['估值', '情绪', '流动性', '市场宽度']
    values = [
        pendulum['valuation'],
        pendulum['sentiment'],
        pendulum['liquidity'],
        pendulum['breadth']
    ]

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='当前状态'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # 显示详细数值
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("估值", f"{pendulum['valuation']:.1f}")
    col2.metric("情绪", f"{pendulum['sentiment']:.1f}")
    col3.metric("流动性", f"{pendulum['liquidity']:.1f}")
    col4.metric("市场宽度", f"{pendulum['breadth']:.1f}")


def render_sector_rotation_chart():
    """渲染行业轮动图"""
    advice = get_investment_advice()
    sectors = advice['sector_advice']['combined_recommendation']

    # 创建横向条形图
    overweight = sectors['overweight'][:5]
    underweight = sectors['underweight'][:3]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=overweight,
        x=[1.0] * len(overweight),
        orientation='h',
        name='超配',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        y=underweight,
        x=[-1.0] * len(underweight),
        orientation='h',
        name='低配',
        marker_color='red'
    ))

    fig.update_layout(
        title="行业配置建议",
        xaxis_title="配置倾向",
        yaxis_title="行业",
        barmode='relative',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def get_phase_color(phase):
    """根据周期阶段返回颜色"""
    color_map = {
        1: 'bullish',   # 复苏/被动补库
        2: 'bullish',   # 繁荣/主动补库
        3: 'bearish',   # 衰退/被动去库
        4: 'bearish'    # 萧条/主动去库
    }
    return color_map.get(phase, 'neutral')


def get_temperature_color(score):
    """根据情绪温度返回颜色"""
    if score < 30:
        return 'bullish'
    elif score < 70:
        return 'neutral'
    else:
        return 'bearish'


def main():
    """主函数"""
    # 侧边栏
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100?text=A%E8%82%A1%E9%87%8F%E5%8C%96%E7%B3%BB%E7%BB%9F", use_column_width=True)

        st.markdown("---")

        st.markdown("### ⚙️ 设置")

        # 刷新按钮
        if st.button("🔄 刷新数据", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        # 下载报告
        if st.button("📥 下载报告", use_container_width=True):
            system = init_system()
            report = system.generate_daily_report()
            st.download_button(
                label="保存报告",
                data=report,
                file_name=f"report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

        st.markdown("---")

        st.markdown("### 📚 快速链接")
        st.markdown("- [使用指南](README.md)")
        st.markdown("- [新手指南](新手使用指南.md)")
        st.markdown("- [GitHub](https://github.com/akfamily/akshare)")

        st.markdown("---")

        st.markdown("### ℹ️ 关于")
        st.markdown("""
        **版本**: 1.0.0
        **更新**: 2025-10-21
        **作者**: AI量化团队

        基于周期理论的A股量化分析系统
        """)

    # 主内容区
    render_header()

    try:
        # 获取数据
        cycle_analysis = get_market_analysis()
        advice = get_investment_advice()

        # 渲染各个部分
        render_cycle_dashboard(cycle_analysis)
        st.markdown("---")

        render_investment_advice(advice)
        st.markdown("---")

        render_key_points(advice)
        st.markdown("---")

        render_charts()

    except Exception as e:
        st.error(f"加载数据失败: {str(e)}")
        st.info("请确保已经运行 `python3 main.py` 至少一次")

    # 页脚
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "© 2025 A股量化分析系统 | 仅供学习研究使用"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    main()
