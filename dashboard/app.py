from pathlib import Path
from html import escape

import altair as alt
import pandas as pd
import streamlit as st


# ============================================================
# SMART WASTE MANAGEMENT — FLEET INTELLIGENCE DASHBOARD
# ============================================================

st.set_page_config(
    page_title="Smart Waste Management",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def html_block(raw: str) -> None:
    st.markdown(" ".join(raw.split()), unsafe_allow_html=True)


# ============================================================
# 1. GLOBAL THEME
# ============================================================

html_block("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family:"Inter",sans-serif; }
.stApp { background:#161A24; color:#E8F1F5; }
.block-container { max-width:1450px; padding:35px 45px 50px; }

#MainMenu, footer, header, [data-testid="stSidebar"] {
    visibility:hidden; display:none;
}

.app-header { padding-bottom:25px; margin-bottom:25px; border-bottom:1px solid #1D303C; }
.app-eyebrow { color:#2DD4BF; font-size:11px; font-weight:800; letter-spacing:2px; margin-bottom:8px; }
.app-title { color:#F4F8FA; font-size:34px; font-weight:800; letter-spacing:-1.2px; margin-bottom:7px; }
.app-subtitle { color:#8198A6; font-size:13px; line-height:1.6; }

.live-badge {
    display:inline-flex; align-items:center; gap:8px; padding:7px 12px;
    border-radius:20px; background:#0D2929; border:1px solid #174A47;
    color:#5EEAD4; font-size:11px; font-weight:700;
}
.live-dot {
    width:7px; height:7px; border-radius:50%; background:#2DD4BF;
    display:inline-block; box-shadow:0 0 8px rgba(45,212,191,.7);
}

.section-heading { margin-top:30px; margin-bottom:15px; }
.section-label { color:#2DD4BF; font-size:10px; font-weight:800; letter-spacing:1.8px; margin-bottom:5px; }
.section-title { color:#F1F6F8; font-size:19px; font-weight:700; margin-bottom:4px; }
.section-description { color:#718996; font-size:11px; }

[data-testid="stMetric"] {
    background:#10232E; border:1px solid #1D3A47; border-radius:14px;
    padding:18px 20px; min-height:120px;
}
[data-testid="stMetricLabel"] {
    color:#78909D !important; font-size:10px !important;
    font-weight:700 !important; text-transform:uppercase; letter-spacing:.8px;
}
[data-testid="stMetricValue"] {
    color:#F2F7F8 !important; font-size:26px !important; font-weight:800 !important;
}
[data-testid="stMetricDelta"] { font-size:10px !important; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:#10232E; border:1px solid #1D3A47; border-radius:14px;
}

.card-heading { color:#F1F6F8; font-size:14px; font-weight:700; margin-bottom:3px; }
.card-description { color:#718996; font-size:12px; margin-bottom:12px; }

.filter-bar {
    background:#10232E; border:1px solid #1D3A47; border-radius:14px;
    padding:14px 20px 6px; margin-bottom:8px;
}
.filter-label { color:#2DD4BF; font-size:10px; font-weight:800; letter-spacing:1.4px; }

.filter-chip {
    display:inline-flex; align-items:center; gap:6px; background:#0D2929;
    border:1px solid #174A47; color:#5EEAD4; padding:4px 10px;
    border-radius:14px; font-size:10.5px; font-weight:700; margin:8px 0 5px;
}

div[data-baseweb="select"] > div {
    background:#0D1820 !important; border-color:#29404D !important;
}
div[data-baseweb="select"] span { color:#DCE6EA !important; }

/* ============================================================
   CUSTOM TABLE
   ============================================================ */

.custom-table-wrapper {
    background:rgba(255,255,255,.018);
    border:1px solid rgba(130,160,175,.22);
    border-radius:14px;
    overflow-x:auto;
    margin-top:8px;
}

.custom-table {
    width:100%;
    min-width:900px;
    border-collapse:separate;
    border-spacing:0;
    font-family:"Inter",sans-serif;
}

.custom-table thead { background:rgba(255,255,255,.055); }

.custom-table th {
    color:#9FB1BB;
    font-size:11px;
    font-weight:700;
    text-align:left;
    padding:13px 12px;
    border-bottom:1px solid rgba(130,160,175,.18);
    white-space:nowrap;
}

.custom-table td {
    color:#DCE6EA;
    font-size:11px;
    padding:12px;
    border-bottom:1px solid rgba(130,160,175,.10);
    background:rgba(255,255,255,.012);
    white-space:nowrap;
}

.custom-table tbody tr:nth-child(even) td { background:rgba(255,255,255,.025); }
.custom-table tbody tr:hover td { background:rgba(45,212,191,.07); }
.custom-table tbody tr:last-child td { border-bottom:none; }

.bin-id { color:#F1F6F8 !important; font-weight:600; }
.location-text { color:#DCE6EA !important; font-weight:500; }
.number-text { color:#DCE6EA !important; text-align:right; font-variant-numeric:tabular-nums; }

.progress-cell {
    display:flex; align-items:center; gap:10px; min-width:220px;
}
.progress-track {
    width:150px; height:7px; background:rgba(255,255,255,.09);
    border:1px solid rgba(130,160,175,.12); border-radius:20px;
    overflow:hidden; flex-shrink:0;
}
.progress-fill { height:100%; background:#2DD4BF; border-radius:20px; }
.progress-fill-warning { height:100%; background:#F6C76B; border-radius:20px; }
.progress-fill-critical { height:100%; background:#FF7F7F; border-radius:20px; }
.progress-value { color:#C8D8DE; font-size:10px; min-width:42px; }

.status-badge {
    display:inline-flex; align-items:center; padding:4px 9px;
    border-radius:20px; font-size:10px; font-weight:700;
}
.status-healthy {
    background:rgba(45,212,191,.10); color:#5EEAD4;
    border:1px solid rgba(45,212,191,.20);
}
.status-critical {
    background:rgba(255,127,127,.10); color:#FF9B9B;
    border:1px solid rgba(255,127,127,.20);
}
.status-high, .status-low {
    background:rgba(246,199,107,.10); color:#F6C76B;
    border:1px solid rgba(246,199,107,.20);
}

.priority-critical { color:#FF9B9B; font-weight:700; }
.priority-high { color:#F6C76B; font-weight:700; }
.priority-medium { color:#D9CC72; font-weight:700; }
.priority-low { color:#5EEAD4; font-weight:700; }

.empty-table { padding:25px; color:#718996; text-align:center; font-size:11px; }

.dashboard-footer {
    margin-top:40px; padding-top:18px; border-top:1px solid #1D303C;
    text-align:center; color:#526B78; font-size:10px;
}
</style>
""")


# ============================================================
# 2. PROJECT PATHS + DATA
# ============================================================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]
ANALYTICS_ROOT = PROJECT_ROOT / "data" / "processed" / "analytics"


def find_parquet_file(dataset_name: str) -> Path:
    folder = ANALYTICS_ROOT / dataset_name
    if not folder.exists():
        raise FileNotFoundError(f"Dataset folder does not exist:\n{folder}")

    files = sorted(folder.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No Parquet files found in:\n{folder}")

    return files[0]


@st.cache_data(ttl=30)
def load_all_data():
    names = [
        "overall_summary",
        "collection_priority",
        "battery_status",
        "location_analysis",
        "critical_bins",
        "bin_analysis",
    ]
    return {
        name: pd.read_parquet(find_parquet_file(name))
        for name in names
    }


try:
    data = load_all_data()
except Exception as error:
    st.error("Unable to load the analytics Parquet datasets.")
    st.code(str(error))
    st.stop()

overall = data["overall_summary"]
priority = data["collection_priority"]
battery = data["battery_status"]
location = data["location_analysis"]
critical = data["critical_bins"]
bin_perf = data["bin_analysis"]


def get_value(df, column, default=0):
    if df is None or df.empty or column not in df.columns:
        return default
    value = df.iloc[0][column]
    return default if pd.isna(value) else value


def number(value, decimals=0):
    try:
        return f"{float(value):,.{decimals}f}"
    except Exception:
        return "0"


def convert_numeric(df, columns):
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
    return df


def safe(value):
    return "" if pd.isna(value) else escape(str(value))


def progress_bar(value, kind="normal"):
    try:
        value = max(0, min(100, float(value)))
    except Exception:
        value = 0

    css = {
        "normal": "progress-fill",
        "warning": "progress-fill-warning",
        "critical": "progress-fill-critical",
    }.get(kind, "progress-fill")

    return (
        f'<div class="progress-cell">'
        f'<div class="progress-track"><div class="{css}" '
        f'style="width:{value:.1f}%"></div></div>'
        f'<span class="progress-value">{value:.1f}%</span>'
        f'</div>'
    )


def status_badge(value):
    value = str(value)
    css = {
        "Healthy": "status-healthy",
        "Critical": "status-critical",
        "High Fill": "status-high",
        "Low Battery": "status-low",
    }.get(value, "status-healthy")
    return f'<span class="status-badge {css}">{safe(value)}</span>'


def priority_badge(value):
    value = str(value)
    css = {
        "Critical": "priority-critical",
        "High": "priority-high",
        "Medium": "priority-medium",
        "Low": "priority-low",
    }.get(value, "priority-low")
    return f'<span class="{css}">{safe(value)}</span>'


# ============================================================
# 3. DATA PREPARATION
# ============================================================

location = convert_numeric(
    location,
    ["total_waste_kg", "avg_fill_level", "avg_battery_level",
     "sensor_readings", "readings"],
)

bin_perf = convert_numeric(
    bin_perf,
    ["avg_fill_level", "avg_battery_level", "total_waste_kg",
     "readings", "max_fill_level"],
)

priority = convert_numeric(priority, ["count"])
battery = convert_numeric(battery, ["count"])
critical = convert_numeric(
    critical,
    ["fill_level", "weight_kg", "battery_level"],
)


# ============================================================
# 4. HEADER
# ============================================================

left, right = st.columns([5, 1], gap="large")

with left:
    html_block("""
    <div class="app-header">
        <div class="app-eyebrow">SMART CITY • WASTE OPERATIONS</div>
        <div class="app-title">Collection Command</div>
        <div class="app-subtitle">
            Real-time visibility into collection priorities, bin utilization,
            sensor health and operational zones.
        </div>
    </div>
    """)

with right:
    html_block("""
    <div style="display:flex;justify-content:flex-end;padding-top:15px;">
        <div class="live-badge"><span class="live-dot"></span>PIPELINE ACTIVE</div>
    </div>
    """)


# ============================================================
# 5. LOCATION FILTER
# ============================================================

all_locations = (
    sorted(location["location"].dropna().unique().tolist())
    if not location.empty and "location" in location.columns
    else []
)

with st.container():
    html_block("""
    <div class="filter-bar">
        <div class="filter-label">FILTER · LOCATION</div>
    </div>
    """)

    selected_locations = st.multiselect(
        "Filter by location",
        options=all_locations,
        default=all_locations,
        label_visibility="collapsed",
    )

filter_active = bool(all_locations) and (
    0 < len(selected_locations) < len(all_locations)
)

if selected_locations:
    location = location[
        location["location"].isin(selected_locations)
    ].copy()

    if "location" in critical.columns:
        critical = critical[
            critical["location"].isin(selected_locations)
        ].copy()

    if "location" in bin_perf.columns:
        bin_perf = bin_perf[
            bin_perf["location"].isin(selected_locations)
        ].copy()

    if "location" in priority.columns:
        priority = priority[
            priority["location"].isin(selected_locations)
        ].copy()

    if "location" in battery.columns:
        battery = battery[
            battery["location"].isin(selected_locations)
        ].copy()

elif all_locations:
    location = location.iloc[0:0]
    critical = critical.iloc[0:0]
    bin_perf = bin_perf.iloc[0:0]

if filter_active:
    html_block(
        f'<div class="filter-chip">● Showing {len(selected_locations)} '
        f'of {len(all_locations)} locations</div>'
    )


# ============================================================
# 6. KPI
# ============================================================

html_block("""
<div class="section-heading">
    <div class="section-label">NETWORK OVERVIEW</div>
    <div class="section-title">Operational Overview</div>
    <div class="section-description">
        Current operational indicators across the monitored waste network.
    </div>
</div>
""")

readings_col = (
    "sensor_readings" if "sensor_readings" in location.columns
    else "readings" if "readings" in location.columns
    else None
)

if filter_active and not location.empty:
    total_records = (
        location[readings_col].sum()
        if readings_col else get_value(overall, "total_records", 0)
    )
    total_waste = (
        location["total_waste_kg"].sum()
        if "total_waste_kg" in location.columns else 0
    )
    weights = location[readings_col] if readings_col else None

    if readings_col and weights.sum() > 0:
        avg_fill = (location["avg_fill_level"] * weights).sum() / weights.sum()
        avg_battery = (
            location["avg_battery_level"] * weights
        ).sum() / weights.sum()
    else:
        avg_fill = (
            location["avg_fill_level"].mean()
            if "avg_fill_level" in location.columns else 0
        )
        avg_battery = (
            location["avg_battery_level"].mean()
            if "avg_battery_level" in location.columns else 0
        )
else:
    total_records = get_value(overall, "total_records", 0)
    total_waste = get_value(overall, "total_waste_kg", 0)
    avg_fill = get_value(overall, "avg_fill_level", 0)
    avg_battery = get_value(overall, "avg_battery_level", 0)

k1, k2, k3, k4, k5 = st.columns(5, gap="medium")

with k1:
    st.metric("Sensor Readings", number(total_records))
with k2:
    st.metric("Total Waste", f"{number(total_waste, 1)} kg")
with k3:
    st.metric("Average Fill", f"{number(avg_fill, 1)}%")
with k4:
    st.metric("Battery Health", f"{number(avg_battery, 1)}%")
with k5:
    st.metric("Critical Bins", number(len(critical)))


# ============================================================
# 7. DONUTS
# ============================================================

html_block("""
<div class="section-heading">
    <div class="section-label">COLLECTION PRIORITY</div>
    <div class="section-title">Where attention is needed</div>
    <div class="section-description">
        Composition of sensor readings by collection urgency and power status.
    </div>
</div>
""")


def donut_chart(df, category, value, colors, selection=None):
    enc = dict(
        theta=alt.Theta(f"{value}:Q"),
        color=alt.Color(
            f"{category}:N",
            scale=alt.Scale(
                domain=list(colors.keys()),
                range=list(colors.values()),
            ),
            legend=alt.Legend(
                orient="right", title=None,
                labelColor="#A8BAC4", labelFontSize=11, symbolSize=90,
            ),
        ),
        tooltip=[
            alt.Tooltip(f"{category}:N", title="Status"),
            alt.Tooltip(f"{value}:Q", title="Readings", format=","),
        ],
    )

    if selection is not None:
        enc["opacity"] = alt.condition(
            selection, alt.value(1), alt.value(.35)
        )

    chart = (
        alt.Chart(df)
        .mark_arc(
            innerRadius=62, outerRadius=92,
            cornerRadius=4, stroke="#10232E", strokeWidth=3,
        )
        .encode(**enc)
        .properties(height=260)
        .configure_view(strokeOpacity=0)
        .configure(background="transparent")
    )

    if selection is not None:
        chart = chart.add_params(selection)

    return chart


priority_colors = {
    "Critical": "#FF7F7F",
    "High": "#F6C76B",
    "Medium": "#D9CC72",
    "Low": "#2DD4BF",
}
battery_colors = {
    "Healthy": "#2DD4BF",
    "Low": "#F6C76B",
    "Critical": "#FF7F7F",
}

selected_priorities = []

d1, d2 = st.columns(2, gap="medium")

with d1:
    with st.container(border=True):
        html_block("""
        <div class="card-heading">Priority Collection Queue</div>
        <div class="card-description">
            Bins requiring the highest collection attention.
        </div>
        """)

        if (
            not priority.empty
            and "collection_priority" in priority.columns
            and "count" in priority.columns
        ):
            try:
                selection = alt.selection_point(
                    fields=["collection_priority"],
                    name="prio_sel",
                    toggle=True,
                )
                chart = donut_chart(
                    priority, "collection_priority", "count",
                    priority_colors, selection
                )
                result = st.altair_chart(
                    chart,
                    use_container_width=True,
                    on_select="rerun",
                    key="priority_donut",
                )
                selected = (
                    (result or {})
                    .get("selection", {})
                    .get("prio_sel", [])
                )
                selected_priorities = [
                    row["collection_priority"] for row in selected
                ] if selected else []
            except TypeError:
                st.altair_chart(
                    donut_chart(
                        priority, "collection_priority", "count",
                        priority_colors
                    ),
                    use_container_width=True,
                )
        else:
            st.info("Collection priority data is unavailable.")

with d2:
    with st.container(border=True):
        html_block("""
        <div class="card-heading">Battery Health</div>
        <div class="card-description">
            Distribution of sensor power status across the fleet.
        </div>
        """)

        if (
            not battery.empty
            and "battery_status" in battery.columns
            and "count" in battery.columns
        ):
            st.altair_chart(
                donut_chart(
                    battery, "battery_status", "count", battery_colors
                ),
                use_container_width=True,
            )
        else:
            st.info("Battery health data is unavailable.")


# ============================================================
# 8. LOCATION ANALYTICS
# ============================================================

html_block("""
<div class="section-heading">
    <div class="section-label">OPERATIONAL PERFORMANCE</div>
    <div class="section-title">Location Analytics</div>
    <div class="section-description">
        Compare waste generation and bin utilization across operating zones.
    </div>
</div>
""")

location_left, location_right = st.columns([1.15, .85], gap="medium")

with location_left:
    with st.container(border=True):
        html_block("""
        <div class="card-heading">Waste Generated by Location</div>
        <div class="card-description">
            Total accumulated waste across monitored locations.
        </div>
        """)

        if (
            not location.empty
            and "location" in location.columns
            and "total_waste_kg" in location.columns
        ):
            chart_data = (
                location[["location", "total_waste_kg"]]
                .copy()
                .sort_values("total_waste_kg", ascending=False)
            )
            chart = (
                alt.Chart(chart_data)
                .mark_bar(cornerRadiusEnd=7, size=25, color="#2DD4BF")
                .encode(
                    y=alt.Y(
                        "location:N", sort="-x", title=None,
                        axis=alt.Axis(
                            labelColor="#A8BAC4",
                            labelFontSize=11,
                            ticks=False, domain=False,
                        ),
                    ),
                    x=alt.X(
                        "total_waste_kg:Q", title="Waste (kg)",
                        axis=alt.Axis(
                            labelColor="#718996",
                            labelFontSize=10,
                            gridColor="#203542",
                            gridOpacity=.8,
                            domain=False,
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip("location:N", title="Location"),
                        alt.Tooltip(
                            "total_waste_kg:Q",
                            title="Waste (kg)",
                            format=",.2f",
                        ),
                    ],
                )
                .properties(height=310)
                .configure_view(strokeOpacity=0)
                .configure(background="transparent")
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Location waste data is unavailable.")

with location_right:
    with st.container(border=True):
        html_block("""
        <div class="card-heading">Average Fill Level</div>
        <div class="card-description">
            Average utilization of bins in each monitored location.
        </div>
        """)

        if (
            not location.empty
            and "location" in location.columns
            and "avg_fill_level" in location.columns
        ):
            chart_data = (
                location[["location", "avg_fill_level"]]
                .copy()
                .sort_values("avg_fill_level", ascending=False)
            )
            chart = (
                alt.Chart(chart_data)
                .mark_bar(cornerRadiusEnd=7, size=25, color="#60A5FA")
                .encode(
                    y=alt.Y(
                        "location:N", sort="-x", title=None,
                        axis=alt.Axis(
                            labelColor="#A8BAC4",
                            labelFontSize=11,
                            ticks=False, domain=False,
                        ),
                    ),
                    x=alt.X(
                        "avg_fill_level:Q",
                        title="Fill (%)",
                        scale=alt.Scale(domain=[0, 100]),
                        axis=alt.Axis(
                            labelColor="#718996",
                            labelFontSize=10,
                            gridColor="#203542",
                            gridOpacity=.8,
                            domain=False,
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip("location:N", title="Location"),
                        alt.Tooltip(
                            "avg_fill_level:Q",
                            title="Average Fill (%)",
                            format=".1f",
                        ),
                    ],
                )
                .properties(height=310)
                .configure_view(strokeOpacity=0)
                .configure(background="transparent")
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Fill-level data is unavailable.")


# ============================================================
# 9. SENSOR HEALTH
# ============================================================

html_block("""
<div class="section-heading">
    <div class="section-label">SENSOR HEALTH</div>
    <div class="section-title">Fleet Health Monitor</div>
    <div class="section-description">
        Identify bins with high utilization or weak battery conditions.
    </div>
</div>
""")

fleet_df = bin_perf.copy()

if not fleet_df.empty:
    def calculate_status(row):
        fill = float(row.get("avg_fill_level", 0))
        battery_level = float(row.get("avg_battery_level", 0))

        if fill >= 85 and battery_level < 30:
            return "Critical"
        if fill >= 85:
            return "High Fill"
        if battery_level < 30:
            return "Low Battery"
        return "Healthy"

    fleet_df["sensor_status"] = fleet_df.apply(
        calculate_status, axis=1
    )

critical_bins = (
    int((fleet_df["sensor_status"] == "Critical").sum())
    if not fleet_df.empty else 0
)
high_fill_bins = (
    int((fleet_df["sensor_status"] == "High Fill").sum())
    if not fleet_df.empty else 0
)
low_battery_bins = (
    int((fleet_df["sensor_status"] == "Low Battery").sum())
    if not fleet_df.empty else 0
)
healthy_bins = (
    int((fleet_df["sensor_status"] == "Healthy").sum())
    if not fleet_df.empty else 0
)

h1, h2, h3, h4 = st.columns(4, gap="medium")

with h1:
    st.metric("Healthy Sensors", healthy_bins)
with h2:
    st.metric("High Fill", high_fill_bins)
with h3:
    st.metric("Low Battery", low_battery_bins)
with h4:
    st.metric("Critical", critical_bins)


# ------------------------------------------------------------
# FLEET TABLE — HTML, NOT st.dataframe
# ------------------------------------------------------------

if not fleet_df.empty:
    status_order = {
        "Critical": 0,
        "High Fill": 1,
        "Low Battery": 2,
        "Healthy": 3,
    }

    if "sensor_status" in fleet_df.columns:
        fleet_df["_sort"] = (
            fleet_df["sensor_status"]
            .map(status_order)
            .fillna(99)
        )
        fleet_df = fleet_df.sort_values("_sort").drop(columns="_sort")

    fleet_df = fleet_df.head(15)

    with st.container(border=True):
        html_block("""
        <div class="card-heading">Sensor Fleet Status</div>
        <div class="card-description">
            Priority-ranked view of monitored bins.
        </div>
        """)

        rows = []

        for _, row in fleet_df.iterrows():
            fill = float(row.get("avg_fill_level", 0))
            batt = float(row.get("avg_battery_level", 0))
            waste = float(row.get("total_waste_kg", 0))
            status = row.get("sensor_status", "Healthy")

            fill_kind = (
                "critical" if fill >= 85
                else "warning" if fill >= 70
                else "normal"
            )
            batt_kind = (
                "critical" if batt < 30
                else "warning" if batt < 50
                else "normal"
            )

            rows.append(f"""
            <tr>
                <td class="bin-id">{safe(row.get("bin_id", "—"))}</td>
                <td class="location-text">{safe(row.get("location", "—"))}</td>
                <td>{progress_bar(fill, fill_kind)}</td>
                <td>{progress_bar(batt, batt_kind)}</td>
                <td class="number-text">{waste:,.2f}</td>
                <td>{status_badge(status)}</td>
            </tr>
            """)

        html_block(f"""
        <div class="custom-table-wrapper">
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Bin ID</th>
                        <th>Location</th>
                        <th>Avg Fill (%)</th>
                        <th>Battery (%)</th>
                        <th>Waste (kg)</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        """)
else:
    st.info("No bin performance data available.")


# ============================================================
# 10. PRIORITY COLLECTION QUEUE
# ============================================================

html_block("""
<div class="section-heading">
    <div class="section-label">COLLECTION OPERATIONS</div>
    <div class="section-title">Priority Collection Queue</div>
    <div class="section-description">
        Bins currently requiring the highest collection attention.
    </div>
</div>
""")

queue_source = critical

if selected_priorities and "collection_priority" in critical.columns:
    queue_source = critical[
        critical["collection_priority"].isin(selected_priorities)
    ]
    html_block(
        f'<div class="filter-chip">● Filtered to: '
        f'{", ".join(safe(x) for x in selected_priorities)}</div>'
    )

if not queue_source.empty:
    queue_df = queue_source.head(15).copy()

    with st.container(border=True):
        rows = []

        for _, row in queue_df.iterrows():
            fill = float(row.get("fill_level", 0))
            batt = float(row.get("battery_level", 0))
            weight = float(row.get("weight_kg", 0))
            priority_value = row.get("collection_priority", "—")

            fill_kind = (
                "critical" if fill >= 85
                else "warning" if fill >= 70
                else "normal"
            )
            batt_kind = (
                "critical" if batt < 30
                else "warning" if batt < 50
                else "normal"
            )

            rows.append(f"""
            <tr>
                <td class="bin-id">{safe(row.get("bin_id", "—"))}</td>
                <td class="location-text">{safe(row.get("location", "—"))}</td>
                <td>{progress_bar(fill, fill_kind)}</td>
                <td class="number-text">{weight:,.2f}</td>
                <td>{progress_bar(batt, batt_kind)}</td>
                <td>{priority_badge(priority_value)}</td>
            </tr>
            """)

        html_block(f"""
        <div class="custom-table-wrapper">
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Bin ID</th>
                        <th>Location</th>
                        <th>Fill (%)</th>
                        <th>Weight (kg)</th>
                        <th>Battery (%)</th>
                        <th>Priority</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """)
else:
    with st.container(border=True):
        html_block("""
        <div class="empty-table">
            No critical collection events match the current filters.
        </div>
        """)


# ============================================================
# 11. LOCATION SUMMARY
# ============================================================

html_block("""
<div class="section-heading">
    <div class="section-label">LOCATION PERFORMANCE</div>
    <div class="section-title">Operational Zone Summary</div>
    <div class="section-description">
        Consolidated performance metrics for each monitored location.
    </div>
</div>
""")

if not location.empty:
    summary = location.copy()

    with st.container(border=True):
        rows = []

        for _, row in summary.iterrows():
            readings = row.get(
                "sensor_readings",
                row.get("readings", 0)
            )
            fill = float(row.get("avg_fill_level", 0))
            waste = float(row.get("total_waste_kg", 0))
            batt = float(row.get("avg_battery_level", 0))

            fill_kind = (
                "critical" if fill >= 85
                else "warning" if fill >= 70
                else "normal"
            )
            batt_kind = (
                "critical" if batt < 30
                else "warning" if batt < 50
                else "normal"
            )

            try:
                readings_text = f"{int(float(readings)):,}"
            except Exception:
                readings_text = "0"

            rows.append(f"""
            <tr>
                <td class="location-text">{safe(row.get("location", "—"))}</td>
                <td class="number-text">{readings_text}</td>
                <td>{progress_bar(fill, fill_kind)}</td>
                <td class="number-text">{waste:,.2f}</td>
                <td>{progress_bar(batt, batt_kind)}</td>
            </tr>
            """)

        html_block(f"""
        <div class="custom-table-wrapper">
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Readings</th>
                        <th>Avg Fill (%)</th>
                        <th>Waste (kg)</th>
                        <th>Battery (%)</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """)
else:
    st.info("Location summary data is unavailable for the current filter.")


# ============================================================
# 12. FOOTER
# ============================================================

html_block("""
<div class="dashboard-footer">
    Smart Waste Management • Urban Waste Intelligence
    &nbsp; | &nbsp; Apache Kafka
    &nbsp; | &nbsp; PySpark
    &nbsp; | &nbsp; Parquet
    &nbsp; | &nbsp; Streamlit
</div>
""")