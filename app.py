import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import io
import os
import joblib

warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Gem · Price Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e4dc;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f17 !important;
    border-right: 1px solid #2a2a3a;
}
[data-testid="stSidebar"] * {
    color: #b8b4ac !important;
}

/* Hero title */
.gem-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.8rem;
    font-weight: 300;
    letter-spacing: 0.15em;
    color: #e8e4dc;
    line-height: 1.1;
}
.gem-subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.2rem;
    color: #8a7f6e;
    letter-spacing: 0.2em;
    margin-top: -0.3rem;
}
.gem-accent {
    color: #c9a96e;
}

/* Metric cards */
.metric-card {
    background: #13131e;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #c9a96e;
}
.metric-label {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #6a6560;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    color: #e8e4dc;
    line-height: 1;
}
.metric-delta {
    font-size: 0.7rem;
    color: #7ab87a;
    margin-top: 0.3rem;
}
.metric-delta.neg { color: #b87a7a; }

/* Section headers */
.section-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 300;
    letter-spacing: 0.12em;
    color: #e8e4dc;
    border-bottom: 1px solid #2a2a3a;
    padding-bottom: 0.6rem;
    margin: 2rem 0 1.2rem 0;
}
.section-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    color: #c9a96e;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}

/* Price output box */
.price-result {
    background: linear-gradient(135deg, #13131e 0%, #1a1a28 100%);
    border: 1px solid #c9a96e44;
    border-radius: 6px;
    padding: 2rem;
    text-align: center;
}
.price-main {
    font-family: 'Cormorant Garamond', serif;
    font-size: 4rem;
    font-weight: 300;
    color: #c9a96e;
    line-height: 1;
}
.price-range {
    font-size: 0.75rem;
    color: #6a6560;
    letter-spacing: 0.2em;
    margin-top: 0.6rem;
}
.price-range span {
    color: #b8b4ac;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0f0f17;
    border-bottom: 1px solid #2a2a3a;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6a6560 !important;
    border-radius: 0;
    padding: 0.8rem 1.6rem;
}
.stTabs [aria-selected="true"] {
    color: #c9a96e !important;
    border-bottom: 2px solid #c9a96e !important;
    background: transparent !important;
}

/* Buttons */
.stButton > button {
    background: #c9a96e;
    color: #0a0a0f;
    border: none;
    border-radius: 2px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    padding: 0.7rem 2rem;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #dfc08a;
    transform: translateY(-1px);
}

/* Inputs */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider {
    background: #13131e !important;
    border-color: #2a2a3a !important;
    color: #e8e4dc !important;
    border-radius: 2px !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #13131e;
    border: 1px dashed #2a2a3a;
    border-radius: 4px;
    padding: 1rem;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #2a2a3a;
}

/* Divider */
hr {
    border-color: #2a2a3a !important;
}

/* Tag pills */
.tag-pill {
    display: inline-block;
    background: #1e1e2e;
    border: 1px solid #2a2a3a;
    border-radius: 2px;
    padding: 0.15rem 0.6rem;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #8a7f6e;
    margin: 0.15rem;
    text-transform: uppercase;
}

/* Info box */
.info-box {
    background: #13131e;
    border-left: 3px solid #c9a96e;
    border-radius: 0 4px 4px 0;
    padding: 0.9rem 1.2rem;
    font-size: 0.8rem;
    color: #8a7f6e;
    line-height: 1.6;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 2px; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False)
def load_and_prepare(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.columns = df.columns.str.strip()
    df["Order_Datetime"] = pd.to_datetime(
        df["Order_Datetime"], infer_datetime_format=True, errors="coerce"
    )
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["order_hour"]      = df["Order_Datetime"].dt.hour
    df["order_dayofweek"] = df["Order_Datetime"].dt.dayofweek
    df["order_month"]     = df["Order_Datetime"].dt.month
    df["order_quarter"]   = df["Order_Datetime"].dt.quarter
    df["order_year"]      = df["Order_Datetime"].dt.year
    df["is_weekend"]      = df["order_dayofweek"].isin([5, 6]).astype(int)

    df["Brand_ID_filled"] = df["Brand_ID"].fillna(-1)
    brand_stats = df.groupby("Brand_ID_filled")["Price_USD"].agg(
        brand_avg_price="mean", brand_median_price="median"
    ).reset_index()
    df = df.merge(brand_stats, on="Brand_ID_filled", how="left")
    df["price_vs_brand_avg"] = df["Price_USD"] / (df["brand_avg_price"] + 1)

    cat_stats = df.groupby("Category")["Price_USD"].agg(
        category_median_price="median", category_price_std="std"
    ).reset_index()
    df = df.merge(cat_stats, on="Category", how="left")

    for col, new_col in [("Main_Gem", "gem_rarity"),
                          ("Main_Metal", "metal_rarity"),
                          ("Main_Color", "color_rarity")]:
        freq = df[col].value_counts(normalize=True)
        df[new_col] = df[col].map(freq).fillna(freq.mean())
        df[new_col] = 1 / (df[new_col] + 1e-6)

    cust_stats = df.groupby("User_ID").agg(
        customer_order_count=("Order_ID", "count"),
        customer_avg_spend=("Price_USD", "mean")
    ).reset_index()
    df = df.merge(cust_stats, on="User_ID", how="left")

    df["metal_gem_combo"]   = df["Main_Metal"].astype(str) + "_" + df["Main_Gem"].astype(str)
    df["gender_category"]   = df["Target_Gender"].astype(str) + "_" + df["Category"].astype(str)
    df["metal_color_combo"] = df["Main_Metal"].astype(str) + "_" + df["Main_Color"].astype(str)
    return df


def dark_fig(figsize=(10, 4)):
    fig, ax = plt.subplots(figsize=figsize, facecolor="#0a0a0f")
    ax.set_facecolor("#13131e")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a3a")
    ax.tick_params(colors="#6a6560", labelsize=8)
    ax.xaxis.label.set_color("#6a6560")
    ax.yaxis.label.set_color("#6a6560")
    ax.title.set_color("#e8e4dc")
    return fig, ax


GOLD   = "#c9a96e"
SILVER = "#8a9bb8"
MUTED  = "#6a6560"
BG2    = "#13131e"
BORDER = "#2a2a3a"


# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='padding: 1.2rem 0 1.8rem 0;'>
        <div style='font-family: Cormorant Garamond, serif; font-size: 1.5rem;
                    font-weight: 300; letter-spacing: 0.2em; color: #c9a96e;'>
            GEM
        </div>
        <div style='font-size: 0.6rem; letter-spacing: 0.3em; color: #6a6560;
                    text-transform: uppercase; margin-top: 0.1rem;'>
            Price Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**DATA SOURCE**")
    uploaded = st.file_uploader(
        "Upload jewelry_orders.csv",
        type=["csv"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**NAVIGATION**")
    page = st.radio(
        "",
        ["📊  Overview", "🔍  Analysis", "🤖  Model Training", "💎  Price Predictor"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div class='info-box'>
        Upload your dataset to unlock all features. The app runs the full
        ML pipeline: EDA → Feature Engineering → Model Training → SHAP Explainability.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.6rem; color: #3a3530; letter-spacing: 0.15em;
                text-transform: uppercase;'>
        Gem v1.0 · Price Intelligence Suite
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════

df_raw = None
df     = None

if uploaded:
    with st.spinner("Parsing dataset…"):
        df_raw = load_and_prepare(uploaded.getvalue())
    if df_raw["Order_Datetime"].isna().all():
        st.error("Could not parse Order_Datetime. Check date format.")
        df_raw = None


# ══════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════

st.markdown("""
<div style='margin-bottom: 2rem;'>
    <div class='gem-title'>
        <span class='gem-accent'>Gem</span> · Price<br>Intelligence
    </div>
    <div class='gem-subtitle'>Jewelry Market Optimization Engine</div>
</div>
""", unsafe_allow_html=True)

if df_raw is None:
    # Landing state
    c1, c2, c3 = st.columns(3)
    for col, icon, label, desc in [
        (c1, "◈", "Upload CSV", "Drop your jewelry_orders.csv in the sidebar to begin"),
        (c2, "◉", "Train Models", "XGBoost · LightGBM · RandomForest benchmarked automatically"),
        (c3, "◊", "Get Prices", "Enter product attributes and receive optimal price predictions"),
    ]:
        with col:
            st.markdown(f"""
            <div class='metric-card' style='text-align:center; padding: 2rem 1rem;'>
                <div style='font-size:2rem; color:#c9a96e; margin-bottom:0.8rem;'>{icon}</div>
                <div style='font-family: Cormorant Garamond, serif; font-size: 1.2rem;
                            color: #e8e4dc; margin-bottom: 0.5rem;'>{label}</div>
                <div style='font-size: 0.72rem; color: #6a6560; line-height: 1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════

if page == "📊  Overview":
    # Top metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        ("TOTAL ORDERS",    f"{len(df_raw):,}",               None),
        ("AVG PRICE",       f"${df_raw['Price_USD'].mean():.0f}", None),
        ("MEDIAN PRICE",    f"${df_raw['Price_USD'].median():.0f}", None),
        ("CATEGORIES",      str(df_raw['Category'].nunique()), None),
        ("BRANDS",          str(int(df_raw['Brand_ID'].nunique())), None),
    ]
    for col, (label, value, delta) in zip([m1, m2, m3, m4, m5], metrics):
        with col:
            delta_html = f"<div class='metric-delta'>{delta}</div>" if delta else ""
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value}</div>
                {delta_html}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Price distribution + Category breakdown
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("<div class='section-tag'>distribution</div><div class='section-header'>Price Distribution</div>", unsafe_allow_html=True)
        fig, ax = dark_fig((8, 3.5))
        prices = df_raw["Price_USD"].dropna()
        ax.hist(prices, bins=80, color=GOLD, alpha=0.7, edgecolor="none")
        ax.set_xlabel("Price (USD)", fontsize=9)
        ax.set_ylabel("Orders", fontsize=9)
        ax.set_title("")
        # Log scale toggle
        log_scale = st.checkbox("Log scale", value=True, key="log_dist")
        if log_scale:
            ax.set_yscale("log")
        ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_b:
        st.markdown("<div class='section-tag'>breakdown</div><div class='section-header'>By Category</div>", unsafe_allow_html=True)
        cat_med = (
            df_raw.groupby("Category")["Price_USD"]
            .median().sort_values(ascending=True).tail(10)
        )
        fig, ax = dark_fig((5, 3.5))
        bars = ax.barh(cat_med.index, cat_med.values, color=GOLD, alpha=0.8, height=0.6)
        ax.set_xlabel("Median Price (USD)", fontsize=9)
        ax.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.5)
        for bar, val in zip(bars, cat_med.values):
            ax.text(val + 2, bar.get_y() + bar.get_height() / 2,
                    f"${val:.0f}", va="center", fontsize=7, color=MUTED)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # Time series + Missing values
    col_c, col_d = st.columns([3, 2])

    with col_c:
        st.markdown("<div class='section-tag'>temporal</div><div class='section-header'>Orders Over Time</div>", unsafe_allow_html=True)
        ts = df_raw.set_index("Order_Datetime")["Price_USD"].resample("W").agg(["count", "mean"])
        fig, ax1 = dark_fig((8, 3))
        ax2 = ax1.twinx()
        ax1.fill_between(ts.index, ts["count"], color=GOLD, alpha=0.2)
        ax1.plot(ts.index, ts["count"], color=GOLD, linewidth=1.5, label="Orders")
        ax2.plot(ts.index, ts["mean"], color=SILVER, linewidth=1, linestyle="--", label="Avg Price")
        ax2.tick_params(colors="#6a6560", labelsize=8)
        ax2.set_facecolor("#13131e")
        ax1.set_xlabel("Week", fontsize=9)
        ax1.set_ylabel("Order Count", fontsize=9, color=GOLD)
        ax2.set_ylabel("Avg Price (USD)", fontsize=9, color=SILVER)
        ax1.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.5)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_d:
        st.markdown("<div class='section-tag'>data quality</div><div class='section-header'>Null Coverage</div>", unsafe_allow_html=True)
        miss = (df_raw.isnull().mean() * 100).sort_values(ascending=True)
        miss = miss[miss > 0]
        fig, ax = dark_fig((5, 3))
        colors = [GOLD if v < 10 else "#b87a7a" if v > 40 else SILVER for v in miss.values]
        ax.barh(miss.index, miss.values, color=colors, height=0.6, alpha=0.85)
        ax.set_xlabel("% Missing", fontsize=9)
        ax.axvline(x=50, color=BORDER, linestyle="--", linewidth=0.8)
        for i, (col_name, val) in enumerate(miss.items()):
            ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=7, color=MUTED)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # Raw data preview
    st.markdown("<div class='section-tag'>raw data</div><div class='section-header'>Dataset Preview</div>", unsafe_allow_html=True)
    st.dataframe(
        df_raw.head(50).style.format({"Price_USD": "${:.2f}", "SKU_Quality": "{:.0f}"}),
        use_container_width=True, height=280
    )


# ══════════════════════════════════════════════════════════
# PAGE: ANALYSIS
# ══════════════════════════════════════════════════════════

elif page == "🔍  Analysis":
    st.markdown("<div class='section-tag'>deep dive</div>", unsafe_allow_html=True)
    st.markdown("<div class='gem-title' style='font-size:2.2rem;'>Feature Analysis</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["METAL & GEM", "COLOR & GENDER", "CORRELATIONS"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Price by Main Metal**")
            metal_order = (
                df_raw.groupby("Main_Metal")["Price_USD"]
                .median().sort_values(ascending=False).index
            )
            fig, ax = dark_fig((6, 4))
            data_metal = [df_raw[df_raw["Main_Metal"] == m]["Price_USD"].dropna()
                          for m in metal_order]
            bp = ax.boxplot(data_metal, patch_artist=True, widths=0.5,
                            medianprops=dict(color=GOLD, linewidth=2))
            for patch in bp["boxes"]:
                patch.set_facecolor(BG2)
                patch.set_edgecolor(BORDER)
            for whisker in bp["whiskers"]:
                whisker.set_color(BORDER)
            for cap in bp["caps"]:
                cap.set_color(BORDER)
            ax.set_xticklabels(metal_order, rotation=35, ha="right", fontsize=8)
            ax.set_ylabel("Price (USD)", fontsize=9)
            ax.set_yscale("log")
            ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        with col2:
            st.markdown("**Price by Main Gem**")
            gem_order = (
                df_raw.groupby("Main_Gem")["Price_USD"]
                .median().sort_values(ascending=False).head(12).index
            )
            gem_med = df_raw[df_raw["Main_Gem"].isin(gem_order)].groupby("Main_Gem")["Price_USD"].median().reindex(gem_order)
            fig, ax = dark_fig((6, 4))
            colors_gem = plt.cm.YlOrBr(np.linspace(0.3, 0.9, len(gem_med)))
            ax.bar(range(len(gem_med)), gem_med.values, color=colors_gem, alpha=0.85, width=0.7)
            ax.set_xticks(range(len(gem_med)))
            ax.set_xticklabels(gem_med.index, rotation=40, ha="right", fontsize=8)
            ax.set_ylabel("Median Price (USD)", fontsize=9)
            ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # Metal × Gem heatmap
        st.markdown("**Metal × Gem Median Price Heatmap**")
        pivot = df_raw.pivot_table(values="Price_USD", index="Main_Metal",
                                    columns="Main_Gem", aggfunc="median")
        top_gems   = df_raw["Main_Gem"].value_counts().head(8).index
        top_metals = df_raw["Main_Metal"].value_counts().head(8).index
        pivot = pivot.loc[
            pivot.index.isin(top_metals),
            pivot.columns.isin(top_gems)
        ].dropna(how="all")

        fig, ax = dark_fig((10, 4))
        sns.heatmap(pivot, ax=ax, cmap="YlOrBr", linewidths=0.5,
                    linecolor=BG2, annot=True, fmt=".0f",
                    annot_kws={"size": 7, "color": "#0a0a0f"},
                    cbar_kws={"shrink": 0.7})
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Price by Main Color**")
            color_med = (
                df_raw.groupby("Main_Color")["Price_USD"]
                .agg(["median", "count"])
                .query("count >= 50")
                .sort_values("median", ascending=True)
                .tail(15)
            )
            fig, ax = dark_fig((6, 4.5))
            ax.barh(color_med.index, color_med["median"],
                    color=GOLD, alpha=0.75, height=0.65)
            ax.set_xlabel("Median Price (USD)", fontsize=9)
            ax.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.5)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        with col2:
            st.markdown("**Price by Target Gender**")
            gender_data = df_raw.dropna(subset=["Target_Gender"])
            genders = gender_data["Target_Gender"].unique()
            fig, ax = dark_fig((6, 4.5))
            palette = [GOLD, SILVER, "#9b7eb8"]
            for i, g in enumerate(genders):
                vals = gender_data[gender_data["Target_Gender"] == g]["Price_USD"].dropna()
                ax.hist(vals, bins=50, alpha=0.6,
                        color=palette[i % len(palette)], label=g)
            ax.set_xlabel("Price (USD)", fontsize=9)
            ax.set_ylabel("Count", fontsize=9)
            ax.set_yscale("log")
            ax.legend(fontsize=8, facecolor=BG2, edgecolor=BORDER,
                      labelcolor="#b8b4ac")
            ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # SKU Quality
        st.markdown("**SKU Quality vs Price**")
        fig, ax = dark_fig((10, 3.5))
        sku_med = df_raw.groupby("SKU_Quality")["Price_USD"].median()
        ax.bar(sku_med.index, sku_med.values, color=GOLD, alpha=0.8, width=0.7)
        ax.set_xlabel("SKU Quality", fontsize=9)
        ax.set_ylabel("Median Price (USD)", fontsize=9)
        ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with tab3:
        st.markdown("**Numeric Feature Correlation Matrix**")
        num_cols = df_raw.select_dtypes(include="number").columns.tolist()
        corr = df_raw[num_cols].corr()
        fig, ax = dark_fig((8, 6))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, ax=ax, mask=mask, cmap="RdYlGn",
                    center=0, vmin=-1, vmax=1,
                    linewidths=0.5, linecolor=BG2,
                    annot=True, fmt=".2f",
                    annot_kws={"size": 7},
                    cbar_kws={"shrink": 0.7})
        ax.tick_params(labelsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()


# ══════════════════════════════════════════════════════════
# PAGE: MODEL TRAINING
# ══════════════════════════════════════════════════════════

elif page == "🤖  Model Training":
    st.markdown("<div class='section-tag'>machine learning</div>", unsafe_allow_html=True)
    st.markdown("<div class='gem-title' style='font-size:2.2rem;'>Model Training</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_ctrl, col_info = st.columns([1, 2])
    with col_ctrl:
        st.markdown("**TRAINING OPTIONS**")
        test_size   = st.slider("Test size %", 10, 30, 20) / 100
        n_estimators = st.select_slider("Trees / estimators",
                                         options=[100, 200, 300, 500], value=200)
        run_shap    = st.checkbox("Run SHAP explainability", value=True)
        train_btn   = st.button("▶  TRAIN MODELS")

    with col_info:
        st.markdown("""
        <div class='info-box'>
            <strong style='color: #c9a96e;'>Pipeline summary</strong><br><br>
            Feature engineering → mutual-info selection → StandardScaler + OrdinalEncoder
            → Ridge · RandomForest · XGBoost · LightGBM benchmarked on validation set
            → best model evaluated on held-out test set → SHAP global + local explanations.
        </div>
        """, unsafe_allow_html=True)

    if train_btn:
        from sklearn.model_selection  import train_test_split
        from sklearn.preprocessing    import StandardScaler, OrdinalEncoder
        from sklearn.impute           import SimpleImputer
        from sklearn.pipeline         import Pipeline
        from sklearn.compose          import ColumnTransformer
        from sklearn.ensemble         import RandomForestRegressor
        from sklearn.linear_model     import Ridge
        from sklearn.feature_selection import mutual_info_regression
        from sklearn.preprocessing    import LabelEncoder
        from sklearn.metrics          import mean_squared_error, mean_absolute_error, r2_score
        from xgboost                  import XGBRegressor
        from lightgbm                 import LGBMRegressor

        TARGET = "Price_USD"
        progress = st.progress(0, text="Engineering features…")

        df_feat = engineer_features(df_raw)
        progress.progress(15, text="Selecting features…")

        DROP = ["Order_Datetime", "Order_ID", "Product_ID", "User_ID",
                "Brand_ID", "Category_ID", "Brand_ID_filled", TARGET]
        feature_cols = [c for c in df_feat.columns if c not in DROP]

        df_enc = df_feat[feature_cols + [TARGET]].copy()
        df_enc.dropna(subset=[TARGET], inplace=True)
        for col in df_enc.select_dtypes(include="object").columns:
            df_enc[col] = LabelEncoder().fit_transform(df_enc[col].astype(str))
        df_enc.fillna(df_enc.median(numeric_only=True), inplace=True)

        X_sel = df_enc[feature_cols]
        y_sel = df_enc[TARGET]

        mi_scores = mutual_info_regression(X_sel, y_sel, random_state=42)
        mi_df = pd.Series(mi_scores, index=feature_cols).sort_values(ascending=False)
        MUST_KEEP = ["SKU_Quality", "brand_avg_price", "category_median_price",
                     "gem_rarity", "metal_rarity"]
        SELECTED = list(dict.fromkeys(MUST_KEEP + mi_df.head(18).index.tolist()))

        progress.progress(30, text="Splitting data…")
        df_model = df_feat[SELECTED + [TARGET]].dropna(subset=[TARGET]).copy()
        df_model["log_price"] = np.log1p(df_model[TARGET])
        X = df_model[SELECTED]
        y = df_model["log_price"]

        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size * 2, random_state=42)
        X_val, X_test, y_val, y_test     = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        num_f = X.select_dtypes(include="number").columns.tolist()
        cat_f = X.select_dtypes(include=["object", "category"]).columns.tolist()

        num_pipe = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())])
        cat_pipe = Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                              ("enc", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))])
        prep = ColumnTransformer([("num", num_pipe, num_f), ("cat", cat_pipe, cat_f)])

        X_train_pp = prep.fit_transform(X_train)
        X_val_pp   = prep.transform(X_val)
        X_test_pp  = prep.transform(X_test)

        progress.progress(45, text="Training models…")

        models = {
            "Ridge":        Ridge(alpha=1.0),
            "RandomForest": RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1, random_state=42),
            "XGBoost":      XGBRegressor(n_estimators=n_estimators, learning_rate=0.05,
                                          random_state=42, tree_method="hist", verbosity=0),
            "LightGBM":     LGBMRegressor(n_estimators=n_estimators, learning_rate=0.05,
                                           random_state=42, verbose=-1),
        }

        results = {}
        for name, mdl in models.items():
            mdl.fit(X_train_pp, y_train)
            p = mdl.predict(X_val_pp)
            yt = np.expm1(y_val); yp = np.expm1(p)
            results[name] = {
                "RMSE": np.sqrt(mean_squared_error(yt, yp)),
                "MAE":  mean_absolute_error(yt, yp),
                "R²":   r2_score(yt, yp),
                "MAPE": np.mean(np.abs((yt - yp) / (yt + 1e-8))) * 100,
            }

        progress.progress(70, text="Evaluating on test set…")
        best_name  = min(results, key=lambda k: results[k]["RMSE"])
        best_model = models[best_name]
        test_preds = best_model.predict(X_test_pp)
        yt_final   = np.expm1(y_test); yp_final = np.expm1(test_preds)
        test_results = {
            "RMSE": np.sqrt(mean_squared_error(yt_final, yp_final)),
            "MAE":  mean_absolute_error(yt_final, yp_final),
            "R²":   r2_score(yt_final, yp_final),
            "MAPE": np.mean(np.abs((yt_final - yp_final) / (yt_final + 1e-8))) * 100,
        }

        st.session_state["trained_model"]   = best_model
        st.session_state["preprocessor"]    = prep
        st.session_state["selected_feats"]  = SELECTED
        st.session_state["num_feats"]       = num_f
        st.session_state["cat_feats"]       = cat_f
        st.session_state["df_feat"]         = df_feat
        st.session_state["feature_names"]   = num_f + cat_f

        progress.progress(80, text="Rendering results…")

        # ── Results ───────────────────────────────────────
        st.markdown("<div class='section-header'>Validation Results</div>", unsafe_allow_html=True)

        res_df = pd.DataFrame(results).T.reset_index().rename(columns={"index": "Model"})
        col_a, col_b = st.columns([2, 3])

        with col_a:
            styled = res_df.style.format({
                "RMSE": "${:.2f}", "MAE": "${:.2f}", "R²": "{:.4f}", "MAPE": "{:.2f}%"
            }).highlight_min(subset=["RMSE", "MAE", "MAPE"], color="#1e2e1e"
            ).highlight_max(subset=["R²"], color="#1e2e1e")
            st.dataframe(styled, use_container_width=True, hide_index=True)

        with col_b:
            fig, axes = dark_fig((7, 3.5))
            fig, axes = plt.subplots(1, 2, figsize=(7, 3.5), facecolor="#0a0a0f")
            for ax in axes:
                ax.set_facecolor("#13131e")
                for spine in ax.spines.values():
                    spine.set_edgecolor(BORDER)
                ax.tick_params(colors="#6a6560", labelsize=8)

            model_names = res_df["Model"].tolist()
            x = np.arange(len(model_names))
            bar_colors = [GOLD if n == best_name else MUTED for n in model_names]

            axes[0].bar(x, res_df["RMSE"], color=bar_colors, alpha=0.85, width=0.6)
            axes[0].set_xticks(x); axes[0].set_xticklabels(model_names, rotation=20, ha="right", fontsize=8)
            axes[0].set_title("RMSE (USD)", fontsize=9, color="#e8e4dc")
            axes[0].grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)

            axes[1].bar(x, res_df["R²"], color=bar_colors, alpha=0.85, width=0.6)
            axes[1].set_xticks(x); axes[1].set_xticklabels(model_names, rotation=20, ha="right", fontsize=8)
            axes[1].set_title("R² Score", fontsize=9, color="#e8e4dc")
            axes[1].grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)

            gold_patch = mpatches.Patch(color=GOLD, label=f"Best: {best_name}")
            axes[0].legend(handles=[gold_patch], fontsize=7, facecolor=BG2,
                           edgecolor=BORDER, labelcolor="#b8b4ac")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # Test set metrics
        st.markdown("<div class='section-header'>Hold-out Test Set — Best Model</div>", unsafe_allow_html=True)
        tm1, tm2, tm3, tm4 = st.columns(4)
        for col, (k, fmt) in zip([tm1, tm2, tm3, tm4],
                                  [("RMSE", "${:.2f}"), ("MAE", "${:.2f}"),
                                   ("R²",   "{:.4f}"),  ("MAPE", "{:.2f}%")]):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>{k} ({best_name})</div>
                    <div class='metric-value'>{fmt.format(test_results[k])}</div>
                </div>
                """, unsafe_allow_html=True)

        # Actual vs predicted
        st.markdown("<div class='section-header'>Actual vs Predicted</div>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            fig, ax = dark_fig((6, 4))
            mn, mx = yt_final.min(), yt_final.max()
            ax.scatter(yt_final, yp_final, alpha=0.15, s=6, color=GOLD)
            ax.plot([mn, mx], [mn, mx], color=SILVER, linewidth=1, linestyle="--")
            ax.set_xlabel("Actual Price (USD)", fontsize=9)
            ax.set_ylabel("Predicted Price (USD)", fontsize=9)
            ax.set_title("Actual vs Predicted", fontsize=10, color="#e8e4dc")
            ax.grid(color=BORDER, linewidth=0.5, alpha=0.4)
            st.pyplot(fig, use_container_width=True)
            plt.close()
        with col_r2:
            fig, ax = dark_fig((6, 4))
            residuals = yt_final - yp_final
            ax.scatter(yp_final, residuals, alpha=0.15, s=6, color=SILVER)
            ax.axhline(0, color=GOLD, linewidth=1, linestyle="--")
            ax.set_xlabel("Predicted Price (USD)", fontsize=9)
            ax.set_ylabel("Residual (USD)", fontsize=9)
            ax.set_title("Residuals", fontsize=10, color="#e8e4dc")
            ax.grid(color=BORDER, linewidth=0.5, alpha=0.4)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # SHAP
        if run_shap and hasattr(best_model, "predict"):
            progress.progress(90, text="Computing SHAP values…")
            try:
                import shap
                feat_names = num_f + cat_f
                explainer   = shap.TreeExplainer(best_model)
                shap_vals   = explainer.shap_values(X_test_pp[:500])

                st.markdown("<div class='section-header'>SHAP Feature Importance</div>", unsafe_allow_html=True)
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    mean_abs = np.abs(shap_vals).mean(axis=0)
                    shap_df = pd.DataFrame({
                        "Feature":    feat_names,
                        "Mean |SHAP|": mean_abs,
                        "Direction":  pd.Series(np.sign(shap_vals.mean(axis=0))).map(
                                          {1.0: "↑ price", -1.0: "↓ price", 0.0: "neutral"})
                    }).sort_values("Mean |SHAP|", ascending=False).head(15)

                    fig, ax = dark_fig((6, 5))
                    colors_shap = [GOLD if d == "↑ price" else SILVER if d == "↓ price" else MUTED
                                   for d in shap_df["Direction"]]
                    ax.barh(shap_df["Feature"][::-1], shap_df["Mean |SHAP|"][::-1],
                            color=colors_shap[::-1], alpha=0.85, height=0.65)
                    ax.set_xlabel("Mean |SHAP Value|", fontsize=9)
                    ax.set_title("Global Feature Importance", fontsize=9, color="#e8e4dc")
                    ax.grid(axis="x", color=BORDER, linewidth=0.5, alpha=0.5)
                    legend_els = [
                        mpatches.Patch(color=GOLD, label="↑ increases price"),
                        mpatches.Patch(color=SILVER, label="↓ decreases price"),
                    ]
                    ax.legend(handles=legend_els, fontsize=7, facecolor=BG2,
                              edgecolor=BORDER, labelcolor="#b8b4ac")
                    st.pyplot(fig, use_container_width=True)
                    plt.close()

                with col_s2:
                    st.markdown("**Business Analyst Summary**")
                    st.dataframe(
                        shap_df.style.format({"Mean |SHAP|": "{:.4f}"}),
                        use_container_width=True, height=400, hide_index=True
                    )

                st.session_state["shap_vals"]  = shap_vals
                st.session_state["feat_names"] = feat_names

            except Exception as e:
                st.warning(f"SHAP skipped: {e}")

        progress.progress(100, text="Done!")
        st.success(f"✓ Training complete — best model: **{best_name}**  |  Test R²: {test_results['R²']:.4f}  |  RMSE: ${test_results['RMSE']:.2f}")


# ══════════════════════════════════════════════════════════
# PAGE: PRICE PREDICTOR
# ══════════════════════════════════════════════════════════

elif page == "💎  Price Predictor":
    st.markdown("<div class='section-tag'>optimization</div>", unsafe_allow_html=True)
    st.markdown("<div class='gem-title' style='font-size:2.2rem;'>Price Predictor</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if "trained_model" not in st.session_state:
        st.markdown("""
        <div class='info-box' style='font-size:0.9rem; padding: 1.5rem;'>
            ⚠️  No trained model found. Please go to <strong>🤖 Model Training</strong>
            and train a model first.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    model       = st.session_state["trained_model"]
    prep        = st.session_state["preprocessor"]
    SELECTED    = st.session_state["selected_feats"]
    df_feat_ref = st.session_state["df_feat"]

    def safe_unique(col):
        return sorted(df_raw[col].dropna().unique().tolist())

    col_form, col_result = st.columns([1, 1])

    with col_form:
        st.markdown("<div class='section-header'>Product Attributes</div>", unsafe_allow_html=True)

        with st.container():
            category    = st.selectbox("Category",    safe_unique("Category"))
            main_metal  = st.selectbox("Main Metal",  safe_unique("Main_Metal"))
            main_gem    = st.selectbox("Main Gem",     ["None"] + safe_unique("Main_Gem"))
            main_color  = st.selectbox("Main Color",  safe_unique("Main_Color"))
            gender      = st.selectbox("Target Gender", ["Unisex"] + safe_unique("Target_Gender"))
            sku_quality = st.slider("SKU Quality", int(df_raw["SKU_Quality"].min()),
                                    int(df_raw["SKU_Quality"].max()),
                                    int(df_raw["SKU_Quality"].median()))
            order_hour  = st.slider("Order Hour (0–23)", 0, 23, 12)
            order_month = st.slider("Order Month", 1, 12, 6)
            predict_btn = st.button("💎  CALCULATE OPTIMAL PRICE")

    with col_result:
        st.markdown("<div class='section-header'>Price Recommendation</div>", unsafe_allow_html=True)

        if predict_btn:
            main_gem_val = None if main_gem == "None" else main_gem
            gender_val   = gender

            # Compute aggregates from reference data
            brand_avg  = df_feat_ref["brand_avg_price"].median()
            brand_med  = df_feat_ref["brand_median_price"].median()
            cat_med_p  = df_feat_ref[df_feat_ref["Category"] == category]["category_median_price"].median()
            cat_std_p  = df_feat_ref[df_feat_ref["Category"] == category]["category_price_std"].median()
            if pd.isna(cat_med_p): cat_med_p = df_feat_ref["category_median_price"].median()
            if pd.isna(cat_std_p): cat_std_p = df_feat_ref["category_price_std"].median()

            gem_r   = df_feat_ref[df_feat_ref["Main_Gem"]   == main_gem_val]["gem_rarity"].median()   if main_gem_val else df_feat_ref["gem_rarity"].median()
            metal_r = df_feat_ref[df_feat_ref["Main_Metal"] == main_metal]["metal_rarity"].median()
            color_r = df_feat_ref[df_feat_ref["Main_Color"] == main_color]["color_rarity"].median()
            if pd.isna(gem_r):   gem_r   = df_feat_ref["gem_rarity"].median()
            if pd.isna(metal_r): metal_r = df_feat_ref["metal_rarity"].median()
            if pd.isna(color_r): color_r = df_feat_ref["color_rarity"].median()

            cust_cnt   = df_feat_ref["customer_order_count"].median()
            cust_spend = df_feat_ref["customer_avg_spend"].median()
            dow        = order_month % 7
            is_wknd    = int(dow in [5, 6])

            sample = {
                "SKU_Quality":           sku_quality,
                "order_hour":            order_hour,
                "order_dayofweek":       dow,
                "order_month":           order_month,
                "order_quarter":         (order_month - 1) // 3 + 1,
                "order_year":            2024,
                "is_weekend":            is_wknd,
                "brand_avg_price":       brand_avg,
                "brand_median_price":    brand_med,
                "price_vs_brand_avg":    1.0,
                "category_median_price": cat_med_p,
                "category_price_std":    cat_std_p,
                "gem_rarity":            gem_r,
                "metal_rarity":          metal_r,
                "color_rarity":          color_r,
                "customer_order_count":  cust_cnt,
                "customer_avg_spend":    cust_spend,
                "Category":              category,
                "Main_Metal":            main_metal,
                "Main_Gem":              str(main_gem_val),
                "Target_Gender":         gender_val,
                "Main_Color":            main_color,
                "metal_gem_combo":       f"{main_metal}_{main_gem_val}",
                "gender_category":       f"{gender_val}_{category}",
                "metal_color_combo":     f"{main_metal}_{main_color}",
            }

            try:
                row    = pd.DataFrame([sample])[SELECTED]
                row_pp = prep.transform(row)
                pred_log   = model.predict(row_pp)[0]
                pred_price = np.expm1(pred_log)
                ci_low  = pred_price * 0.85
                ci_high = pred_price * 1.15

                st.markdown(f"""
                <div class='price-result'>
                    <div style='font-size:0.65rem; letter-spacing:0.3em; color:#6a6560;
                                text-transform:uppercase; margin-bottom:0.8rem;'>
                        Optimal Price
                    </div>
                    <div class='price-main'>${pred_price:,.2f}</div>
                    <div class='price-range'>
                        Recommended range &nbsp;
                        <span>${ci_low:,.0f} – ${ci_high:,.0f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Comparable prices
                mask = (df_raw["Category"] == category) & (df_raw["Main_Metal"] == main_metal)
                if main_gem_val:
                    mask = mask & (df_raw["Main_Gem"] == main_gem_val)
                comparables = df_raw[mask]["Price_USD"].dropna()

                if len(comparables) > 5:
                    st.markdown("**Market Comparables**")
                    fig, ax = dark_fig((5, 2.5))
                    ax.hist(comparables, bins=40, color=GOLD, alpha=0.5)
                    ax.axvline(pred_price, color="#e8e4dc", linewidth=2, linestyle="--", label=f"Prediction ${pred_price:,.0f}")
                    ax.axvline(comparables.median(), color=SILVER, linewidth=1.5, linestyle=":", label=f"Market median ${comparables.median():,.0f}")
                    ax.axvspan(ci_low, ci_high, alpha=0.1, color=GOLD, label="Recommended range")
                    ax.legend(fontsize=7, facecolor=BG2, edgecolor=BORDER, labelcolor="#b8b4ac")
                    ax.set_xlabel("Price (USD)", fontsize=9)
                    ax.grid(axis="y", color=BORDER, linewidth=0.5, alpha=0.5)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()

                    cm1, cm2, cm3 = st.columns(3)
                    for c, (lbl, val) in zip([cm1, cm2, cm3], [
                        ("MARKET MEDIAN",  f"${comparables.median():,.0f}"),
                        ("MARKET P25",     f"${comparables.quantile(0.25):,.0f}"),
                        ("MARKET P75",     f"${comparables.quantile(0.75):,.0f}"),
                    ]):
                        with c:
                            st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-label'>{lbl}</div>
                                <div class='metric-value' style='font-size:1.4rem;'>{val}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    pct = (pred_price - comparables.median()) / comparables.median() * 100
                    direction = "above" if pct > 0 else "below"
                    st.markdown(f"""
                    <div class='info-box' style='margin-top:1rem;'>
                        Predicted price is <strong style='color:#c9a96e;'>{abs(pct):.1f}%
                        {direction}</strong> the market median for
                        {category} · {main_metal}{' · ' + main_gem_val if main_gem_val else ''}.
                        Based on {len(comparables):,} comparable orders.
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.markdown("""
            <div style='text-align:center; padding: 4rem 2rem; color: #3a3530;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>◊</div>
                <div style='font-size: 0.75rem; letter-spacing: 0.25em; text-transform: uppercase;'>
                    Configure product attributes<br>and click Calculate
                </div>
            </div>
            """, unsafe_allow_html=True)
