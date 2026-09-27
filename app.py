"""
🛒 Supermarket Sales Analytics — Premium Dashboard
A dynamic, interactive data analytics application.
Upload any supermarket sales dataset and get instant business insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import io

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PREMIUM CUSTOM CSS — High-End Visual Design Skill
# Vibe: Ethereal Glass (Dark OLED) + Asymmetrical Bento Layout
# Fonts: Plus Jakarta Sans (body), Clash Display vibe via weight contrasts
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── GLOBAL RESET ── */
    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: linear-gradient(160deg, #050505 0%, #0a0a0f 40%, #080812 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e8e8ed;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c0c14 0%, #08080e 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.04) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.85rem !important;
    }

    /* ── HEADINGS ── */
    .stMarkdown h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.4rem !important;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0b0 50%, #7c7cf0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem !important;
    }
    .stMarkdown h2 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        color: #ffffff !important;
        letter-spacing: -0.02em;
        margin-top: 2.5rem !important;
    }
    .stMarkdown h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: rgba(255,255,255,0.85) !important;
    }

    /* ── METRIC CARDS (Double-Bezel Architecture) ── */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 1.2rem;
        padding: 1.4rem 1.6rem;
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.03),
            0 8px 32px rgba(0,0,0,0.4),
            inset 0 1px 1px rgba(255,255,255,0.06);
        transition: all 0.7s cubic-bezier(0.32,0.72,0,1);
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(124,124,240,0.2);
        box-shadow:
            0 0 0 1px rgba(124,124,240,0.1),
            0 12px 40px rgba(124,124,240,0.08),
            inset 0 1px 1px rgba(255,255,255,0.08);
        transform: translateY(-2px);
    }
    div[data-testid="stMetric"] label {
        color: rgba(255,255,255,0.45) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        color: #ffffff !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
    }

    /* ── PLOTLY CHARTS CONTAINER ── */
    .stPlotlyChart {
        background: linear-gradient(145deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.005) 100%);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 1.2rem;
        padding: 0.5rem;
        box-shadow:
            0 4px 24px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.04);
        transition: all 0.7s cubic-bezier(0.32,0.72,0,1);
    }
    .stPlotlyChart:hover {
        border-color: rgba(124,124,240,0.12);
    }

    /* ── DATAFRAME ── */
    .stDataFrame {
        border-radius: 1rem;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.04) !important;
    }

    /* ── FILE UPLOADER ── */
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border: 1px dashed rgba(124,124,240,0.3);
        border-radius: 1rem;
        padding: 1rem;
        transition: all 0.5s cubic-bezier(0.32,0.72,0,1);
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: rgba(124,124,240,0.5);
        background: rgba(124,124,240,0.03);
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.02);
        border-radius: 0.8rem;
        padding: 0.3rem;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.6rem;
        padding: 0.5rem 1.2rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.5);
        transition: all 0.5s cubic-bezier(0.32,0.72,0,1);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(124,124,240,0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(124,124,240,0.2);
    }

    /* ── EXPANDER ── */
    .streamlit-expanderHeader {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: rgba(255,255,255,0.8) !important;
        background: rgba(255,255,255,0.02) !important;
        border-radius: 0.8rem !important;
    }

    /* ── SELECTBOX / MULTISELECT ── */
    div[data-baseweb="select"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 0.6rem !important;
        color: #ffffff !important;
    }

    /* ── DIVIDER ── */
    hr {
        border-color: rgba(255,255,255,0.04) !important;
        margin: 2rem 0 !important;
    }

    /* ── NOISE OVERLAY ── */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        z-index: 50;
        pointer-events: none;
        opacity: 0.025;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    /* ── HIDE DEFAULT STREAMLIT ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PLOTLY THEME — Matches Ethereal Glass aesthetic
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHART_COLORS = ['#7c7cf0', '#f07c7c', '#7cf0b0', '#f0d07c', '#c07cf0', '#7cd4f0', '#f07cc0', '#a0f07c']
CHART_BG = 'rgba(0,0,0,0)'
CHART_GRID = 'rgba(255,255,255,0.04)'
CHART_TEXT = 'rgba(255,255,255,0.6)'
CHART_TITLE_FONT = dict(family='Plus Jakarta Sans', size=16, color='rgba(255,255,255,0.9)')
CHART_AXIS_FONT = dict(family='Plus Jakarta Sans', size=11, color=CHART_TEXT)
CHART_TICK_FONT = dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.4)')

def style_fig(fig, height=420):
    """Apply premium Ethereal Glass styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=CHART_AXIS_FONT,
        title_font=CHART_TITLE_FONT,
        legend=dict(
            font=dict(family='Plus Jakarta Sans', size=11, color='rgba(255,255,255,0.5)'),
            bgcolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=height,
        xaxis=dict(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID, tickfont=CHART_TICK_FONT),
        yaxis=dict(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID, tickfont=CHART_TICK_FONT),
        hoverlabel=dict(
            bgcolor='rgba(12,12,20,0.95)',
            bordercolor='rgba(124,124,240,0.3)',
            font=dict(family='JetBrains Mono', size=12, color='#ffffff')
        )
    )
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR — Data Source
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("# 🛒 Data Source")
    st.markdown("---")

    data_source = st.radio(
        "Choose data source",
        ["📂 Default Dataset", "📤 Upload New File"],
        index=0,
        help="Upload your own CSV/Excel/ODS file to see instant analysis"
    )

    df = None

    if data_source == "📂 Default Dataset":
        default_path = os.path.join(os.path.dirname(__file__), 'data', 'supermarket_sales.ods')
        if os.path.exists(default_path):
            df = pd.read_excel(default_path, engine='odf')
            st.success("Default dataset loaded")
        else:
            st.error("Default dataset not found. Please upload a file.")
    else:
        uploaded_file = st.file_uploader(
            "Drop your file here",
            type=['csv', 'xlsx', 'xls', 'ods'],
            help="Supports CSV, Excel (.xlsx/.xls), and ODS formats"
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.ods'):
                    df = pd.read_excel(uploaded_file, engine='odf')
                else:
                    df = pd.read_excel(uploaded_file)
                st.success(f"Loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    if df is not None:
        st.markdown("---")
        st.markdown("### 📊 Dataset Info")
        st.markdown(f"**Rows:** `{len(df):,}`")
        st.markdown(f"**Columns:** `{len(df.columns)}`")
        st.markdown(f"**Memory:** `{df.memory_usage(deep=True).sum() / 1024:.1f} KB`")

        # Auto-detect key columns
        st.markdown("---")
        st.markdown("### 🔧 Column Mapping")
        st.markdown("*Map your data columns to analysis fields*")

        numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
        all_cols = list(df.columns)

        # Smart defaults
        def find_col(candidates, cols):
            for c in candidates:
                for col in cols:
                    if c.lower() in col.lower():
                        return col
            return cols[0] if cols else None

        default_sales = find_col(['sales', 'total', 'revenue', 'amount'], numeric_cols)
        default_product = find_col(['product', 'item', 'name'], all_cols)
        default_category = find_col(['category', 'type', 'group', 'dept'], all_cols)
        default_branch = find_col(['branch', 'store', 'location', 'city'], all_cols)
        default_payment = find_col(['payment', 'pay', 'method'], all_cols)
        default_customer = find_col(['customer', 'member', 'type'], all_cols)
        default_rating = find_col(['rating', 'score', 'review', 'stars'], numeric_cols)
        default_quantity = find_col(['quantity', 'qty', 'units', 'count'], numeric_cols)

        sales_col = st.selectbox("💰 Sales column", numeric_cols,
                                 index=numeric_cols.index(default_sales) if default_sales in numeric_cols else 0)
        product_col = st.selectbox("📦 Product column", all_cols,
                                   index=all_cols.index(default_product) if default_product in all_cols else 0)
        category_col = st.selectbox("🏷️ Category column", all_cols,
                                    index=all_cols.index(default_category) if default_category in all_cols else 0)
        branch_col = st.selectbox("🏪 Branch/Location column", all_cols,
                                  index=all_cols.index(default_branch) if default_branch in all_cols else 0)
        payment_col = st.selectbox("💳 Payment column", all_cols,
                                   index=all_cols.index(default_payment) if default_payment in all_cols else 0)
        customer_col = st.selectbox("👤 Customer type column", all_cols,
                                    index=all_cols.index(default_customer) if default_customer in all_cols else 0)
        rating_col = st.selectbox("⭐ Rating column", numeric_cols,
                                  index=numeric_cols.index(default_rating) if default_rating in numeric_cols else 0)
        quantity_col = st.selectbox("📊 Quantity column", numeric_cols,
                                   index=numeric_cols.index(default_quantity) if default_quantity in numeric_cols else 0)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN CONTENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if df is None:
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                min-height:60vh; text-align:center;">
        <div style="font-size:4rem; margin-bottom:1.5rem;">🛒</div>
        <h1 style="font-size:2.8rem !important; margin-bottom:0.5rem;">Supermarket Sales Analytics</h1>
        <p style="color:rgba(255,255,255,0.4); font-size:1.1rem; max-width:500px; line-height:1.7;">
            Upload a CSV, Excel, or ODS file from the sidebar to begin your analysis.
            The dashboard will dynamically adapt to your data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── HEADER ──
st.markdown("# Supermarket Sales Analytics")
st.markdown(f"*Dynamic insights from **{len(df):,}** transactions across **{df[product_col].nunique()}** products*")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KPI CARDS — Bento Grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("## Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

total_sales = df[sales_col].sum()
avg_transaction = df[sales_col].mean()
total_transactions = len(df)
avg_rating = df[rating_col].mean()
top_product = df.groupby(product_col)[sales_col].sum().idxmax()
top_payment = df[payment_col].value_counts().idxmax()

kpi1.metric("Total Revenue", f"₹{total_sales:,.0f}")
kpi2.metric("Avg Transaction", f"₹{avg_transaction:,.0f}")
kpi3.metric("Total Orders", f"{total_transactions:,}")
kpi4.metric("Avg Rating", f"{avg_rating:.2f} ⭐")
kpi5.metric("Top Product", top_product)
kpi6.metric("Top Payment", top_payment)

st.markdown("---")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANALYSIS TABS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📦 Products", "🏪 Branches", "🏷️ Categories",
    "💳 Payments", "👤 Customers", "⭐ Ratings", "📋 Raw Data"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: PRODUCT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## Which Product Generates the Highest Sales?")

    col1, col2 = st.columns([3, 2])

    with col1:
        product_sales = df.groupby(product_col)[sales_col].sum().sort_values(ascending=True).reset_index()
        fig = px.bar(product_sales, x=sales_col, y=product_col, orientation='h',
                     color=sales_col, color_continuous_scale=['#2a2a4a', '#7c7cf0'],
                     text=product_sales[sales_col].apply(lambda x: f'₹{x:,.0f}'))
        fig.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.6)'))
        fig.update_coloraxes(showscale=False)
        fig = style_fig(fig, height=500)
        fig.update_layout(title='Total Sales by Product', xaxis_title='', yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top 5 products summary
        top5 = df.groupby(product_col)[sales_col].sum().nlargest(5).reset_index()
        fig2 = px.pie(top5, values=sales_col, names=product_col, hole=0.6,
                      color_discrete_sequence=CHART_COLORS)
        fig2.update_traces(textinfo='label+percent', textfont=dict(family='Plus Jakarta Sans', size=11))
        fig2 = style_fig(fig2, height=400)
        fig2.update_layout(title='Top 5 Products Share', showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    winner = df.groupby(product_col)[sales_col].sum().idxmax()
    winner_val = df.groupby(product_col)[sales_col].sum().max()
    st.info(f"🏆 **{winner}** generated the highest total sales: **₹{winner_val:,.2f}**")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: BRANCH ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("## Which Branch Performs Best?")

    branch_stats = df.groupby(branch_col).agg(
        Total_Sales=(sales_col, 'sum'),
        Transactions=(sales_col, 'count'),
        Avg_Transaction=(sales_col, 'mean'),
        Avg_Rating=(rating_col, 'mean')
    ).reset_index().sort_values('Total_Sales', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(branch_stats, x=branch_col, y='Total_Sales',
                     color=branch_col, color_discrete_sequence=CHART_COLORS,
                     text=branch_stats['Total_Sales'].apply(lambda x: f'₹{x:,.0f}'))
        fig.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=11))
        fig = style_fig(fig)
        fig.update_layout(title='Total Sales by Branch', showlegend=False, xaxis_title='', yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(branch_stats, values='Total_Sales', names=branch_col,
                      color_discrete_sequence=CHART_COLORS, hole=0.55)
        fig2.update_traces(textinfo='label+percent', textfont=dict(family='Plus Jakarta Sans', size=12))
        fig2 = style_fig(fig2)
        fig2.update_layout(title='Revenue Share by Branch')
        st.plotly_chart(fig2, use_container_width=True)

    # Branch performance table
    st.markdown("### Branch Performance Summary")
    display_stats = branch_stats.copy()
    display_stats['Total_Sales'] = display_stats['Total_Sales'].apply(lambda x: f'₹{x:,.2f}')
    display_stats['Avg_Transaction'] = display_stats['Avg_Transaction'].apply(lambda x: f'₹{x:,.2f}')
    display_stats['Avg_Rating'] = display_stats['Avg_Rating'].apply(lambda x: f'{x:.2f} ⭐')
    st.dataframe(display_stats, use_container_width=True, hide_index=True)

    best_branch = branch_stats.iloc[0][branch_col]
    best_sales = branch_stats.iloc[0]['Total_Sales']
    st.info(f"🏆 **{best_branch}** performed best with total sales of **₹{best_sales:,.2f}**")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: CATEGORY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("## Which Category Sells the Most?")

    cat_sales = df.groupby(category_col)[sales_col].sum().sort_values(ascending=False).reset_index()

    col1, col2 = st.columns([3, 2])

    with col1:
        fig = px.bar(cat_sales, x=category_col, y=sales_col,
                     color=category_col, color_discrete_sequence=CHART_COLORS,
                     text=cat_sales[sales_col].apply(lambda x: f'₹{x:,.0f}'))
        fig.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=11))
        fig = style_fig(fig, height=450)
        fig.update_layout(title='Total Sales by Category', showlegend=False, xaxis_title='', yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.treemap(cat_sales, path=[category_col], values=sales_col,
                          color=sales_col, color_continuous_scale=['#1a1a3a', '#7c7cf0'])
        fig2.update_traces(textinfo='label+value', texttemplate='%{label}<br>₹%{value:,.0f}',
                          textfont=dict(family='Plus Jakarta Sans', size=13))
        fig2.update_coloraxes(showscale=False)
        fig2 = style_fig(fig2, height=450)
        fig2.update_layout(title='Category Treemap')
        st.plotly_chart(fig2, use_container_width=True)

    top_cat = cat_sales.iloc[0]
    st.info(f"🏆 **{top_cat[category_col]}** had the highest sales: **₹{top_cat[sales_col]:,.2f}**")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: PAYMENT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("## What is the Most Popular Payment Method?")

    payment_counts = df[payment_col].value_counts().reset_index()
    payment_counts.columns = [payment_col, 'Count']
    payment_revenue = df.groupby(payment_col)[sales_col].sum().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(payment_counts, x=payment_col, y='Count',
                     color=payment_col, color_discrete_sequence=CHART_COLORS,
                     text='Count')
        fig.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=13, color='white'))
        fig = style_fig(fig)
        fig.update_layout(title='Transaction Count by Payment Method', showlegend=False,
                         xaxis_title='', yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(payment_revenue, x=payment_col, y=sales_col,
                      color=payment_col, color_discrete_sequence=CHART_COLORS,
                      text=payment_revenue[sales_col].apply(lambda x: f'₹{x:,.0f}'))
        fig2.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=11))
        fig2 = style_fig(fig2)
        fig2.update_layout(title='Total Revenue by Payment Method', showlegend=False,
                          xaxis_title='', yaxis_title='')
        st.plotly_chart(fig2, use_container_width=True)

    top_pay = payment_counts.iloc[0]
    st.info(f"🏆 **{top_pay[payment_col]}** was the most popular payment method with **{top_pay['Count']}** transactions")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5: CUSTOMER ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("## Do Members Spend More Than Normal Customers?")

    cust_stats = df.groupby(customer_col).agg(
        Total_Sales=(sales_col, 'sum'),
        Transactions=(sales_col, 'count'),
        Avg_Transaction=(sales_col, 'mean'),
        Median_Transaction=(sales_col, 'median')
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(df, x=customer_col, y=sales_col, color=customer_col,
                     color_discrete_sequence=[CHART_COLORS[0], CHART_COLORS[1]])
        fig = style_fig(fig, height=450)
        fig.update_layout(title='Sales Distribution by Customer Type', showlegend=False,
                         xaxis_title='', yaxis_title='Sales (₹)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.violin(df, x=customer_col, y=sales_col, color=customer_col,
                         color_discrete_sequence=[CHART_COLORS[0], CHART_COLORS[1]], box=True)
        fig2 = style_fig(fig2, height=450)
        fig2.update_layout(title='Sales Violin Plot', showlegend=False,
                          xaxis_title='', yaxis_title='Sales (₹)')
        st.plotly_chart(fig2, use_container_width=True)

    # Avg transaction comparison
    fig3 = px.bar(cust_stats, x=customer_col, y='Avg_Transaction',
                  color=customer_col, color_discrete_sequence=[CHART_COLORS[0], CHART_COLORS[1]],
                  text=cust_stats['Avg_Transaction'].apply(lambda x: f'₹{x:,.2f}'))
    fig3.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=13))
    fig3 = style_fig(fig3, height=350)
    fig3.update_layout(title='Average Transaction Value Comparison', showlegend=False,
                      xaxis_title='', yaxis_title='')
    st.plotly_chart(fig3, use_container_width=True)

    if len(cust_stats) >= 2:
        sorted_cust = cust_stats.sort_values('Avg_Transaction', ascending=False)
        top_cust = sorted_cust.iloc[0]
        bot_cust = sorted_cust.iloc[1]
        diff = top_cust['Avg_Transaction'] - bot_cust['Avg_Transaction']
        st.info(f"🏆 **{top_cust[customer_col]}** spend more on average (₹{top_cust['Avg_Transaction']:,.2f}) "
                f"vs **{bot_cust[customer_col]}** (₹{bot_cust['Avg_Transaction']:,.2f}) — "
                f"Difference: **₹{abs(diff):,.2f}**")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6: RATING ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    st.markdown("## Customer Rating Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(df, x=rating_col, nbins=20, color_discrete_sequence=[CHART_COLORS[3]],
                          marginal='box')
        fig.add_vline(x=df[rating_col].mean(), line_dash='dash', line_color=CHART_COLORS[0],
                     annotation_text=f"Mean: {df[rating_col].mean():.2f}",
                     annotation_font=dict(family='JetBrains Mono', size=12, color=CHART_COLORS[0]))
        fig = style_fig(fig, height=420)
        fig.update_layout(title='Rating Distribution', xaxis_title='Rating', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        branch_rating = df.groupby(branch_col)[rating_col].mean().sort_values(ascending=False).reset_index()
        fig2 = px.bar(branch_rating, x=branch_col, y=rating_col,
                      color=branch_col, color_discrete_sequence=CHART_COLORS,
                      text=branch_rating[rating_col].apply(lambda x: f'{x:.2f}'))
        fig2.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', size=13))
        fig2 = style_fig(fig2, height=420)
        fig2.update_layout(title='Average Rating by Branch', showlegend=False,
                          xaxis_title='', yaxis_title='Avg Rating')
        st.plotly_chart(fig2, use_container_width=True)

    # Rating heatmap: Category × Branch
    if category_col != branch_col:
        pivot = df.pivot_table(values=rating_col, index=category_col, columns=branch_col, aggfunc='mean')
        fig3 = px.imshow(pivot, text_auto='.2f', color_continuous_scale=['#0a0a2a', '#3a3a7a', '#7c7cf0', '#b0b0ff'],
                        aspect='auto')
        fig3 = style_fig(fig3, height=400)
        fig3.update_layout(title='Average Rating: Category × Branch')
        st.plotly_chart(fig3, use_container_width=True)

    st.info(f"⭐ The average customer rating is **{df[rating_col].mean():.2f}** out of {df[rating_col].max():.0f}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 7: RAW DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
with tab7:
    st.markdown("## Raw Data Explorer")
    st.markdown("*Browse, filter, and search your complete dataset*")

    # Correlation matrix for numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) >= 2:
        corr = numeric_df.corr()
        fig = px.imshow(corr, text_auto='.2f', color_continuous_scale=['#f07c7c', '#1a1a3a', '#7c7cf0'],
                       aspect='auto', zmin=-1, zmax=1)
        fig = style_fig(fig, height=400)
        fig.update_layout(title='Correlation Matrix')
        st.plotly_chart(fig, use_container_width=True)

    # Full dataset
    st.dataframe(df, use_container_width=True, height=500)

    # Download button
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="supermarket_sales_export.csv",
        mime="text/csv"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; color:rgba(255,255,255,0.2); font-size:0.75rem;
            font-family:'Plus Jakarta Sans', sans-serif; letter-spacing:0.1em;">
    SUPERMARKET SALES ANALYTICS • BUILT WITH STREAMLIT & PLOTLY
</div>
""", unsafe_allow_html=True)
