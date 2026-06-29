"""
PROJECT: SALES DATA ANALYSIS USING PANDAS
Course Requirement: Week 3 - Working with Real Data
Description: Clean, process, and analyze sales data to generate key business insights.
"""

import os
import pandas as pd


def generate_mock_data(filename="sales_data.csv"):
    """Generates a mock CSV file if it doesn't exist to ensure the script runs seamlessly."""
    import random

    print(f"'{filename}' not found. Generating a sample dataset with 100 rows...")
    data = {
        "Customer_ID": [f"CUST_{random.randint(1000, 1050)}" for _ in range(100)],
        "Product": random.choices(
            ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"], k=100
        ),
        "Region": random.choices(["North", "South", "East", "West"], k=100),
        "Price": random.choices([50000, 1000, 2000, 15000, 3000], k=100),
        "Quantity": random.choices([1, 2, 3, 5], k=100),
    }
    # Mix in a few missing values and duplicates for cleaning demonstration
    df_mock = pd.DataFrame(data)
    df_mock.loc[::15, "Price"] = None  # Insert missing values
    df_mock["Total_Sales"] = df_mock["Price"] * df_mock["Quantity"]

    # Add duplicate rows
    df_mock = pd.concat([df_mock, df_mock.head(3)], ignore_index=True)
    df_mock.to_csv(filename, index=False)
    print(f" Sample data written to {filename}\n")


def load_and_explore_data(filepath):
    """STEP 1 & 2: Load the dataset securely and display structural properties."""
    print("=" * 60)
    print(f" Loading Dataset: {filepath}")
    print("=" * 60)

    df = pd.read_csv(filepath)

    print(f"\n Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f" Columns Present: {df.columns.tolist()}")
    print("\n--- Data Types ---")
    print(df.dtypes)

    return df


def clean_data(df):
    """STEP 3 & 4: Drop duplicates and handle missing values in place safely."""
    print("\n" + "=" * 60)
    print(" DATA CLEANING STAGE")
    print("=" * 60)

    # 1. Handle Duplicate Rows
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    dropped_dupes = initial_rows - len(df)
    print(f" Removed {dropped_dupes} duplicate rows.")

    # 2. Track & Handle Missing Values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # Fill missing values selectively by data type
    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    # Direct column-specific assignments prevent FutureWarnings in modern Pandas
    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[text_cols] = df[text_cols].fillna("Unknown")

    # Recalculate Total_Sales if necessary post-cleaning
    if "Price" in df.columns and "Quantity" in df.columns:
        df["Total_Sales"] = df["Price"] * df["Quantity"]

    print("\n Data cleaned successfully.")
    return df


def perform_analysis(df):
    """STEP 5: Extract analytical metrics and aggregations using vectorization."""
    print("\n" + "=" * 60)
    print(" RUNNING ANALYTICAL METRICS")
    print("=" * 60)

    # Core scalar KPI calculations
    metrics = {
        "total_revenue": df["Total_Sales"].sum(),
        "average_sale": df["Total_Sales"].mean(),
        "highest_sale": df["Total_Sales"].max(),
        "lowest_sale": df["Total_Sales"].min(),
        "total_quantity": df["Quantity"].sum(),
        "average_price": df["Price"].mean(),
        "total_customers": df["Customer_ID"].nunique(),
    }

    # Advanced Dataframe aggregations
    metrics["product_sales"] = df.groupby("Product")["Total_Sales"].sum()
    metrics["region_sales"] = df.groupby("Region")["Total_Sales"].sum()

    metrics["best_product"] = metrics["product_sales"].idxmax()
    metrics["best_product_sales"] = metrics["product_sales"].max()
    metrics["best_region"] = metrics["region_sales"].idxmax()

    return metrics


def generate_report(metrics):
    """STEP 6: Output formatted analytical summary to the console."""
    print("\n" + "=" * 70)
    print("                         SALES ANALYSIS REPORT")
    print("=" * 70)

    print(f"Total Revenue             : ₹{metrics['total_revenue']:,.2f}")
    print(f"Average Sale              : ₹{metrics['average_sale']:,.2f}")
    print(f"Highest Sale              : ₹{metrics['highest_sale']:,.2f}")
    print(f"Lowest Sale               : ₹{metrics['lowest_sale']:,.2f}")
    print(f"Total Quantity Sold       : {metrics['total_quantity']:,}")
    print(f"Average Product Price     : ₹{metrics['average_price']:,.2f}")
    print(f"Total Unique Customers    : {metrics['total_customers']:,}")

    print("\nSales by Product Breakdowns:")
    print("-" * 70)
    for prod, val in metrics["product_sales"].items():
        print(f" • {prod:<15} : ₹{val:,.2f}")

    print("\nSales by Region Breakdowns:")
    print("-" * 70)
    for reg, val in metrics["region_sales"].items():
        print(f" • {reg:<15} : ₹{val:,.2f}")

    print("\n" + "=" * 70)
    print("                                INSIGHTS")
    print("=" * 70)
    print(
        f" Key Takeaway 1: Top performing product is '{metrics['best_product']}' generating ₹{metrics['best_product_sales']:,.2f}."
    )
    print(
        f"Key Takeaway 2: Core regional powerhouse is the '{metrics['best_region']}' zone."
    )
    print(
        f" Performance   : Processed transactions for {metrics['total_customers']} high-value customers."
    )
    print("=" * 70)


def main():
    csv_file = "sales_data.csv"

    # Verify or dynamically generate data asset
    if not os.path.exists(csv_file):
        generate_mock_data(csv_file)

    # Pipeline execution flow
    sales_df = load_and_explore_data(csv_file)
    cleaned_df = clean_data(sales_df)
    analysis_results = perform_analysis(cleaned_df)
    generate_report(analysis_results)


if __name__ == "__main__":
    main()