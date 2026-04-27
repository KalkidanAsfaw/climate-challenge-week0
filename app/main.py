import sys
import os

# ensure project root is on the path so `import utils` resolves
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import (
    load_all_data,
    filter_data,
    get_monthly_avg,
    get_summary_stats,
    get_extreme_heat_counts,
    COUNTRIES,
    COUNTRY_COLORS,
    VARIABLES,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="EthioClimate — COP32 Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------
@st.cache_data
def get_data():
    return load_all_data()


df_all = get_data()

if df_all.empty:
    st.error(
        "No cleaned CSV files found in the `data/` directory.  "
        "Place `ethiopia_clean.csv`, `kenya_clean.csv`, `nigeria_clean.csv`, "
        "`sudan_clean.csv`, and `tanzania_clean.csv` there, then refresh."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar — controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🌍 Dashboard Controls")
    st.markdown("---")

    selected_countries = st.multiselect(
        "Countries",
        options=COUNTRIES,
        default=COUNTRIES,
        help="Select one or more countries to display.",
    )

    year_min = int(df_all["YEAR"].min())
    year_max = int(df_all["YEAR"].max())
    year_range = st.slider(
        "Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        help="Drag the handles to zoom into a specific period.",
    )

    selected_variable = st.selectbox(
        "Variable",
        options=list(VARIABLES.keys()),
        format_func=lambda k: VARIABLES[k],
        index=0,
        help="Controls the Trend and Distribution charts.",
    )

    st.markdown("---")
    st.caption("Data: NASA POWER | 2015 – 2026")
    st.caption("EthioClimate Analytics · COP32 Addis Ababa 2027")

if not selected_countries:
    st.warning("Please select at least one country from the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# Filter
# ---------------------------------------------------------------------------
df = filter_data(df_all, selected_countries, year_range)

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🌍 African Climate Dashboard — COP32 Insights")
st.caption(
    f"**{', '.join(selected_countries)}** · "
    f"**{year_range[0]}–{year_range[1]}** · "
    f"Variable: **{VARIABLES[selected_variable]}**"
)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Countries", len(selected_countries))
k2.metric("Daily Records", f"{len(df):,}")
k3.metric(
    f"Mean {selected_variable}",
    f"{df[selected_variable].mean():.2f}",
)
k4.metric("Max T2M_MAX on record", f"{df['T2M_MAX'].max():.1f} °C")

st.divider()

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["📈  Trend Analysis", "📦  Distribution", "📊  Summary Statistics"]
)

# ── Tab 1: Trend ────────────────────────────────────────────────────────────
with tab1:
    st.subheader(f"Monthly Average {VARIABLES[selected_variable]}")

    monthly = get_monthly_avg(df, selected_variable)

    fig_trend = go.Figure()
    for country in selected_countries:
        sub = monthly[monthly["Country"] == country].sort_values("Date")
        fig_trend.add_trace(
            go.Scatter(
                x=sub["Date"],
                y=sub[selected_variable],
                name=country,
                line=dict(color=COUNTRY_COLORS[country], width=2),
                mode="lines",
                hovertemplate=f"<b>{country}</b><br>%{{x|%b %Y}}<br>"
                              f"{VARIABLES[selected_variable]}: %{{y:.2f}}<extra></extra>",
            )
        )
    fig_trend.update_layout(
        xaxis_title="Date",
        yaxis_title=VARIABLES[selected_variable],
        legend_title="Country",
        hovermode="x unified",
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ── Tab 2: Distribution ──────────────────────────────────────────────────────
with tab2:
    st.subheader(f"Distribution of {VARIABLES[selected_variable]}")

    cap_pct = 0.99
    cap_val = df[selected_variable].quantile(cap_pct)
    df_plot = df.copy()
    df_plot[selected_variable] = df_plot[selected_variable].clip(upper=cap_val)

    fig_box = px.box(
        df_plot,
        x="Country",
        y=selected_variable,
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        category_orders={"Country": selected_countries},
        labels={selected_variable: VARIABLES[selected_variable]},
        height=450,
    )
    fig_box.update_layout(
        showlegend=False,
        xaxis_title="Country",
        yaxis_title=VARIABLES[selected_variable],
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_box, use_container_width=True)
    st.caption(f"Values capped at 99th percentile ({cap_val:.2f}) for readability.")

# ── Tab 3: Summary Statistics ───────────────────────────────────────────────
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(f"{VARIABLES[selected_variable]} — Summary")
        stats = get_summary_stats(df, selected_variable)
        st.dataframe(stats.style.format("{:.3f}"), use_container_width=True)

    with col_b:
        st.subheader("Precipitation (PRECTOTCORR) — Summary")
        precip_stats = get_summary_stats(df, "PRECTOTCORR")
        st.dataframe(precip_stats.style.format("{:.3f}"), use_container_width=True)

    st.markdown("---")
    st.subheader("Extreme Heat — Avg Days per Year with T2M_MAX > 35 °C")
    heat = get_extreme_heat_counts(df)
    heat = heat[heat["Country"].isin(selected_countries)]

    fig_heat = px.bar(
        heat.sort_values("heat_days", ascending=False),
        x="Country",
        y="heat_days",
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        text="heat_days",
        labels={"heat_days": "Days / Year"},
        height=350,
    )
    fig_heat.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig_heat.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_heat, use_container_width=True)
