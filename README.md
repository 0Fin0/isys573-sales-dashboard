# ISYS 573 Sales Dashboard
### AugOps Demo · Generative AI and LLMs for Business · SFSU

An interactive retail sales dashboard built entirely in Python — reads `data/sales.csv`
and generates a single self-contained HTML file with drill-down charts.

This repo is the live demo for **Slide 15: GitHub Copilot 2025 — The Full Agentic Workflow**.
It demonstrates all 5 steps of the AugOps development loop using GitHub Copilot.

---

## Quick Start

```bash
git clone https://github.com/[your-handle]/isys573-sales-dashboard
cd isys573-sales-dashboard
pip install -r requirements.txt
python dashboard.py
open dashboard.html   # macOS
# or: start dashboard.html  (Windows)
```

## What the Dashboard Shows

| Chart | Description |
|-------|-------------|
| Revenue by Region | Bar chart — West / East / South / Midwest |
| Monthly Trend | Line chart — Jan–Dec revenue |
| Category Breakdown | Donut pie — 6 product categories |
| Top 10 Products | Horizontal bar — best sellers by revenue |
| **Quarter Filter** | Dropdown — Full Year / Q1 / Q2 / Q3 / Q4 |

KPI cards show: Total Revenue · Transactions · Avg Transaction · Top Region

## Running Tests

```bash
pytest tests/ -v
```

## The AugOps 5-Step Demo (Slide 15)

| Step | Action |
|------|--------|
| 01 `copilot-instructions.md` | Already committed. Copilot reads it on every task. |
| 02 Agent Mode | Prompt: *"Build the sales dashboard from data/sales.csv with region bar, monthly line, category pie, and top products bar. Output to dashboard.html."* |
| 03 MCP Integration | Create the Issue below using GitHub MCP from chat. |
| 04 Coding Agent | Assign Issue #1 to @copilot. Watch it work. |
| 05 Review & Merge | Review the PR diff, comment `@copilot add a summary stats table`, merge. |

## Pre-Written GitHub Issue — Assign to @copilot

> **Title:** Add sales rep leaderboard section to dashboard
>
> **Description:**
> Add a new section below the existing charts showing a sales rep performance leaderboard.
>
> **Acceptance Criteria:**
> - [ ] Horizontal bar chart showing total revenue per sales rep, sorted descending
> - [ ] Chart respects the quarter filter (updates when dropdown changes)
> - [ ] New `build_rep_leaderboard(df)` function in `dashboard.py`
> - [ ] At least 3 pytest tests for the new function in `tests/test_dashboard.py`
> - [ ] All existing tests still pass
>
> **Notes:**
> - Follow existing code style (type hints, docstrings, `pathlib.Path`)
> - Do not modify `data/sales.csv`
> - Run `pytest tests/ -v` before opening the PR

---

*Dataset: 500 synthetic retail transactions · 2024 · 4 regions · 6 categories · 10 sales reps*
