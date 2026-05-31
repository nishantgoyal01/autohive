import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="AutoHive | Car Market Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# PATH CONFIG
# =============================================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "database" / "cars.db"


# =============================================================================
# CONSTANTS
# =============================================================================
CHART_HEIGHT = 430


# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data(db_path: str) -> pd.DataFrame:
    db_file = Path(db_path)

    if not db_file.exists():
        return pd.DataFrame()

    try:
        with sqlite3.connect(db_file) as conn:
            df = pd.read_sql_query("SELECT * FROM cars", conn)
        return df

    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    required_columns = [
        "name",
        "brand",
        "year",
        "price",
        "km_driven",
        "fuel_type",
        "transmission",
        "location",
        "url",
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["km_driven"] = pd.to_numeric(df["km_driven"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    df = df.dropna(subset=["price", "km_driven"])

    df["name"] = df["name"].fillna("Unnamed Car")
    df["brand"] = df["brand"].fillna("Unknown")
    df["fuel_type"] = df["fuel_type"].fillna("Unknown")
    df["transmission"] = df["transmission"].fillna("Unknown")
    df["location"] = df["location"].fillna("Unknown")
    df["url"] = df["url"].fillna("")

    df["price"] = df["price"].astype(int)
    df["km_driven"] = df["km_driven"].astype(int)

    if df["year"].notna().any():
        df["year"] = df["year"].astype("Int64")

    # Remove duplicate listings.
    # Do not include URL because same car can appear with different URLs.
    df = df.drop_duplicates(
        subset=[
            "name",
            "brand",
            "year",
            "price",
            "km_driven",
            "fuel_type",
            "transmission",
            "location",
        ],
        keep="first",
    )

    # Deal score:
    # Lower score means listing price is cheaper than brand median.
    brand_median = df.groupby("brand")["price"].transform("median")
    df["deal_score"] = df["price"] / brand_median

    return df


df = load_data(str(DB_PATH))
df = prepare_data(df)


# =============================================================================
# EMPTY DATA HANDLING
# =============================================================================
if df.empty:
    st.title("🚗 AutoHive")
    st.warning("No valid car data found.")

    st.markdown(
        """
        Please run the complete pipeline first:

        ```bash
        python scraper/scrape_dynamic.py
        python analytics/clean_data.py
        streamlit run dashboard/app.py
        ```

        Expected database path:

        ```text
        database/cars.db
        ```
        """
    )

    st.stop()


# =============================================================================
# THEME
# =============================================================================
T = {
    "bg": "#080C14",
    "card": "#111827",
    "card2": "#1F2937",
    "text": "#F9FAFB",
    "muted": "#9CA3AF",
    "border": "#374151",
    "accent": "#6366F1",
    "accent2": "#818CF8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "template": "plotly_dark",
}


# =============================================================================
# CSS
# =============================================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {T["bg"]};
            color: {T["text"]};
        }}

        .block-container {{
            padding-top: 1rem;
            padding-left: 1.4rem;
            padding-right: 1.4rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }}

        header[data-testid="stHeader"] {{
            background: {T["card"]};
            border-bottom: 1px solid {T["border"]};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {T["card"]};
            border-right: 1px solid {T["border"]};
        }}

        div[data-testid="stVerticalBlock"] {{
            gap: 1rem;
        }}

        .autohive-topbar {{
            position: sticky;
            top: 0;
            z-index: 999;
            background: {T["card"]};
            border: 1px solid {T["border"]};
            border-radius: 18px;
            padding: 0.85rem 1.2rem;
            margin-bottom: 1.1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 8px 28px rgba(0,0,0,0.14);
        }}

        .autohive-topbar-title {{
            font-size: 1.3rem;
            font-weight: 900;
            color: {T["text"]};
            letter-spacing: -0.04em;
        }}

        .autohive-topbar-subtitle {{
            color: {T["muted"]};
            font-size: 0.82rem;
            margin-top: 0.1rem;
        }}

        .autohive-topbar-badge {{
            background: {T["card2"]};
            color: {T["text"]};
            border: 1px solid {T["border"]};
            border-radius: 999px;
            padding: 0.45rem 0.9rem;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .main-header {{
            padding: 1rem 0 1.2rem 0;
            border-bottom: 1px solid {T["border"]};
            margin-bottom: 1.2rem;
        }}

        .main-title {{
            font-size: 2rem;
            font-weight: 850;
            color: {T["text"]};
            margin-bottom: 0.2rem;
        }}

        .main-subtitle {{
            color: {T["muted"]};
            font-size: 0.95rem;
        }}

        .kpi-card {{
            background: {T["card"]};
            border: 1px solid {T["border"]};
            border-radius: 18px;
            padding: 1.05rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }}

        .kpi-label {{
            color: {T["muted"]};
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.4rem;
            font-weight: 700;
        }}

        .kpi-value {{
            color: {T["text"]};
            font-size: 1.35rem;
            font-weight: 850;
        }}

        .section-title {{
            font-size: 1.15rem;
            font-weight: 850;
            margin: 1.2rem 0 0.7rem 0;
            color: {T["text"]};
        }}

        .insight-card {{
            background: {T["card"]};
            border: 1px solid {T["border"]};
            border-radius: 16px;
            padding: 1.05rem;
            height: 100%;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }}

        .insight-label {{
            color: {T["muted"]};
            font-size: 0.72rem;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .insight-value {{
            color: {T["text"]};
            font-size: 1rem;
            font-weight: 800;
        }}

        .footer {{
            text-align: center;
            color: {T["muted"]};
            border-top: 1px solid {T["border"]};
            padding-top: 1rem;
            margin-top: 2rem;
            font-size: 0.85rem;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# CHART HELPERS
# =============================================================================
def apply_common_layout(fig, title: str, height: int = CHART_HEIGHT):
    fig.update_layout(
        title={
            "text": title,
            "x": 0.02,
            "xanchor": "left",
        },
        height=height,
        margin=dict(l=45, r=35, t=75, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T["text"]),
    )

    return fig


def format_price_lakh(value: float) -> str:
    return f"₹{value:.1f}L"


# =============================================================================
# AUTOHIVE TOP BAR
# =============================================================================
st.markdown(
    f"""
    <div class="autohive-topbar">
        <div>
            <div class="autohive-topbar-title">🚗 AutoHive</div>
            <div class="autohive-topbar-subtitle">
                Used-Car Market Intelligence Platform
            </div>
        </div>
        <div class="autohive-topbar-badge">
            {len(df):,} Listings Loaded
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# SIDEBAR FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("## 🚗 AutoHive")
    st.caption("Used-Car Market Intelligence")

    st.divider()

    search_query = st.text_input(
        "Search car",
        placeholder="e.g. Swift, Creta, Honda City",
    )

    brands = st.multiselect(
        "Brand",
        sorted(df["brand"].dropna().unique()),
        default=sorted(df["brand"].dropna().unique()),
    )

    locations = st.multiselect(
        "Location",
        sorted(df["location"].dropna().unique()),
        default=sorted(df["location"].dropna().unique()),
    )

    fuel_types = st.multiselect(
        "Fuel Type",
        sorted(df["fuel_type"].dropna().unique()),
        default=sorted(df["fuel_type"].dropna().unique()),
    )

    transmissions = st.multiselect(
        "Transmission",
        sorted(df["transmission"].dropna().unique()),
        default=sorted(df["transmission"].dropna().unique()),
    )

    min_price = int(df["price"].min())
    max_price = int(df["price"].max())

    price_range = st.slider(
        "Price Range",
        min_price,
        max_price,
        (min_price, max_price),
        step=10000,
    )

    has_year = df["year"].notna().any()

    if has_year:
        min_year = int(df["year"].min())
        max_year = int(df["year"].max())

        year_range = st.slider(
            "Manufacturing Year",
            min_year,
            max_year,
            (min_year, max_year),
        )
    else:
        year_range = None

    st.divider()

    st.metric("Total Records", f"{len(df):,}")
    st.metric("Brands", df["brand"].nunique())
    st.metric("Cities", df["location"].nunique())


# =============================================================================
# APPLY FILTERS
# =============================================================================
filtered_df = df[
    df["brand"].isin(brands)
    & df["location"].isin(locations)
    & df["fuel_type"].isin(fuel_types)
    & df["transmission"].isin(transmissions)
    & df["price"].between(price_range[0], price_range[1])
].copy()

if year_range is not None:
    filtered_df = filtered_df[
        filtered_df["year"].between(year_range[0], year_range[1])
    ]

if search_query:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search_query, case=False, na=False)
    ]

if filtered_df.empty:
    st.error("No listings match your filters. Try changing brand, price, year, or location filters.")
    st.stop()


# =============================================================================
# HEADER
# =============================================================================
st.markdown(
    f"""
    <div class="main-header">
        <div class="main-title">🚗 AutoHive Dashboard</div>
        <div class="main-subtitle">
            Professional Used-Car Market Intelligence Dashboard · Showing 
            <b>{len(filtered_df):,}</b> of <b>{len(df):,}</b> listings
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# KPI CARDS
# =============================================================================
total_cars = len(filtered_df)
avg_price = filtered_df["price"].mean()
median_price = filtered_df["price"].median()
avg_km = filtered_df["km_driven"].mean()
top_brand = filtered_df["brand"].value_counts().idxmax()
top_city = filtered_df["location"].value_counts().idxmax()

k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    (k1, "Total Listings", f"{total_cars:,}"),
    (k2, "Average Price", f"₹{avg_price:,.0f}"),
    (k3, "Median Price", f"₹{median_price:,.0f}"),
    (k4, "Avg KM Driven", f"{avg_km:,.0f} km"),
    (k5, "Top Brand", top_brand),
]

for col, label, value in kpis:
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Overview",
        "🏷️ Brand Analytics",
        "💡 Market Insights",
        "📋 Listings & Export",
    ]
)


# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================
with tab1:
    st.markdown('<div class="section-title">Market Snapshot</div>', unsafe_allow_html=True)

    cheapest_car = filtered_df.sort_values("price").iloc[0]
    expensive_car = filtered_df.sort_values("price", ascending=False).iloc[0]
    best_deal = filtered_df.sort_values("deal_score").iloc[0]

    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">Most Affordable</div>
                <div class="insight-value">{cheapest_car["name"]}</div>
                <p>₹{cheapest_car["price"]:,.0f} · {cheapest_car["location"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">Premium Listing</div>
                <div class="insight-value">{expensive_car["name"]}</div>
                <p>₹{expensive_car["price"]:,.0f} · {expensive_car["location"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">Best Relative Deal</div>
                <div class="insight-value">{best_deal["name"]}</div>
                <p>₹{best_deal["price"]:,.0f} · {best_deal["brand"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Equal 2 x 2 chart layout
    row1_col1, row1_col2 = st.columns(2, gap="medium")
    row2_col1, row2_col2 = st.columns(2, gap="medium")

    # -------------------------------------------------------------------------
    # CHART 1: PRICE DISTRIBUTION BY BUDGET RANGE
    # -------------------------------------------------------------------------
    with row1_col1:
        price_df = filtered_df.copy()
        price_df["price_lakh"] = price_df["price"] / 100000

        avg_price_lakh = price_df["price_lakh"].mean()
        median_price_lakh = price_df["price_lakh"].median()

        bins = [0, 2, 5, 8, 10, 15, 20, 30, 50, 100]
        labels = [
            "0-2L",
            "2-5L",
            "5-8L",
            "8-10L",
            "10-15L",
            "15-20L",
            "20-30L",
            "30-50L",
            "50L+",
        ]

        price_df["budget_range"] = pd.cut(
            price_df["price_lakh"],
            bins=bins,
            labels=labels,
            include_lowest=True,
        )

        budget_counts = (
            price_df["budget_range"]
            .value_counts()
            .reindex(labels)
            .reset_index()
        )

        budget_counts.columns = ["Budget Range", "Number of Listings"]

        fig = px.bar(
            budget_counts,
            x="Budget Range",
            y="Number of Listings",
            text="Number of Listings",
            template=T["template"],
            color="Number of Listings",
            color_continuous_scale=[
                [0, "#312E81"],
                [0.5, T["accent"]],
                [1, T["accent2"]],
            ],
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=1,
            marker_line_color="rgba(255,255,255,0.25)",
            hovertemplate=(
                "<b>Budget Range:</b> %{x}<br>"
                "<b>Listings:</b> %{y}<extra></extra>"
            ),
        )

        fig = apply_common_layout(fig, "Price Distribution by Budget Range")

        fig.update_layout(
            coloraxis_showscale=False,
            bargap=0.25,
            annotations=[
                dict(
                    text=f"Avg: {format_price_lakh(avg_price_lakh)}",
                    xref="paper",
                    yref="paper",
                    x=0.72,
                    y=1.08,
                    showarrow=False,
                    font=dict(size=11, color=T["warning"]),
                    bgcolor="rgba(245,158,11,0.12)",
                    bordercolor=T["warning"],
                    borderwidth=1,
                    borderpad=4,
                ),
                dict(
                    text=f"Median: {format_price_lakh(median_price_lakh)}",
                    xref="paper",
                    yref="paper",
                    x=0.91,
                    y=1.08,
                    showarrow=False,
                    font=dict(size=11, color=T["success"]),
                    bgcolor="rgba(16,185,129,0.12)",
                    bordercolor=T["success"],
                    borderwidth=1,
                    borderpad=4,
                ),
            ],
        )

        fig.update_xaxes(
            title_text="Budget Range",
            showgrid=False,
            tickfont=dict(size=11),
        )

        fig.update_yaxes(
            title_text="Number of Listings",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
            rangemode="tozero",
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------------
    # CHART 2: AVERAGE PRICE BY MANUFACTURING YEAR
    # -------------------------------------------------------------------------
    with row1_col2:
        if has_year:
            year_data = (
                filtered_df.dropna(subset=["year"])
                .groupby("year")["price"]
                .mean()
                .reset_index()
                .sort_values("year")
            )

            fig = px.line(
                year_data,
                x="year",
                y="price",
                markers=True,
                template=T["template"],
            )

            fig.update_traces(
                line_width=3,
                marker_size=7,
                line_color=T["accent"],
            )

            fig = apply_common_layout(fig, "Average Price by Manufacturing Year")

            fig.update_xaxes(
                title_text="Year",
                showgrid=False,
            )

            fig.update_yaxes(
                title_text="Average Price (₹)",
                showgrid=True,
                gridcolor="rgba(128,128,128,0.18)",
                tickformat=".2s",
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Year data is not available.")

    # -------------------------------------------------------------------------
    # CHART 3: PRICE VS KILOMETERS DRIVEN
    # -------------------------------------------------------------------------
    with row2_col1:
        fig = px.scatter(
            filtered_df,
            x="km_driven",
            y="price",
            color="fuel_type",
            hover_data=["name", "brand", "location", "transmission"],
            template=T["template"],
        )

        fig.update_traces(
            marker=dict(
                size=8,
                opacity=0.75,
                line=dict(width=0.5, color="rgba(255,255,255,0.3)"),
            )
        )

        fig = apply_common_layout(fig, "Price vs Kilometers Driven")

        fig.update_xaxes(
            title_text="Kilometers Driven",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
            tickformat=".2s",
        )

        fig.update_yaxes(
            title_text="Price (₹)",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
            tickformat=".2s",
        )

        fig.update_layout(
            legend_title_text="Fuel Type",
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="right",
                x=1.02,
            ),
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------------
    # CHART 4: FUEL TYPE DISTRIBUTION
    # -------------------------------------------------------------------------
    with row2_col2:
        fuel_data = filtered_df["fuel_type"].value_counts().reset_index()
        fuel_data.columns = ["fuel_type", "count"]

        fig = px.pie(
            fuel_data,
            names="fuel_type",
            values="count",
            hole=0.48,
            template=T["template"],
            color_discrete_sequence=[
                T["accent"],
                "#EF553B",
                "#00CC96",
                "#AB63FA",
                "#FFA15A",
            ],
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Listings: %{value}<br>Share: %{percent}<extra></extra>",
            marker=dict(line=dict(color="rgba(255,255,255,0.2)", width=1)),
        )

        fig = apply_common_layout(fig, "Fuel Type Distribution")

        fig.update_layout(
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="right",
                x=1.05,
            )
        )

        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# TAB 2: BRAND ANALYTICS
# =============================================================================
with tab2:
    st.markdown('<div class="section-title">Brand Performance</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2, gap="medium")

    with b1:
        brand_price = (
            filtered_df.groupby("brand")["price"]
            .mean()
            .reset_index()
            .sort_values("price", ascending=False)
            .head(15)
        )

        fig = px.bar(
            brand_price,
            x="brand",
            y="price",
            template=T["template"],
            color_discrete_sequence=[T["accent"]],
        )

        fig = apply_common_layout(fig, "Average Price by Brand")

        fig.update_xaxes(
            title_text="Brand",
            tickangle=-35,
            showgrid=False,
        )

        fig.update_yaxes(
            title_text="Average Price (₹)",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
            tickformat=".2s",
        )

        st.plotly_chart(fig, use_container_width=True)

    with b2:
        brand_count = filtered_df["brand"].value_counts().head(15).reset_index()
        brand_count.columns = ["brand", "count"]

        fig = px.bar(
            brand_count,
            x="brand",
            y="count",
            template=T["template"],
            color_discrete_sequence=[T["accent"]],
        )

        fig = apply_common_layout(fig, "Listing Count by Brand")

        fig.update_xaxes(
            title_text="Brand",
            tickangle=-35,
            showgrid=False,
        )

        fig.update_yaxes(
            title_text="Number of Listings",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
        )

        st.plotly_chart(fig, use_container_width=True)

    top_brands = filtered_df["brand"].value_counts().head(10).index
    box_df = filtered_df[filtered_df["brand"].isin(top_brands)]

    fig = px.box(
        box_df,
        x="brand",
        y="price",
        color="brand",
        title="Price Spread of Top 10 Brands",
        template=T["template"],
    )

    fig.update_layout(
        xaxis_title="Brand",
        yaxis_title="Price (₹)",
        showlegend=False,
        height=480,
        margin=dict(l=45, r=35, t=75, b=50),
    )

    fig.update_yaxes(tickformat=".2s")

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# TAB 3: MARKET INSIGHTS
# =============================================================================
with tab3:
    st.markdown('<div class="section-title">Location Intelligence</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2, gap="medium")

    with m1:
        city_price = (
            filtered_df.groupby("location")["price"]
            .mean()
            .reset_index()
            .sort_values("price", ascending=False)
            .head(12)
        )

        fig = px.bar(
            city_price,
            x="location",
            y="price",
            template=T["template"],
            color_discrete_sequence=[T["accent"]],
        )

        fig = apply_common_layout(fig, "Average Price by City")

        fig.update_xaxes(
            title_text="City",
            tickangle=-35,
            showgrid=False,
        )

        fig.update_yaxes(
            title_text="Average Price (₹)",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
            tickformat=".2s",
        )

        st.plotly_chart(fig, use_container_width=True)

    with m2:
        city_count = filtered_df["location"].value_counts().head(12).reset_index()
        city_count.columns = ["location", "count"]

        fig = px.pie(
            city_count,
            names="location",
            values="count",
            hole=0.48,
            template=T["template"],
        )

        fig = apply_common_layout(fig, "Listings Share by City")

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Transmission and Fuel Insights</div>', unsafe_allow_html=True)

    i1, i2 = st.columns(2, gap="medium")

    with i1:
        transmission_data = filtered_df["transmission"].value_counts().reset_index()
        transmission_data.columns = ["transmission", "count"]

        fig = px.bar(
            transmission_data,
            x="transmission",
            y="count",
            template=T["template"],
            color_discrete_sequence=[T["accent"]],
        )

        fig = apply_common_layout(fig, "Transmission Type Distribution", height=400)

        fig.update_xaxes(
            title_text="Transmission",
            showgrid=False,
        )

        fig.update_yaxes(
            title_text="Listings",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
        )

        st.plotly_chart(fig, use_container_width=True)

    with i2:
        fuel_price = (
            filtered_df.groupby("fuel_type")["price"]
            .mean()
            .reset_index()
            .sort_values("price", ascending=False)
        )

        fig = px.bar(
            fuel_price,
            x="fuel_type",
            y="price",
            template=T["template"],
            color_discrete_sequence=[T["accent"]],
        )

        fig = apply_common_layout(fig, "Average Price by Fuel Type", height=400)

        fig.update_xaxes(
            title_text="Fuel Type",
            showgrid=False,
        )

        fig.update_yaxes(
            title_text="Average Price (₹)",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.18)",
            tickformat=".2s",
        )

        st.plotly_chart(fig, use_container_width=True)

    if has_year:
        st.markdown('<div class="section-title">Depreciation Trend</div>', unsafe_allow_html=True)

        top_6_brands = filtered_df["brand"].value_counts().head(6).index

        depreciation_df = (
            filtered_df[filtered_df["brand"].isin(top_6_brands)]
            .dropna(subset=["year"])
            .groupby(["brand", "year"])["price"]
            .mean()
            .reset_index()
            .sort_values("year")
        )

        fig = px.line(
            depreciation_df,
            x="year",
            y="price",
            color="brand",
            markers=True,
            template=T["template"],
        )

        fig.update_traces(line_width=3, marker_size=7)

        fig = apply_common_layout(fig, "Average Price by Year for Top Brands", height=480)

        fig.update_xaxes(title_text="Manufacturing Year")
        fig.update_yaxes(title_text="Average Price (₹)", tickformat=".2s")

        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# TAB 4: LISTINGS AND EXPORT
# =============================================================================
with tab4:
    st.markdown('<div class="section-title">Top 10 Affordable Listings</div>', unsafe_allow_html=True)

    display_cols = [
        "name",
        "brand",
        "year",
        "price",
        "km_driven",
        "fuel_type",
        "transmission",
        "location",
        "url",
    ]

    available_cols = [col for col in display_cols if col in filtered_df.columns]

    cheapest_10 = filtered_df.sort_values("price").head(10)

    st.dataframe(
        cheapest_10[available_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "price": st.column_config.NumberColumn("Price", format="₹%d"),
            "km_driven": st.column_config.NumberColumn("KM Driven", format="%d km"),
            "url": st.column_config.LinkColumn("Listing URL"),
        },
    )

    st.markdown('<div class="section-title">Best Relative Deals</div>', unsafe_allow_html=True)

    best_deals = filtered_df.sort_values("deal_score").head(10)

    st.dataframe(
        best_deals[available_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "price": st.column_config.NumberColumn("Price", format="₹%d"),
            "km_driven": st.column_config.NumberColumn("KM Driven", format="%d km"),
            "url": st.column_config.LinkColumn("Listing URL"),
        },
    )

    st.markdown('<div class="section-title">All Filtered Listings</div>', unsafe_allow_html=True)

    st.dataframe(
        filtered_df[available_cols].sort_values("price"),
        use_container_width=True,
        hide_index=True,
        height=520,
        column_config={
            "price": st.column_config.NumberColumn("Price", format="₹%d"),
            "km_driven": st.column_config.NumberColumn("KM Driven", format="%d km"),
            "url": st.column_config.LinkColumn("Listing URL"),
        },
    )

    csv = (
        filtered_df.drop(columns=["deal_score"], errors="ignore")
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="autohive_filtered_listings.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =============================================================================
# FOOTER
# =============================================================================
st.markdown(
    """
    <div class="footer">
        🚗 <b>AutoHive</b> · Used-Car Market Intelligence · Built with Streamlit, SQLite, Pandas and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)