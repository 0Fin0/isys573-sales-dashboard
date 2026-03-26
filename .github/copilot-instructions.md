# GitHub Copilot Instructions
## Project
ISYS 573 Retail Sales Dashboard — Python · Pandas · Plotly · pytest

## Coding Conventions
- Python 3.11+ syntax and type hints on every function
- PEP 8 line length: 88 characters (Black-compatible)
- Use `pathlib.Path` — never `os.path` or raw strings for paths
- Docstrings: Google style, required on all public functions/classes
- Prefer `pd.DataFrame` method chaining over intermediate variables
- Use `plotly.express` for new charts; `plotly.graph_objects` for customization

## Data Rules
- `data/sales.csv` is read-only — never write to it
- Always validate required columns after loading (see `load_data()`)
- Date parsing: always use `parse_dates=["date"]` in `pd.read_csv`
- Revenue is pre-calculated — never recompute from units × price in display logic

## Testing
- All new functions that filter or transform data need a pytest test
- Tests go in `tests/test_dashboard.py`
- Use `pd.testing.assert_frame_equal` for DataFrame comparisons
- Run: `pytest tests/ -v` — must pass before any commit

## HTML Output Rules
- Dashboard must remain a single self-contained HTML file
- Quarter filter dropdown must always be present and functional
- Plotly charts embedded as JSON in `<script>` tags — no external CDN data
- KPI cards: Total Revenue, Transactions, Avg Transaction, Top Region

## What NOT to do
- Do not add Flask, FastAPI, or Streamlit — this is not a web app
- Do not use `os.path` — use `pathlib.Path`
- Do not skip tests when adding new filtering logic
- Do not hardcode quarter names — derive from data
