"""
ISYS 573 Sales Dashboard
========================
Reads data/sales.csv and generates an interactive HTML report with:
  - Quarter filter dropdown (Q1 / Q2 / Q3 / Q4 / Full Year)
  - Revenue by region (bar chart)
  - Monthly revenue trend (line chart)
  - Revenue by category (pie chart)
  - Top 10 products by revenue (horizontal bar)
  - Summary KPI cards

Usage:
    python dashboard.py                      # outputs dashboard.html
    python dashboard.py --output report.html # custom output path
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


DATA_PATH = Path(__file__).parent / "data" / "sales.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and validate the sales CSV."""
    if not path.exists():
        raise FileNotFoundError(f"Sales data not found: {path}")
    df = pd.read_csv(path, parse_dates=["date"])
    required = {"date", "region", "category", "product",
                "units_sold", "unit_price", "revenue", "channel"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["quarter"] = df["date"].dt.quarter.map(
        {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
    )
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def build_region_bar(df: pd.DataFrame) -> go.Figure:
    """Revenue by region — horizontal bar chart."""
    summary = (
        df.groupby("region")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=True)   # ascending so largest is at top
    )
    colors = ["#9B59B6", "#02C39A", "#F4A261", "#00B4D8"]
    fig = go.Figure(go.Bar(
        x=summary["revenue"],
        y=summary["region"],
        orientation="h",
        marker_color=colors[:len(summary)],
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title="Revenue by Region",
        plot_bgcolor="white",
        xaxis=dict(tickprefix="$", tickformat=",.0f", title="Total Revenue ($)"),
        yaxis=dict(title="Region"),
        showlegend=False,
        margin=dict(t=50, b=30, l=80),
    )
    return fig


def build_monthly_line(df: pd.DataFrame) -> go.Figure:
    """Monthly revenue trend — line chart."""
    monthly = (
        df.groupby("month")["revenue"]
        .sum()
        .reset_index()
        .sort_values("month")
    )
    fig = px.line(
        monthly, x="month", y="revenue",
        markers=True,
        labels={"revenue": "Revenue ($)", "month": "Month"},
        title="Monthly Revenue Trend",
        color_discrete_sequence=["#2196F3"],
    )
    fig.update_layout(plot_bgcolor="white",
                      yaxis=dict(tickprefix="$", tickformat=",.0f"),
                      margin=dict(t=50, b=30))
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        line=dict(width=2.5)
    )
    return fig


def build_category_pie(df: pd.DataFrame) -> go.Figure:
    """Revenue by product category — pie chart."""
    cat = df.groupby("category")["revenue"].sum().reset_index()
    fig = px.pie(
        cat, names="category", values="revenue",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Revenue by Category",
        hole=0.35,
    )
    fig.update_traces(
        textposition="inside", textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(margin=dict(t=50, b=10))
    return fig


def build_top_products(df: pd.DataFrame, n: int = 10) -> go.Figure:
    """Top N products by revenue — horizontal bar chart."""
    top = (
        df.groupby("product")["revenue"]
        .sum()
        .nlargest(n)
        .reset_index()
        .sort_values("revenue")
    )
    fig = px.bar(
        top, x="revenue", y="product",
        orientation="h",
        color="revenue",
        color_continuous_scale="Blues",
        labels={"revenue": "Revenue ($)", "product": "Product"},
        title=f"Top {n} Products by Revenue",
    )
    fig.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="white",
        xaxis=dict(tickprefix="$", tickformat=",.0f"),
        margin=dict(t=50, b=30)
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>"
    )
    return fig


def build_sales_risk_insights(df: pd.DataFrame) -> list[dict[str, str]]:
    """Build transparent, data-grounded sales risk and opportunity insights."""
    if df.empty or "revenue" not in df.columns:
        return [{
            "title": "No insight data available",
            "priority": "Low",
            "evidence": "The selected period has no sales records to analyze.",
            "action": "Review the filter selection or source data before acting.",
        }]

    total_revenue = float(df["revenue"].sum())
    if total_revenue <= 0:
        return [{
            "title": "Revenue data requires review",
            "priority": "Low",
            "evidence": "The selected period has no positive revenue.",
            "action": "Validate the source data before using dashboard insights.",
        }]

    insights: list[dict[str, str]] = []

    if "region" in df.columns:
        region_revenue = df.groupby("region")["revenue"].sum().sort_values(
            ascending=False
        )
        top_region = str(region_revenue.index[0])
        top_region_revenue = float(region_revenue.iloc[0])
        top_region_share = top_region_revenue / total_revenue
        priority = "High" if top_region_share >= 0.35 else "Medium"
        insights.append({
            "title": f"Revenue concentration in {top_region}",
            "priority": priority,
            "evidence": (
                f"{top_region} contributes ${top_region_revenue:,.0f}, "
                f"or {top_region_share:.1%} of filtered revenue."
            ),
            "action": (
                f"Protect {top_region} performance while reviewing whether "
                "other regions can reduce dependency."
            ),
        })

        if len(region_revenue) > 1:
            low_region = str(region_revenue.index[-1])
            low_region_revenue = float(region_revenue.iloc[-1])
            average_region_revenue = float(region_revenue.mean())
            gap_to_average = average_region_revenue - low_region_revenue
            priority = (
                "High"
                if gap_to_average > average_region_revenue * 0.2
                else "Medium"
            )
            insights.append({
                "title": f"Underperformance watch: {low_region}",
                "priority": priority,
                "evidence": (
                    f"{low_region} generated ${low_region_revenue:,.0f}, "
                    f"${gap_to_average:,.0f} below the regional average."
                ),
                "action": (
                    f"Review product mix, channel coverage, and rep support in "
                    f"{low_region}."
                ),
            })

    if "category" in df.columns:
        category_revenue = df.groupby("category")["revenue"].sum().sort_values(
            ascending=False
        )
        top_category = str(category_revenue.index[0])
        top_category_revenue = float(category_revenue.iloc[0])
        top_category_share = top_category_revenue / total_revenue
        insights.append({
            "title": f"Growth opportunity: {top_category}",
            "priority": "Medium",
            "evidence": (
                f"{top_category} is the top category at "
                f"${top_category_revenue:,.0f}, or {top_category_share:.1%} "
                "of filtered revenue."
            ),
            "action": (
                f"Evaluate whether promotions, inventory, or sales enablement "
                f"can responsibly expand {top_category} momentum."
            ),
        })

    if "channel" in df.columns:
        channel_revenue = df.groupby("channel")["revenue"].sum().sort_values(
            ascending=False
        )
        top_channel = str(channel_revenue.index[0])
        top_channel_share = float(channel_revenue.iloc[0]) / total_revenue
        if top_channel_share >= 0.6:
            insights.append({
                "title": f"Channel dependency on {top_channel}",
                "priority": "Medium",
                "evidence": (
                    f"{top_channel} represents {top_channel_share:.1%} of "
                    "filtered revenue."
                ),
                "action": (
                    "Check whether the lower-share channel needs support or "
                    "whether the current channel mix is intentional."
                ),
            })

    return insights[:3]


def kpi_card_html(label: str, value: str, color: str = "#2196F3") -> str:
    """Render a single KPI card as HTML."""
    return f"""
    <div style="background:#fff;border-radius:8px;padding:20px 24px;
                box-shadow:0 2px 8px rgba(0,0,0,.08);text-align:center;
                border-top:4px solid {color};flex:1;min-width:160px;">
      <div style="font-size:13px;color:#666;font-weight:600;
                  text-transform:uppercase;letter-spacing:.5px;">{label}</div>
      <div style="font-size:28px;font-weight:700;color:#1a1a2e;margin-top:6px;">{value}</div>
    </div>"""


def build_html(df: pd.DataFrame) -> str:
    """
    Assemble the full dashboard HTML with quarter-filter dropdown.
    All charts are rendered as divs; JavaScript swaps the Plotly JSON
    when the user changes the dropdown selection.
    """
    quarters = ["Full Year", "Q1", "Q2", "Q3", "Q4"]
    chart_data: dict[str, dict] = {}

    for q in quarters:
        subset = df if q == "Full Year" else df[df["quarter"] == q]
        if subset.empty:
            # Placeholder for quarters with no data
            empty = go.Figure()
            empty.update_layout(title="No data for this period")
            chart_data[q] = {
                "region": empty.to_json(),
                "monthly": empty.to_json(),
                "category": empty.to_json(),
                "top_products": empty.to_json(),
                "total_revenue": "$0",
                "total_orders": "0",
                "avg_order": "$0",
                "insights": build_sales_risk_insights(subset),
                "top_region": "—",
            }
            continue

        total_rev = subset["revenue"].sum()
        total_orders = len(subset)
        avg_order = total_rev / total_orders if total_orders else 0
        top_region = (
            subset.groupby("region")["revenue"].sum().idxmax()
            if not subset.empty else "—"
        )

        chart_data[q] = {
            "region":       build_region_bar(subset).to_json(),
            "monthly":      build_monthly_line(subset).to_json(),
            "category":     build_category_pie(subset).to_json(),
            "top_products": build_top_products(subset).to_json(),
            "total_revenue": f"${total_rev:,.0f}",
            "total_orders":  f"{total_orders:,}",
            "avg_order":     f"${avg_order:,.0f}",
            "insights":      build_sales_risk_insights(subset),
            "top_region":    top_region,
        }

    # Serialize all chart data to embed in HTML
    import json
    chart_json = json.dumps(chart_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>ISYS 573 · Retail Sales Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0;}}
    body{{font-family:'Segoe UI',Arial,sans-serif;background:#f4f6f9;color:#1a1a2e;}}
    header{{background:linear-gradient(135deg,#0D1B2A 0%,#1E3A5F 100%);
            color:#fff;padding:24px 32px;display:flex;
            align-items:center;justify-content:space-between;}}
    header h1{{font-size:22px;font-weight:700;}}
    header p{{font-size:13px;color:#8DA9C4;margin-top:4px;}}
    .filter-bar{{background:#fff;padding:14px 32px;
                 border-bottom:1px solid #e0e6ed;
                 display:flex;align-items:center;gap:16px;}}
    .filter-bar label{{font-size:14px;font-weight:600;color:#444;}}
    select{{padding:8px 14px;border:1.5px solid #cdd8e3;border-radius:6px;
            font-size:14px;background:#fff;cursor:pointer;color:#1a1a2e;}}
    select:focus{{outline:none;border-color:#2196F3;}}
    .kpis{{display:flex;gap:16px;flex-wrap:wrap;padding:24px 32px 8px;}}
    .insights-panel{{margin:16px 32px 0;background:#fff;border-radius:10px;
                    box-shadow:0 2px 8px rgba(0,0,0,.06);padding:22px 24px;
                    border-left:4px solid #02C39A;}}
    .insights-heading{{display:flex;align-items:flex-start;justify-content:space-between;
                      gap:16px;margin-bottom:14px;}}
    .insights-heading h2{{font-size:18px;margin:0;color:#1a1a2e;}}
    .insights-note{{font-size:12px;color:#607080;max-width:520px;line-height:1.4;}}
    .insights-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}}
    .insight-card{{border:1px solid #e0e6ed;border-radius:8px;padding:14px;
                  background:#fbfcfe;min-height:164px;}}
    .insight-title-row{{display:flex;align-items:flex-start;justify-content:space-between;
                       gap:10px;margin-bottom:8px;}}
    .insight-title{{font-weight:700;font-size:14px;color:#1a1a2e;line-height:1.25;}}
    .priority{{font-size:11px;font-weight:700;text-transform:uppercase;
              border-radius:999px;padding:4px 8px;white-space:nowrap;}}
    .priority.high{{background:#ffebee;color:#b71c1c;}}
    .priority.medium{{background:#fff3e0;color:#a45a00;}}
    .priority.low{{background:#e8f5e9;color:#1b5e20;}}
    .insight-label{{font-size:11px;font-weight:700;color:#607080;
                   text-transform:uppercase;margin-top:10px;margin-bottom:3px;}}
    .insight-text{{font-size:13px;line-height:1.45;color:#2f3a45;}}
    .charts-grid{{display:grid;
                  grid-template-columns:1fr 1fr;
                  gap:20px;padding:16px 32px 32px;}}
    .chart-card{{background:#fff;border-radius:10px;
                 padding:8px;box-shadow:0 2px 8px rgba(0,0,0,.06);}}
    @media(max-width:1000px){{.insights-grid{{grid-template-columns:1fr;}}}}
    @media(max-width:800px){{.charts-grid{{grid-template-columns:1fr;}}
                            .insights-heading{{flex-direction:column;}}
                            .insights-panel{{margin:16px 18px 0;}}
                            .kpis{{padding-left:18px;padding-right:18px;}}
                            .charts-grid{{padding-left:18px;padding-right:18px;}}}}
    footer{{text-align:center;padding:16px;font-size:12px;color:#999;
            border-top:1px solid #e0e6ed;background:#fff;}}
  </style>
</head>
<body>

<header>
  <div>
    <h1>🛒 Retail Sales Dashboard</h1>
    <p>ISYS 573 · Generative AI and LLMs for Business · SFSU</p>
  </div>
  <div style="font-size:12px;color:#8DA9C4;text-align:right;">
    Data: 2024 Retail Sales<br>500 transactions · 4 regions · 6 categories
  </div>
</header>

<div class="filter-bar">
  <label for="qFilter">📅 Filter by Quarter:</label>
  <select id="qFilter" onchange="applyFilter(this.value)">
    {"".join(f'<option value="{q}">{q}</option>' for q in quarters)}
  </select>
  <span id="filterLabel" style="font-size:13px;color:#666;margin-left:8px;"></span>
</div>

<div class="kpis" id="kpiRow"></div>

<section class="insights-panel" aria-labelledby="insightsTitle">
  <div class="insights-heading">
    <h2 id="insightsTitle">AI Sales Risk Insights</h2>
    <p class="insights-note">
      Generated from the selected dashboard data using transparent business
      rules. Human review is required before action.
    </p>
  </div>
  <div class="insights-grid" id="insightsGrid"></div>
</section>

<div class="charts-grid">
  <div class="chart-card"><div id="chartRegion"  style="height:340px;"></div></div>
  <div class="chart-card"><div id="chartMonthly" style="height:340px;"></div></div>
  <div class="chart-card"><div id="chartCategory"    style="height:340px;"></div></div>
  <div class="chart-card"><div id="chartTopProducts" style="height:340px;"></div></div>
</div>

<footer>
  Built with Python · Pandas · Plotly &nbsp;|&nbsp;
  ISYS 573 AugOps Demo &nbsp;|&nbsp;
  github.com/[your-handle]/isys573-sales-dashboard
</footer>

<script>
const DATA = {chart_json};

const KPI_COLORS = ["#2196F3","#4CAF50","#FF9800","#9C27B0"];
const KPI_LABELS = ["Total Revenue","Transactions","Avg Transaction","Top Region"];
const KPI_KEYS   = ["total_revenue","total_orders","avg_order","top_region"];

function escapeHtml(value) {{
  return String(value).replace(/[&<>"']/g, char => ({{
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\\"": "&quot;",
    "'": "&#39;"
  }}[char]));
}}

function applyFilter(quarter) {{
  const d = DATA[quarter];

  // KPI cards
  const kpiRow = document.getElementById("kpiRow");
  kpiRow.innerHTML = KPI_KEYS.map((k,i) => `
    <div style="background:#fff;border-radius:8px;padding:18px 22px;
                box-shadow:0 2px 8px rgba(0,0,0,.07);text-align:center;
                border-top:4px solid ${{KPI_COLORS[i]}};flex:1;min-width:150px;">
      <div style="font-size:12px;color:#888;font-weight:600;
                  text-transform:uppercase;letter-spacing:.4px;">${{KPI_LABELS[i]}}</div>
      <div style="font-size:26px;font-weight:700;color:#1a1a2e;margin-top:5px;">${{d[k]}}</div>
    </div>`).join("");

  const insightsGrid = document.getElementById("insightsGrid");
  insightsGrid.innerHTML = d.insights.map(item => `
    <article class="insight-card">
      <div class="insight-title-row">
        <div class="insight-title">${{escapeHtml(item.title)}}</div>
        <span class="priority ${{escapeHtml(item.priority).toLowerCase()}}">
          ${{escapeHtml(item.priority)}}
        </span>
      </div>
      <div class="insight-label">Evidence</div>
      <div class="insight-text">${{escapeHtml(item.evidence)}}</div>
      <div class="insight-label">Action</div>
      <div class="insight-text">${{escapeHtml(item.action)}}</div>
    </article>`).join("");

  // Charts
  Plotly.react("chartRegion",      JSON.parse(d.region).data,      JSON.parse(d.region).layout,      {{responsive:true}});
  Plotly.react("chartMonthly",     JSON.parse(d.monthly).data,     JSON.parse(d.monthly).layout,     {{responsive:true}});
  Plotly.react("chartCategory",    JSON.parse(d.category).data,    JSON.parse(d.category).layout,    {{responsive:true}});
  Plotly.react("chartTopProducts", JSON.parse(d.top_products).data, JSON.parse(d.top_products).layout, {{responsive:true}});

  document.getElementById("filterLabel").textContent =
    quarter === "Full Year" ? "Showing all 2024 data" : `Showing ${{quarter}} 2024 only`;
}}

// Initialise on load
applyFilter("Full Year");
</script>
</body>
</html>"""
    return html


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ISYS 573 Sales Dashboard")
    parser.add_argument("--data",   default=str(DATA_PATH), help="Path to sales CSV")
    parser.add_argument("--output", default="dashboard.html", help="Output HTML file")
    args = parser.parse_args()

    print(f"Loading data from {args.data} …")
    df = load_data(Path(args.data))
    print(f"  {len(df)} rows · {df['region'].nunique()} regions · "
          f"{df['category'].nunique()} categories")

    print("Building dashboard …")
    html = build_html(df)

    out = Path(args.output)
    out.write_text(html, encoding="utf-8")
    print(f"✅  Dashboard saved → {out.resolve()}")
    print(f"   Open in browser: file://{out.resolve()}")


if __name__ == "__main__":
    main()
