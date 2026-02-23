"""
Lab 12.3: Data Analysis
=======================

Analyze a CSV dataset with pandas and create visualizations.
Practice DataFrame operations, grouping, and plotting.

Install: pip install pandas matplotlib
"""

import pandas as pd
from io import StringIO


# ============================================================
# Sample Dataset (embedded CSV)
# ============================================================

SALES_CSV = """\
date,product,category,quantity,unit_price,region
2024-01-05,Widget A,Electronics,10,29.99,North
2024-01-05,Widget B,Electronics,5,49.99,South
2024-01-08,Gadget X,Home,20,14.99,North
2024-01-12,Widget A,Electronics,8,29.99,East
2024-01-12,Gizmo Z,Home,15,9.99,West
2024-01-15,Widget B,Electronics,12,49.99,North
2024-01-18,Gadget X,Home,25,14.99,South
2024-01-22,Widget A,Electronics,6,29.99,West
2024-01-25,Gizmo Z,Home,30,9.99,North
2024-01-28,Widget B,Electronics,3,49.99,East
2024-02-01,Widget A,Electronics,15,29.99,North
2024-02-05,Gadget X,Home,18,14.99,East
2024-02-08,Gizmo Z,Home,22,9.99,South
2024-02-12,Widget B,Electronics,9,49.99,West
2024-02-15,Widget A,Electronics,11,29.99,South
2024-02-18,Gadget X,Home,14,14.99,North
2024-02-22,Widget B,Electronics,7,49.99,North
2024-02-25,Gizmo Z,Home,35,9.99,East
"""


def load_data() -> pd.DataFrame:
    """
    Load the CSV data into a DataFrame.

    - Parse the 'date' column as datetime
    - Add a 'revenue' column (quantity * unit_price)
    - Return the DataFrame
    """
    # TODO: Implement
    pass


def top_products(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """
    Return the top N products by total revenue.

    Return a DataFrame with columns: product, total_revenue
    Sorted by total_revenue descending.
    """
    # TODO: Implement using groupby and sort_values
    pass


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize sales by region.

    Return a DataFrame with columns: region, total_revenue, order_count, avg_order_value
    Sorted by total_revenue descending.
    Round avg_order_value to 2 decimal places.
    """
    # TODO: Implement
    pass


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate monthly revenue trend.

    Return a DataFrame with columns: month, revenue
    'month' should be a Period (e.g., "2024-01") using df['date'].dt.to_period('M')
    """
    # TODO: Implement
    pass


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate revenue share by category.

    Return a DataFrame with columns: category, revenue, percentage
    'percentage' is the category's share of total revenue, rounded to 1 decimal.
    """
    # TODO: Implement
    pass


def high_value_transactions(df: pd.DataFrame, threshold: float = 200) -> pd.DataFrame:
    """
    Return transactions where revenue exceeds the threshold.
    Sort by revenue descending.
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_load():
    df = load_data()
    assert "revenue" in df.columns
    assert df["date"].dtype == "datetime64[ns]"
    assert len(df) == 18
    print(f"✓ load_data: {len(df)} rows, columns: {list(df.columns)}")
    return df


def test_top_products(df):
    result = top_products(df)
    assert len(result) == 3
    assert result.iloc[0]["total_revenue"] >= result.iloc[1]["total_revenue"]
    print(f"✓ top_products:\n{result.to_string(index=False)}")


def test_by_region(df):
    result = sales_by_region(df)
    assert "region" in result.columns
    assert "avg_order_value" in result.columns
    assert len(result) == 4
    print(f"✓ sales_by_region:\n{result.to_string(index=False)}")


def test_monthly(df):
    result = monthly_trend(df)
    assert len(result) == 2  # Jan and Feb
    print(f"✓ monthly_trend:\n{result.to_string(index=False)}")


def test_category(df):
    result = category_breakdown(df)
    total_pct = result["percentage"].sum()
    assert abs(total_pct - 100.0) < 0.5, f"Percentages should sum to ~100, got {total_pct}"
    print(f"✓ category_breakdown:\n{result.to_string(index=False)}")


def test_high_value(df):
    result = high_value_transactions(df)
    assert all(result["revenue"] > 200)
    print(f"✓ high_value_transactions: {len(result)} transactions above $200")


if __name__ == "__main__":
    df = test_load()
    test_top_products(df)
    test_by_region(df)
    test_monthly(df)
    test_category(df)
    test_high_value(df)
    print("\nAll tests passed! ✓")
