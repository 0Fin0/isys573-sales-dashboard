# GitHub Copilot Instructions

## Project

ISYS 573 Retail Sales Dashboard - Python, Pandas, Plotly, pytest.

## Coding Conventions

- Python 3.11+ syntax and type hints on every function.
- PEP 8 line length: 88 characters, Black-compatible.
- Use `pathlib.Path`; do not use `os.path` or raw strings for paths.
- Docstrings are required on all public functions and classes.
- Prefer `pd.DataFrame` method chaining over unnecessary intermediate values.
- Use `plotly.express` for new charts and `plotly.graph_objects` for
  customization.

## Data Rules

- `data/sales.csv` is read-only; never write to it.
- Always validate required columns after loading. See `load_data()`.
- Date parsing should use `parse_dates=["date"]` in `pd.read_csv`.
- Revenue is pre-calculated. Do not recompute it from units and price in display
  logic.

## Testing

- All new functions that filter or transform data need pytest tests.
- Tests go in `tests/test_dashboard.py`.
- Use `pd.testing.assert_frame_equal` for DataFrame comparisons.
- Run `pytest tests/ -v`; tests must pass before any commit.

## HTML Output Rules

- Dashboard must remain a single self-contained HTML file.
- Quarter filter dropdown must always be present and functional.
- Plotly charts are embedded as JSON in `<script>` tags; do not use external CDN
  data.
- KPI cards remain: Total Revenue, Transactions, Avg Transaction, Top Region.

## Responsible AI Feature Rules

- Do not add API keys, tokens, or external AI service calls.
- Keep AI-labeled dashboard insights grounded in `data/sales.csv`.
- Do not invent customers, forecasts, causes, or unsupported business claims.
- Any insight text must include evidence from existing metrics or transparent
  business rules.
- Add empty-state handling for missing or filtered data.
- Use cautious business language and require human review before action.

## What Not To Do

- Do not add Flask, FastAPI, or Streamlit. This is not a web app.
- Do not use `os.path`; use `pathlib.Path`.
- Do not skip tests when adding new filtering logic.
- Do not hardcode quarter names; derive them from data where practical.
