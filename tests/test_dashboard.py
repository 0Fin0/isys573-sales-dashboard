"""
Tests for ISYS 573 Sales Dashboard
===================================
Run: pytest tests/ -v
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from dashboard import load_data, build_region_bar, build_monthly_line, \
                      build_category_pie, build_top_products, \
                      build_sales_risk_insights

DATA_PATH = Path(__file__).parent.parent / "data" / "sales.csv"


@pytest.fixture
def df() -> pd.DataFrame:
    return load_data(DATA_PATH)


class TestLoadData:
    def test_loads_without_error(self, df):
        assert len(df) == 500

    def test_required_columns_present(self, df):
        required = {"date", "region", "category", "product",
                    "units_sold", "unit_price", "revenue", "channel"}
        assert required.issubset(set(df.columns))

    def test_date_parsed_as_datetime(self, df):
        assert pd.api.types.is_datetime64_any_dtype(df["date"])

    def test_quarter_column_added(self, df):
        assert "quarter" in df.columns
        assert set(df["quarter"].unique()).issubset({"Q1", "Q2", "Q3", "Q4"})

    def test_month_column_added(self, df):
        assert "month" in df.columns

    def test_revenue_is_positive(self, df):
        assert (df["revenue"] > 0).all()

    def test_four_regions(self, df):
        assert df["region"].nunique() == 4

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_data(Path("/nonexistent/path.csv"))


class TestRegionChart:
    def test_returns_figure(self, df):
        fig = build_region_bar(df)
        assert fig is not None

    def test_has_four_bars(self, df):
        fig = build_region_bar(df)
        # go.Bar renders all regions in one trace.
        assert len(fig.data[0].y) == 4

    def test_filtered_by_quarter(self, df):
        q1 = df[df["quarter"] == "Q1"]
        fig = build_region_bar(q1)
        # Should only show regions present in Q1
        assert len(fig.data[0].x) <= 4


class TestMonthlyChart:
    def test_returns_figure(self, df):
        fig = build_monthly_line(df)
        assert fig is not None

    def test_has_twelve_months_or_fewer(self, df):
        fig = build_monthly_line(df)
        assert len(fig.data[0].x) <= 12

    def test_revenue_values_are_positive(self, df):
        fig = build_monthly_line(df)
        assert all(v > 0 for v in fig.data[0].y)


class TestCategoryChart:
    def test_returns_figure(self, df):
        fig = build_category_pie(df)
        assert fig is not None

    def test_six_categories(self, df):
        fig = build_category_pie(df)
        assert len(fig.data[0].labels) == 6


class TestTopProducts:
    def test_returns_figure(self, df):
        fig = build_top_products(df)
        assert fig is not None

    def test_default_top_10(self, df):
        fig = build_top_products(df)
        assert len(fig.data[0].y) == 10

    def test_custom_n(self, df):
        fig = build_top_products(df, n=5)
        assert len(fig.data[0].y) == 5

    def test_sorted_ascending_for_horizontal_bar(self, df):
        fig = build_top_products(df)
        revenues = list(fig.data[0].x)
        assert revenues == sorted(revenues)


class TestSalesRiskInsights:
    def test_returns_three_insights_for_full_dataset(self, df):
        insights = build_sales_risk_insights(df)
        assert len(insights) == 3

    def test_each_insight_has_required_fields(self, df):
        insights = build_sales_risk_insights(df)
        required = {"title", "priority", "evidence", "action"}
        for insight in insights:
            assert required.issubset(insight.keys())
            assert insight["priority"] in {"High", "Medium", "Low"}
            assert insight["evidence"]
            assert insight["action"]

    def test_empty_data_returns_review_message(self, df):
        empty = df.iloc[0:0]
        insights = build_sales_risk_insights(empty)
        assert len(insights) == 1
        assert insights[0]["priority"] == "Low"
        assert "no sales records" in insights[0]["evidence"].lower()

    def test_filtered_data_stays_grounded_in_period(self, df):
        q1 = df[df["quarter"] == "Q1"]
        insights = build_sales_risk_insights(q1)
        assert len(insights) == 3
        assert all("$" in insight["evidence"] or "%" in insight["evidence"]
                   for insight in insights)
