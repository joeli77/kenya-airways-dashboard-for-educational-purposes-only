import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Kenya Airways PLC – Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# KENYA AIRWAYS COLOR SYSTEM
# =====================================================

KA_RED = "#C8102E"
KA_DARK = "#2F2F2F"
KA_GOLD = "#C8A96A"
KA_LIGHT = "#F7F7F5"
KA_BORDER = "#E5E5E5"
KA_GRAY = "#6B7280"
KA_GREEN = "#15803D"

# =====================================================
# DASHBOARD STYLING
# =====================================================

st.markdown(
f"""
<style>

.main {{
    background-color:white;
}}

.block-container {{
    max-width:1400px;
    padding-top:1.2rem;
}}

h1,h2,h3 {{
    color:{KA_DARK};
}}

.meta {{
    color:{KA_GRAY};
    font-size:0.9rem;
}}

.banner {{
    background:linear-gradient(90deg,{KA_RED},{KA_DARK});
    color:white;
    padding:1rem;
    border-radius:12px;
}}

.chip {{
    display:inline-block;
    padding:3px 10px;
    border-radius:20px;
    background:{KA_LIGHT};
    border:1px solid {KA_BORDER};
    font-size:0.75rem;
}}

.callout {{
    border-left:5px solid {KA_RED};
    background:#FAFAFA;
    padding:0.8rem 1rem;
    border-radius:10px;
}}

.wsbox {{
    border:1px solid {KA_BORDER};
    padding:0.7rem 1rem;
    border-radius:10px;
}}

</style>
""",
unsafe_allow_html=True
)

# =====================================================
# DATA — VERIFIED ACTUALS MODE
# =====================================================

@st.cache_data
def load_financial_data():

    data = [

        {
        "period":"FY2023",
        "type":"FY",
        "revenue":177.0,
        "operating_profit":10.5,
        "pbt":-22.5,
        "pat":-22.7,
        "operating_cashflow":9.2,
        "assets":185.7,
        "liabilities":329.0,
        "equity":-143.3
        },

        {
        "period":"FY2024",
        "type":"FY",
        "revenue":188.5,
        "operating_profit":16.6,
        "pbt":5.5,
        "pat":5.4,
        "operating_cashflow":17.7,
        "assets":179.1,
        "liabilities":297.4,
        "equity":-118.3
        },

        {
        "period":"HY2024",
        "type":"HY",
        "revenue":91.0,
        "operating_profit":1.3,
        "pbt":5.4,
        "pat":None,
        "operating_cashflow":None,
        "assets":None,
        "liabilities":None,
        "equity":None
        },

        {
        "period":"HY2025",
        "type":"HY",
        "revenue":75.0,
        "operating_profit":-6.2,
        "pbt":-12.2,
        "pat":None,
        "operating_cashflow":None,
        "assets":None,
        "liabilities":None,
        "equity":None
        }

    ]

    df = pd.DataFrame(data)

    df["operating_margin"] = df["operating_profit"] / df["revenue"] * 100
    df["pbt_margin"] = df["pbt"] / df["revenue"] * 100
    df["net_margin"] = df["pat"] / df["revenue"] * 100

    return df


@st.cache_data
def load_operating_data():

    data = [

        {
        "period":"FY2023",
        "passengers":5.00,
        "capacity_ask":14.75,
        "cabin_factor":73.5
        },

        {
        "period":"FY2024",
        "passengers":5.23,
        "capacity_ask":16.23,
        "cabin_factor":75.2
        },

        {
        "period":"HY2024",
        "passengers":2.90,
        "capacity_ask":7.99,
        "cabin_factor":None
        },

        {
        "period":"HY2025",
        "passengers":2.50,
        "capacity_ask":6.71,
        "cabin_factor":None
        }

    ]

    return pd.DataFrame(data)

financial_df = load_financial_data()
operating_df = load_operating_data()

# =====================================================
# FORMAT HELPERS
# =====================================================

def fmt_bn(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"KSh {x:,.1f}bn"

def fmt_pct(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{x:,.1f}%"

def fmt_m(x):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{x:,.2f}M"

def yoy_delta(current, prior):
    if current is None or prior is None or pd.isna(current) or pd.isna(prior):
        return None
    return current - prior

def yoy_pct(current, prior):
    if current is None or prior is None or pd.isna(current) or pd.isna(prior) or prior == 0:
        return None
    return (current - prior) / abs(prior) * 100

def delta_text(current, prior, suffix="", pp=False):
    if current is None or prior is None or pd.isna(current) or pd.isna(prior):
        return "N/A"
    diff = current - prior
    sign = "+" if diff >= 0 else ""
    if pp:
        return f"{sign}{diff:.1f}pp"
    if suffix:
        return f"{sign}{diff:.1f}{suffix}"
    return f"{sign}{diff:.1f}"

def pct_change_text(current, prior):
    val = yoy_pct(current, prior)
    if val is None or pd.isna(val):
        return "N/A"
    sign = "+" if val >= 0 else ""
    return f"{sign}{val:.1f}%"

# =====================================================
# SOURCE REGISTER
# =====================================================

source_register = pd.DataFrame([
    {
        "Source": "FY2024 Annual Report",
        "Period": "FY2024",
        "Role": "Primary official source",
        "Status": "Base reporting layer"
    },
    {
        "Source": "FY2024 Signed Financials",
        "Period": "FY2024",
        "Role": "Primary official source",
        "Status": "Base reporting layer"
    },
    {
        "Source": "FY2024 Full Year Financial Results",
        "Period": "FY2024",
        "Role": "Primary official source",
        "Status": "Base reporting layer"
    },
    {
        "Source": "FY2024 Investor Briefing",
        "Period": "FY2024",
        "Role": "Primary official source",
        "Status": "Base reporting layer"
    },
    {
        "Source": "HY2025 Interim Reporting / Briefing",
        "Period": "HY2025",
        "Role": "Primary official source",
        "Status": "Latest update layer"
    },
    {
        "Source": "HY2025 Press Coverage",
        "Period": "HY2025",
        "Role": "Secondary context only",
        "Status": "Used only if needed"
    }
])

# =====================================================
# SIDEBAR CONTROLS
# =====================================================

st.sidebar.markdown("## Dashboard Controls")

selected_period = st.sidebar.selectbox(
    "Selected period",
    ["FY2024", "FY2023", "HY2025", "HY2024"],
    index=0
)

compare_mode = st.sidebar.selectbox(
    "Compare against",
    ["Prior comparable period", "None"],
    index=0
)

show_sources = st.sidebar.toggle("Show source emphasis", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Trust & Scope")
st.sidebar.markdown("- **Truth Mode:** Verified Actuals Only")
st.sidebar.markdown("- **Base Layer:** FY2024 audited/reported")
st.sidebar.markdown("- **Update Layer:** HY2025 interim")
st.sidebar.markdown("- **Forecasts:** Not included")
st.sidebar.markdown("- **Synthetic data:** Not used")

# =====================================================
# PERIOD SELECTION LOGIC
# =====================================================

selected_row = financial_df[financial_df["period"] == selected_period].iloc[0]

prior_map = {
    "FY2024": "FY2023",
    "HY2025": "HY2024",
    "FY2023": None,
    "HY2024": None
}

compare_period = prior_map.get(selected_period) if compare_mode == "Prior comparable period" else None
compare_row = None
if compare_period is not None:
    compare_df = financial_df[financial_df["period"] == compare_period]
    if not compare_df.empty:
        compare_row = compare_df.iloc[0]

selected_ops = operating_df[operating_df["period"] == selected_period]
selected_ops = selected_ops.iloc[0] if not selected_ops.empty else None

compare_ops = None
if compare_period is not None:
    compare_ops_df = operating_df[operating_df["period"] == compare_period]
    if not compare_ops_df.empty:
        compare_ops = compare_ops_df.iloc[0]

# =====================================================
# HEADER
# =====================================================

st.markdown(
    f"""
    <div class="banner">
        <div style="font-size:1.55rem;font-weight:700;">
            Kenya Airways PLC – Executive Financial Dashboard
        </div>
        <div class="banner-sub">
            Verified Actuals Mode | FY2024 audited base with HY2025 interim update layer | Educational / analytical use
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

meta_parts = [
    f"Selected Period: {selected_period}",
    f"Comparison: {compare_period if compare_period else 'None'}",
    "Reporting Scope: Group reported results only",
    "Forecast Inclusion: None",
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}"
]
st.markdown(
    f"<div class='meta'>{' &nbsp;&nbsp;|&nbsp;&nbsp; '.join(meta_parts)}</div>",
    unsafe_allow_html=True
)

if show_sources:
    st.markdown(
        """
        <span class="chip">Source hierarchy active</span>
        <span class="chip">FY2024 audited base</span>
        <span class="chip">HY2025 interim separated</span>
        <span class="chip">No invented forecasts</span>
        """,
        unsafe_allow_html=True
    )

st.markdown("")

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Overview",
    "Profitability & Revenue",
    "Operating Drivers",
    "Financial Position & Liquidity",
    "Latest Update: HY2025",
    "Sources, Notes & Limitations"
])

# =====================================================
# TAB 1 — EXECUTIVE OVERVIEW
# =====================================================

with tab1:
    st.subheader("Executive Overview")
    st.caption("Purpose: give leadership the full story in under a minute.")

    # Executive headline
    if selected_period == "FY2024":
        headline = "FY2024 marked a return to profitability, with revenue growth, higher traffic, and stronger operating earnings versus FY2023."
    elif selected_period == "HY2025":
        headline = "HY2025 interim results show a weaker trading period, with lower revenue, lower traffic, and an operating loss versus HY2024."
    elif selected_period == "FY2023":
        headline = "FY2023 provides the comparative base period, showing lower traffic and a loss position ahead of the FY2024 turnaround."
    else:
        headline = "HY2024 provides the prior interim comparison point used to assess the HY2025 update layer."

    st.markdown(
        f"""
        <div class="callout">
            <div style="font-weight:700; margin-bottom:0.25rem;">Executive headline</div>
            {headline}
        </div>
        """,
        unsafe_allow_html=True
    )

    # What changed strip
    if selected_period == "FY2024":
        changes = [
            "Turnover +6.0%",
            "Operating profit +58.1%",
            "PBT moved from loss to profit",
            "Passengers +4.6%",
            "Capacity / ASK +10.0%",
            "Cabin factor 75.2%"
        ]
    elif selected_period == "HY2025":
        changes = [
            "Revenue -17.6%",
            "Operating result weakened vs HY2024",
            "PBT moved from profit to loss",
            "Passengers -13.8%",
            "Capacity / ASK -16.0%",
            "Fleet availability pressure reported"
        ]
    else:
        changes = [
            "Selected period is shown as a comparison base",
            "Use compare toggle for direct period review"
        ]

    st.markdown(
        "<div class='what-changed'><b>What changed this period?</b><br>" +
        " • ".join(changes) +
        "</div>",
        unsafe_allow_html=True
    )

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)
    c5, c6, c7, c8 = st.columns(4)

    revenue_prior = compare_row["revenue"] if compare_row is not None else None
    op_prior = compare_row["operating_profit"] if compare_row is not None else None
    pbt_prior = compare_row["pbt"] if compare_row is not None else None
    pat_prior = compare_row["pat"] if compare_row is not None else None
    ocf_prior = compare_row["operating_cashflow"] if compare_row is not None else None
    cash_prior = compare_row["cash_end_ksh_bn"] if compare_row is not None and "cash_end_ksh_bn" in compare_row else None

    passengers_current = selected_ops["passengers"] if selected_ops is not None else None
    passengers_prior = compare_ops["passengers"] if compare_ops is not None else None
    cabin_current = selected_ops["cabin_factor"] if selected_ops is not None else None
    cabin_prior = compare_ops["cabin_factor"] if compare_ops is not None else None

    c1.metric("Revenue", fmt_bn(selected_row["revenue"]), pct_change_text(selected_row["revenue"], revenue_prior))
    c2.metric("Operating Profit", fmt_bn(selected_row["operating_profit"]), pct_change_text(selected_row["operating_profit"], op_prior))
    c3.metric("Profit Before Tax", fmt_bn(selected_row["pbt"]), pct_change_text(selected_row["pbt"], pbt_prior))
    c4.metric("Profit After Tax", fmt_bn(selected_row["pat"]), pct_change_text(selected_row["pat"], pat_prior))

    c5.metric("Passengers", fmt_m(passengers_current), pct_change_text(passengers_current, passengers_prior))
    c6.metric("Cabin Factor", fmt_pct(cabin_current), delta_text(cabin_current, cabin_prior, pp=True))
    c7.metric("Operating Cash Flow", fmt_bn(selected_row["operating_cashflow"]), pct_change_text(selected_row["operating_cashflow"], ocf_prior))
    c8.metric("Year-end Cash", fmt_bn(selected_row["cash_end_ksh_bn"]), pct_change_text(selected_row["cash_end_ksh_bn"], cash_prior))

    if show_sources:
        st.markdown(
            """
            <span class="chip">Source: FY2024 full-year results / interim release</span>
            <span class="chip">KPI layer: reported figures only</span>
            <span class="chip">Comparatives: prior comparable period where available</span>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    # Main trend chart
    overview_df = financial_df[financial_df["period"].isin(["FY2023", "FY2024"])].copy()
    fig_overview = go.Figure()
    fig_overview.add_trace(go.Bar(
        x=overview_df["period"],
        y=overview_df["revenue"],
        name="Revenue",
        marker_color=[KA_GRAY if p != selected_period else KA_DARK for p in overview_df["period"]]
    ))
    fig_overview.add_trace(go.Bar(
        x=overview_df["period"],
        y=overview_df["operating_profit"],
        name="Operating Profit",
        marker_color=[KA_BORDER if p != selected_period else KA_RED for p in overview_df["period"]]
    ))
    fig_overview.update_layout(
        barmode="group",
        title="Scale and operating profitability — FY2023 vs FY2024",
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="",
        margin=dict(l=20, r=20, t=60, b=20),
        height=430
    )
    fig_overview.update_yaxes(title="KSh bn", gridcolor="#EEEEEE")
    st.plotly_chart(fig_overview, use_container_width=True)

    st.markdown(
        """
        <div class="section-note">
            Chart conclusion: FY2024 shows modest top-line growth with a much larger improvement in operating earnings, supporting a clearer turnaround narrative than revenue alone would suggest.
        </div>
        """,
        unsafe_allow_html=True
    )

    # What / So what / Now what
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            f"""
            <div class="wsbox">
                <div class="small-label">What happened?</div>
                <div style="margin-top:0.35rem;">
                    Revenue was {fmt_bn(selected_row["revenue"])}, operating profit was {fmt_bn(selected_row["operating_profit"])}, and reported PBT was {fmt_bn(selected_row["pbt"])} for {selected_period}.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            f"""
            <div class="wsbox">
                <div class="small-label">So what?</div>
                <div style="margin-top:0.35rem;">
                    The selected period should be interpreted through both commercial scale and earnings quality. For FY2024, the improvement was broader than traffic alone; for HY2025, the interim picture weakened materially.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_c:
        st.markdown(
            f"""
            <div class="wsbox">
                <div class="small-label">Now what?</div>
                <div style="margin-top:0.35rem;">
                    Monitor whether the next reported period sustains operating performance, liquidity discipline, and traffic recovery without blurring the distinction between audited annual results and interim updates.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="trust-box">
            <b>Trust / provenance note:</b> This dashboard uses reported Kenya Airways figures only. FY2024 is treated as the audited / reported annual base layer, while HY2025 is shown separately as an interim update layer.
        </div>
        """,
        unsafe_allow_html=True
    )
# =====================================================
# TAB 2 — PROFITABILITY & REVENUE
# =====================================================

with tab2:
    st.subheader("Profitability & Revenue")
    st.caption("Purpose: show the financial turnaround and where it came from.")

    st.markdown(
        """
        <div class="callout">
            <div style="font-weight:700; margin-bottom:0.25rem;">Executive callout</div>
            FY2024’s reported earnings improvement was materially larger than top-line growth alone, so this section separates scale, operating performance, and below-operating-line outcome.
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4, m5, m6 = st.columns(6)

    rev_prior = compare_row["revenue"] if compare_row is not None else None
    op_prior = compare_row["operating_profit"] if compare_row is not None else None
    pbt_prior = compare_row["pbt"] if compare_row is not None else None
    pat_prior = compare_row["pat"] if compare_row is not None else None
    op_margin_prior = compare_row["operating_margin"] if compare_row is not None else None
    pbt_margin_prior = compare_row["pbt_margin"] if compare_row is not None else None

    m1.metric("Revenue", fmt_bn(selected_row["revenue"]), pct_change_text(selected_row["revenue"], rev_prior))
    m2.metric("Operating Profit", fmt_bn(selected_row["operating_profit"]), pct_change_text(selected_row["operating_profit"], op_prior))
    m3.metric("PBT", fmt_bn(selected_row["pbt"]), pct_change_text(selected_row["pbt"], pbt_prior))
    m4.metric("PAT", fmt_bn(selected_row["pat"]), pct_change_text(selected_row["pat"], pat_prior))
    m5.metric("Operating Margin", fmt_pct(selected_row["operating_margin"]), delta_text(selected_row["operating_margin"], op_margin_prior, pp=True))
    m6.metric("PBT Margin", fmt_pct(selected_row["pbt_margin"]), delta_text(selected_row["pbt_margin"], pbt_margin_prior, pp=True))

    st.markdown(
        """
        <span class="chip">Driver tag: revenue scale</span>
        <span class="chip">Driver tag: operating leverage</span>
        <span class="chip">Driver tag: below-operating-line effect</span>
        """,
        unsafe_allow_html=True
    )

    col_left, col_right = st.columns(2)

    with col_left:
        profit_df = financial_df[financial_df["period"].isin(["FY2023", "FY2024"])].copy()
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            x=profit_df["period"],
            y=profit_df["revenue"],
            name="Revenue",
            marker_color=[KA_GRAY, KA_RED]
        ))
        fig_rev.update_layout(
            title="Turnover trend — FY2023 vs FY2024",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )
        fig_rev.update_yaxes(title="KSh bn", gridcolor="#EEEEEE")
        st.plotly_chart(fig_rev, use_container_width=True)

        st.markdown(
            """
            <div class="section-note">
                Chart conclusion: FY2024 revenue growth was positive but moderate relative to the larger improvement in reported earnings.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        fig_profit = go.Figure()
        fig_profit.add_trace(go.Bar(
            x=profit_df["period"],
            y=profit_df["operating_profit"],
            name="Operating Profit",
            marker_color=KA_RED
        ))
        fig_profit.add_trace(go.Bar(
            x=profit_df["period"],
            y=profit_df["pbt"],
            name="PBT",
            marker_color=KA_DARK
        ))
        fig_profit.add_trace(go.Bar(
            x=profit_df["period"],
            y=profit_df["pat"],
            name="PAT",
            marker_color=KA_GOLD
        ))
        fig_profit.update_layout(
            title="Profitability trend — operating profit, PBT, PAT",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            barmode="group"
        )
        fig_profit.update_yaxes(title="KSh bn", gridcolor="#EEEEEE")
        st.plotly_chart(fig_profit, use_container_width=True)

        st.markdown(
            """
            <div class="section-note">
                Chart conclusion: FY2024 moved from a loss position to reported profitability at pretax and after-tax level, not just at operating level.
            </div>
            """,
            unsafe_allow_html=True
        )

    margin_df = financial_df[financial_df["period"].isin(["FY2023", "FY2024"])][
        ["period", "operating_margin", "pbt_margin", "net_margin"]
    ].copy()

    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(
        x=margin_df["period"],
        y=margin_df["operating_margin"],
        mode="lines+markers+text",
        name="Operating Margin",
        text=[f"{v:.1f}%" if pd.notna(v) else "" for v in margin_df["operating_margin"]],
        textposition="top center",
        line=dict(color=KA_RED, width=3)
    ))
    fig_margin.add_trace(go.Scatter(
        x=margin_df["period"],
        y=margin_df["pbt_margin"],
        mode="lines+markers+text",
        name="PBT Margin",
        text=[f"{v:.1f}%" if pd.notna(v) else "" for v in margin_df["pbt_margin"]],
        textposition="bottom center",
        line=dict(color=KA_DARK, width=3)
    ))
    fig_margin.add_trace(go.Scatter(
        x=margin_df["period"],
        y=margin_df["net_margin"],
        mode="lines+markers+text",
        name="Net Margin",
        text=[f"{v:.1f}%" if pd.notna(v) else "" for v in margin_df["net_margin"]],
        textposition="middle right",
        line=dict(color=KA_GOLD, width=3)
    ))
    fig_margin.update_layout(
        title="Margin comparison — operating, pretax, and net",
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    fig_margin.update_yaxes(title="Margin %", gridcolor="#EEEEEE")
    st.plotly_chart(fig_margin, use_container_width=True)

    wa, sb, nw = st.columns(3)

    with wa:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">What happened?</div>
                <div style="margin-top:0.35rem;">
                    Revenue improved year on year in FY2024, while operating profit, pretax profit, and after-tax profit improved much more sharply.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with sb:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">So what?</div>
                <div style="margin-top:0.35rem;">
                    The financial story is not just one of traffic growth. Margin improvement and below-operating-line movement are both central to understanding the FY2024 result.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with nw:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">Now what?</div>
                <div style="margin-top:0.35rem;">
                    The next leadership watchpoint is whether later reported periods preserve operating margin and pretax quality without depending on the same result mix.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# TAB 3 — OPERATING DRIVERS
# =====================================================

with tab3:
    st.subheader("Operating Drivers")
    st.caption("Purpose: connect financial performance to traffic and operations.")

    st.markdown(
        """
        <div class="callout">
            <div style="font-weight:700; margin-bottom:0.25rem;">Executive callout</div>
            This section isolates the operating base behind the financial result: traffic, capacity, and utilization.
        </div>
        """,
        unsafe_allow_html=True
    )

    op1, op2, op3, op4, op5 = st.columns(5)

    asks_current = selected_ops["capacity_ask"] if selected_ops is not None else None
    asks_prior = compare_ops["capacity_ask"] if compare_ops is not None else None
    passengers_current = selected_ops["passengers"] if selected_ops is not None else None
    passengers_prior = compare_ops["passengers"] if compare_ops is not None else None
    cabin_current = selected_ops["cabin_factor"] if selected_ops is not None else None
    cabin_prior = compare_ops["cabin_factor"] if compare_ops is not None else None

    fy2024_ops = operating_df[operating_df["period"] == "FY2024"]
    cargo_value = None
    if not fy2024_ops.empty:
        cargo_value = 25.0

    op1.metric("Passengers", fmt_m(passengers_current), pct_change_text(passengers_current, passengers_prior))
    op2.metric("Capacity / ASK", f"{asks_current:,.2f}bn" if asks_current is not None and pd.notna(asks_current) else "N/A", pct_change_text(asks_current, asks_prior))
    op3.metric("Cabin Factor", fmt_pct(cabin_current), delta_text(cabin_current, cabin_prior, pp=True))
    op4.metric("Cargo Growth", fmt_pct(cargo_value if selected_period == "FY2024" else None), "Reported for FY2024")
    op5.metric("Yield Note", "At par" if selected_period == "FY2024" else "N/A", "Reported commentary")

    st.markdown(
        """
        <span class="chip">Metric definition: ASK = available seat kilometres</span>
        <span class="chip">Metric definition: cabin factor = passenger load / utilization proxy</span>
        <span class="chip">Metric definition: yield note shown only where explicitly reported</span>
        """,
        unsafe_allow_html=True
    )

    c_left, c_mid, c_right = st.columns(3)

    with c_left:
        pax_df = operating_df[operating_df["period"].isin(["FY2023", "FY2024"])].copy()
        fig_pax = go.Figure()
        fig_pax.add_trace(go.Scatter(
            x=pax_df["period"],
            y=pax_df["passengers"],
            mode="lines+markers+text",
            text=[f"{v:.2f}M" for v in pax_df["passengers"]],
            textposition="top center",
            line=dict(color=KA_RED, width=3),
            name="Passengers"
        ))
        fig_pax.update_layout(
            title="Passenger trend",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=360,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )
        fig_pax.update_yaxes(title="Millions", gridcolor="#EEEEEE")
        st.plotly_chart(fig_pax, use_container_width=True)

    with c_mid:
        ask_df = operating_df[operating_df["period"].isin(["FY2023", "FY2024"])].copy()
        fig_ask = go.Figure()
        fig_ask.add_trace(go.Bar(
            x=ask_df["period"],
            y=ask_df["capacity_ask"],
            marker_color=[KA_GRAY, KA_DARK],
            name="ASK"
        ))
        fig_ask.update_layout(
            title="Capacity / ASK trend",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=360,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )
        fig_ask.update_yaxes(title="bn", gridcolor="#EEEEEE")
        st.plotly_chart(fig_ask, use_container_width=True)

    with c_right:
        cf_df = operating_df[operating_df["period"].isin(["FY2023", "FY2024"])].copy()
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Scatter(
            x=cf_df["period"],
            y=cf_df["cabin_factor"],
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in cf_df["cabin_factor"]],
            textposition="top center",
            line=dict(color=KA_GOLD, width=3),
            name="Cabin Factor"
        ))
        fig_cf.update_layout(
            title="Cabin factor trend",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=360,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )
        fig_cf.update_yaxes(title="%", gridcolor="#EEEEEE")
        st.plotly_chart(fig_cf, use_container_width=True)

    st.markdown(
        """
        <div class="section-note">
            Chart conclusion: FY2024 combined higher traffic with higher capacity and a modest improvement in utilization, supporting the commercial base of the reported result.
        </div>
        """,
        unsafe_allow_html=True
    )

    wa2, sb2, nw2 = st.columns(3)

    with wa2:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">What happened?</div>
                <div style="margin-top:0.35rem;">
                    FY2024 reported 5.23 million passengers, 16.23 billion ASK, and a 75.2% cabin factor, alongside cargo tonnage growth.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with sb2:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">So what?</div>
                <div style="margin-top:0.35rem;">
                    The top-line and operating result were supported by a larger operating base, rather than by pricing commentary alone.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with nw2:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">Now what?</div>
                <div style="margin-top:0.35rem;">
                    Watch whether future capacity and fleet availability continue to convert into traffic and utilization in a way that sustains earnings quality.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# TAB 4 — FINANCIAL POSITION & LIQUIDITY
# =====================================================

with tab4:
    st.subheader("Financial Position & Liquidity")
    st.caption("Purpose: show balance-sheet and funding condition.")

    st.markdown(
        """
        <div class="callout">
            <div style="font-weight:700; margin-bottom:0.25rem;">Executive callout</div>
            This section focuses on reported financial position and cash generation, rather than treating profitability in isolation.
        </div>
        """,
        unsafe_allow_html=True
    )

    fp1, fp2, fp3, fp4, fp5, fp6 = st.columns(6)

    assets_prior = compare_row["assets"] if compare_row is not None else None
    liab_prior = compare_row["liabilities"] if compare_row is not None else None
    eq_prior = compare_row["equity"] if compare_row is not None else None
    ocf_prior = compare_row["operating_cashflow"] if compare_row is not None else None
    inv_prior = compare_row["investing_cashflow"] if compare_row is not None else None
    cash_prior = compare_row["cash_end_ksh_bn"] if compare_row is not None else None

    fp1.metric("Total Assets", fmt_bn(selected_row["assets"]), pct_change_text(selected_row["assets"], assets_prior))
    fp2.metric("Total Liabilities", fmt_bn(selected_row["liabilities"]), pct_change_text(selected_row["liabilities"], liab_prior))
    fp3.metric("Total Equity", fmt_bn(selected_row["equity"]), pct_change_text(selected_row["equity"], eq_prior))
    fp4.metric("Operating Cash Flow", fmt_bn(selected_row["operating_cashflow"]), pct_change_text(selected_row["operating_cashflow"], ocf_prior))
    fp5.metric("Investing Cash Flow", fmt_bn(selected_row["investing_cashflow"]), pct_change_text(selected_row["investing_cashflow"], inv_prior))
    fp6.metric("Year-end Cash", fmt_bn(selected_row["cash_end_ksh_bn"]), pct_change_text(selected_row["cash_end_ksh_bn"], cash_prior))

    left_fp, right_fp = st.columns(2)

    with left_fp:
        fp_chart_df = financial_df[financial_df["period"].isin(["FY2023", "FY2024"])].copy()
        fig_fp = go.Figure()
        fig_fp.add_trace(go.Bar(
            x=fp_chart_df["period"],
            y=fp_chart_df["assets"],
            name="Assets",
            marker_color=KA_DARK
        ))
        fig_fp.add_trace(go.Bar(
            x=fp_chart_df["period"],
            y=fp_chart_df["liabilities"],
            name="Liabilities",
            marker_color=KA_RED
        ))
        fig_fp.update_layout(
            title="Assets vs liabilities",
            barmode="group",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=390,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        fig_fp.update_yaxes(title="KSh bn", gridcolor="#EEEEEE")
        st.plotly_chart(fig_fp, use_container_width=True)

    with right_fp:
        cash_seq = pd.DataFrame({
            "Flow": ["Operating", "Investing", "Financing", "Ending Cash"],
            "Value": [
                selected_row["operating_cashflow"],
                selected_row["investing_cashflow"],
                selected_row["financing_cashflow"],
                selected_row["cash_end_ksh_bn"]
            ]
        })

        fig_cash = go.Figure()
        fig_cash.add_trace(go.Bar(
            x=cash_seq["Flow"],
            y=cash_seq["Value"],
            marker_color=[KA_GREEN, KA_GOLD, KA_GRAY, KA_RED]
        ))
        fig_cash.update_layout(
            title=f"Cash flow and ending cash — {selected_period}",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=390,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )
        fig_cash.update_yaxes(title="KSh bn", gridcolor="#EEEEEE")
        st.plotly_chart(fig_cash, use_container_width=True)

    st.markdown(
        """
        <div class="section-note">
            Chart conclusion: FY2024 combined positive operating cash generation with a year-end cash balance, while liabilities remained materially larger than equity.
        </div>
        """,
        unsafe_allow_html=True
    )

    snapshot_df = pd.DataFrame({
        "Metric": [
            "Total Assets",
            "Total Liabilities",
            "Total Equity",
            "Operating Cash Flow",
            "Investing Cash Flow",
            "Financing Cash Flow",
            "Year-end Cash"
        ],
        selected_period: [
            fmt_bn(selected_row["assets"]),
            fmt_bn(selected_row["liabilities"]),
            fmt_bn(selected_row["equity"]),
            fmt_bn(selected_row["operating_cashflow"]),
            fmt_bn(selected_row["investing_cashflow"]),
            fmt_bn(selected_row["financing_cashflow"]),
            fmt_bn(selected_row["cash_end_ksh_bn"]),
        ]
    })
    st.dataframe(snapshot_df, use_container_width=True, hide_index=True)

    wa3, sb3, nw3 = st.columns(3)

    with wa3:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">What happened?</div>
                <div style="margin-top:0.35rem;">
                    The selected annual base period shows positive reported operating cash flow and a year-end cash balance, alongside a still-heavy liability position.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with sb3:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">So what?</div>
                <div style="margin-top:0.35rem;">
                    Earnings improvement matters more when it translates into cash generation, but balance-sheet context remains essential for interpreting resilience.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with nw3:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">Now what?</div>
                <div style="margin-top:0.35rem;">
                    Leadership should continue to monitor liquidity, liability burden, and cash conversion alongside reported profit recovery.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="trust-box">
            <b>Limitation note:</b> Detailed current/non-current breakdowns, debt schedules, and lease detail are not expanded here unless explicitly captured in the loaded reported figures.
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# TAB 5 — LATEST UPDATE: HY2025
# =====================================================

with tab5:
    st.subheader("Latest Update: HY2025")
    st.caption("Purpose: separate the most recent interim change from the FY2024 audited base.")

    st.markdown(
        f"""
        <div class="banner" style="background:linear-gradient(90deg,{KA_GOLD}, {KA_DARK});">
            <div style="font-size:1.15rem;font-weight:700;">HY2025 interim update layer</div>
            <div class="banner-sub">
                Interim period shown separately from FY2024 annual base. Do not read as a like-for-like full-year continuation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    hy25 = financial_df[financial_df["period"] == "HY2025"].iloc[0]
    hy24 = financial_df[financial_df["period"] == "HY2024"].iloc[0]
    hy25_ops = operating_df[operating_df["period"] == "HY2025"].iloc[0]
    hy24_ops = operating_df[operating_df["period"] == "HY2024"].iloc[0]

    u1, u2, u3, u4, u5, u6 = st.columns(6)
    u1.metric("Revenue", fmt_bn(hy25["revenue"]), pct_change_text(hy25["revenue"], hy24["revenue"]))
    u2.metric("Operating Result", fmt_bn(hy25["operating_profit"]), pct_change_text(hy25["operating_profit"], hy24["operating_profit"]))
    u3.metric("PBT", fmt_bn(hy25["pbt"]), pct_change_text(hy25["pbt"], hy24["pbt"]))
    u4.metric("Passengers", fmt_m(hy25_ops["passengers"]), pct_change_text(hy25_ops["passengers"], hy24_ops["passengers"]))
    u5.metric("Capacity / ASK", f"{hy25_ops['capacity_ask']:.2f}bn", pct_change_text(hy25_ops["capacity_ask"], hy24_ops["capacity_ask"]))
    u6.metric("Fleet Watchpoint", "Grounded wide-bodies", "Operational pressure")

    st.markdown(
        """
        <div class="what-changed">
            <b>What changed in HY2025?</b><br>
            Revenue declined versus HY2024, traffic and capacity both moved lower, and the interim period shifted from operating profit to operating loss.
        </div>
        """,
        unsafe_allow_html=True
    )

    hy_comp = pd.DataFrame({
        "Metric": ["Revenue", "Operating Result", "PBT", "Passengers", "Capacity / ASK"],
        "HY2024": [hy24["revenue"], hy24["operating_profit"], hy24["pbt"], hy24_ops["passengers"], hy24_ops["capacity_ask"]],
        "HY2025": [hy25["revenue"], hy25["operating_profit"], hy25["pbt"], hy25_ops["passengers"], hy25_ops["capacity_ask"]],
    })

    left_hy, right_hy = st.columns(2)

    with left_hy:
        fig_hy = go.Figure()
        fig_hy.add_trace(go.Bar(
            x=["Revenue", "Passengers", "Capacity / ASK"],
            y=[hy24["revenue"], hy24_ops["passengers"], hy24_ops["capacity_ask"]],
            name="HY2024",
            marker_color=KA_GRAY
        ))
        fig_hy.add_trace(go.Bar(
            x=["Revenue", "Passengers", "Capacity / ASK"],
            y=[hy25["revenue"], hy25_ops["passengers"], hy25_ops["capacity_ask"]],
            name="HY2025",
            marker_color=KA_RED
        ))
        fig_hy.update_layout(
            title="HY2025 vs HY2024 — commercial comparison",
            barmode="group",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=390,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        fig_hy.update_yaxes(gridcolor="#EEEEEE")
        st.plotly_chart(fig_hy, use_container_width=True)

    with right_hy:
        fig_hy_profit = go.Figure()
        fig_hy_profit.add_trace(go.Bar(
            x=["Operating Result", "PBT"],
            y=[hy24["operating_profit"], hy24["pbt"]],
            name="HY2024",
            marker_color=KA_GRAY
        ))
        fig_hy_profit.add_trace(go.Bar(
            x=["Operating Result", "PBT"],
            y=[hy25["operating_profit"], hy25["pbt"]],
            name="HY2025",
            marker_color=KA_GOLD
        ))
        fig_hy_profit.update_layout(
            title="HY2025 vs HY2024 — earnings comparison",
            barmode="group",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=390,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        fig_hy_profit.update_yaxes(title="KSh bn", gridcolor="#EEEEEE")
        st.plotly_chart(fig_hy_profit, use_container_width=True)

    st.markdown(
        f"""
        <div class="callout" style="border-left:5px solid {KA_GOLD};">
            <div style="font-weight:700; margin-bottom:0.25rem;">Operational watchpoint</div>
            HY2025 should be read as an interim pressure period. The dashboard keeps it separate from FY2024 because fleet availability and lower traffic/capacity materially changed the reporting picture.
        </div>
        """,
        unsafe_allow_html=True
    )

    wa4, sb4, nw4 = st.columns(3)

    with wa4:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">What happened?</div>
                <div style="margin-top:0.35rem;">
                    HY2025 showed lower revenue, lower traffic, lower capacity, and a weaker operating and pretax outcome than HY2024.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with sb4:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">So what?</div>
                <div style="margin-top:0.35rem;">
                    The post-FY2024 picture is not a simple continuation of the annual turnaround; it is an interim setback that needs separate reading.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with nw4:
        st.markdown(
            """
            <div class="wsbox">
                <div class="small-label">Now what?</div>
                <div style="margin-top:0.35rem;">
                    Watch fleet restoration, traffic normalization, and whether later reported periods recover commercial scale and operating performance.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# TAB 6 — SOURCES, NOTES & LIMITATIONS
# =====================================================

with tab6:
    st.subheader("Sources, Notes & Limitations")
    st.caption("Purpose: make the dashboard credible and review-ready.")

    st.markdown(
        """
        <div class="callout">
            <div style="font-weight:700; margin-bottom:0.25rem;">Source hierarchy</div>
            FY2024 annual reporting forms the base layer. HY2025 is a separate interim update layer. Secondary press context should not override official reported figures.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Source Register")
    st.dataframe(source_register, use_container_width=True, hide_index=True)

    st.markdown("### Scope Notes")
    scope_df = pd.DataFrame({
        "Item": [
            "Truth mode",
            "Base layer",
            "Update layer",
            "Forecasts",
            "Synthetic segment data",
            "Narrative rule"
        ],
        "Status": [
            "Verified Actuals Mode only",
            "FY2024 audited / reported",
            "HY2025 interim, shown separately",
            "Not included",
            "Not used",
            "Descriptive, evidence-based only"
        ]
    })
    st.dataframe(scope_df, use_container_width=True, hide_index=True)

    st.markdown("### Omitted / Limited Items")
    omission_df = pd.DataFrame({
        "Area": [
            "Route-level performance",
            "Geographic segment splits",
            "Detailed debt maturity schedule",
            "Detailed lease schedule",
            "Forecast / guidance module",
            "Management intent / strategy claims"
        ],
        "Treatment": [
            "Omitted unless explicitly reported",
            "Omitted unless explicitly reported",
            "Not expanded in Version 1",
            "Not expanded in Version 1",
            "Not included",
            "Not inferred"
        ]
    })
    st.dataframe(omission_df, use_container_width=True, hide_index=True)

    st.markdown("### Build Notes / Limitations")
    st.markdown(
        """
        - This dashboard uses only the period-level values embedded in the verified build scope.
        - FY2024 is treated as the annual base reporting layer.
        - HY2025 is intentionally separated to avoid mixing interim and annual storytelling.
        - Some detailed balance-sheet, lease, and financing breakdowns may require deeper extraction from source materials for a future version.
        - The design uses Kenya Airways-inspired colors in a restrained executive format rather than a marketing-style replica.
        """
    )

    st.markdown("### Suggested Version 2 Enhancements")
    st.markdown(
        """
        - Add current vs non-current statement breakdowns where fully extracted
        - Add signed-financials detail tables
        - Add investor-briefing commentary callouts
        - Add downloadable source appendix
        - Add richer selected-period comparison logic
        """
    )

# =====================================================
# GLOBAL FOOTER
# =====================================================

st.markdown("---")
st.markdown(
    f"""
    <div class="meta">
        Kenya Airways PLC – Executive Financial Dashboard &nbsp;&nbsp;|&nbsp;&nbsp;
        Verified Actuals Mode &nbsp;&nbsp;|&nbsp;&nbsp;
        FY2024 annual base + HY2025 interim update &nbsp;&nbsp;|&nbsp;&nbsp;
        Built with Streamlit / Pandas / Plotly &nbsp;&nbsp;|&nbsp;&nbsp;
        Last refreshed: {datetime.now().strftime("%Y-%m-%d")}
    </div>
    """,
    unsafe_allow_html=True
)
