# AGENTS.md
## Project Overview
Retail sales dashboard that reads `data/sales.csv` and generates
a self-contained interactive HTML report (`dashboard.html`) using
Pandas + Plotly. No web server required — output is a single file.

## Tech Stack
- Python 3.11+
- pandas >= 2.0
- plotly >= 5.18
- pytest >= 7.0

## Build & Test
```bash
# Install dependencies
pip install -r requirements.txt

# Generate dashboard
python dashboard.py

# Run tests
pytest tests/ -v

# Custom output path
python dashboard.py --output report.html
```

## Project Structure
```
isys573-sales-dashboard/
├── data/
│   └── sales.csv          # Source data — NEVER modify
├── tests/
│   └── test_dashboard.py  # pytest test suite
├── dashboard.py           # Main script — entry point
├── requirements.txt
├── AGENTS.md              # This file
└── .github/
    ├── copilot-instructions.md
    └── agents/
        └── test-agent.md  # Custom QA agent
```

## Code Standards
- Follow PEP 8 strictly
- Type hints required on all function signatures
- Docstrings required on all public functions
- Use `pathlib.Path` for all file paths — never `os.path`
- All monetary values formatted as `$x,xxx` (no decimals in display)

## Data Contract — data/sales.csv
Required columns: `date`, `region`, `category`, `product`,
`units_sold`, `unit_price`, `discount_pct`, `revenue`, `channel`, `sales_rep`
- `date`: ISO format YYYY-MM-DD
- `revenue`: float, pre-calculated (units × price × (1 - discount))
- **NEVER modify files in data/ — treat as read-only source of truth**

## Testing Requirements
- All new filtering logic must have pytest tests
- Tests live in `tests/test_dashboard.py`
- Tests must pass before any PR is opened
- Run `pytest tests/ -v` to verify

## Boundaries
- ALWAYS: Run pytest before opening a PR
- ALWAYS: Preserve the quarter-filter dropdown functionality
- ASK FIRST: Adding new data sources or external API calls
- NEVER: Modify data/sales.csv
- NEVER: Add a web server (Flask, FastAPI, Streamlit) — output must stay HTML
- NEVER: Use deprecated Plotly APIs (use `plotly.express` or `plotly.graph_objects`)
