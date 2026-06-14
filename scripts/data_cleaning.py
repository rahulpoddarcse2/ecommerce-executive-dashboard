"""
data_cleaning.py
----------------
Python data-cleaning module:
  • Missing value imputation
  • Outlier detection & capping (IQR method)
  • Feature engineering (revenue, CLV components, time features)
  • Data type standardisation
"""

import pandas as pd
import numpy as np
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
RAW_PATH     = "/home/claude/ecommerce_dashboard/data/raw/raw_ecommerce_data.csv"
CLEANED_PATH = "/home/claude/ecommerce_dashboard/data/cleaned/cleaned_ecommerce_data.csv"

# ══════════════════════════════════════════════════════════════════════════════
class DataCleaner:
    """End-to-end cleaning pipeline for raw e-commerce transactional data."""

    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath)
        print(f"📥 Loaded {len(self.df):,} rows × {self.df.shape[1]} cols")
        self._original_shape = self.df.shape

    # ── 1. Basic type fixes ───────────────────────────────────────────────────
    def fix_dtypes(self):
        self.df["order_date"] = pd.to_datetime(self.df["order_date"])
        self.df["quantity"]   = pd.to_numeric(self.df["quantity"],  errors="coerce")
        self.df["unit_price"] = pd.to_numeric(self.df["unit_price"], errors="coerce")
        self.df["discount"]   = pd.to_numeric(self.df["discount"],  errors="coerce")
        print("  ✔ Data types fixed")
        return self

    # ── 2. Missing value imputation ───────────────────────────────────────────
    def handle_missing(self):
        before = self.df.isnull().sum().sum()

        # Numeric: median imputation per category
        for col in ["unit_price", "quantity", "discount", "shipping_cost"]:
            self.df[col] = self.df.groupby("product_category")[col].transform(
                lambda x: x.fillna(x.median())
            )
            self.df[col] = self.df[col].fillna(self.df[col].median())

        # Categorical: mode imputation
        for col in ["customer_age", "customer_gender"]:
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

        after = self.df.isnull().sum().sum()
        print(f"  ✔ Missing values: {before} → {after}")
        return self

    # ── 3. Outlier detection & capping (IQR) ──────────────────────────────────
    def handle_outliers(self):
        outlier_cols = ["unit_price", "quantity"]
        total_capped = 0
        for col in outlier_cols:
            Q1, Q3 = self.df[col].quantile([0.25, 0.75])
            IQR    = Q3 - Q1
            lower  = Q1 - 1.5 * IQR
            upper  = Q3 + 1.5 * IQR
            n_out  = ((self.df[col] < lower) | (self.df[col] > upper)).sum()
            self.df[col] = self.df[col].clip(lower, upper)
            total_capped += n_out
            print(f"  ✔ Outliers capped in '{col}': {n_out} values (bounds [{lower:.1f}, {upper:.1f}])")
        return self

    # ── 4. Feature engineering ────────────────────────────────────────────────
    def engineer_features(self):
        # Revenue
        self.df["revenue"] = (
            self.df["unit_price"] * self.df["quantity"] * (1 - self.df["discount"])
        ).round(2)
        self.df["gross_revenue"] = (self.df["unit_price"] * self.df["quantity"]).round(2)
        self.df["discount_amount"] = (self.df["gross_revenue"] - self.df["revenue"]).round(2)
        self.df["net_revenue"]  = (self.df["revenue"] - self.df["shipping_cost"]).round(2)
        self.df["profit_margin"] = (self.df["net_revenue"] / self.df["gross_revenue"].replace(0, np.nan)).round(4)

        # Time features
        self.df["year"]    = self.df["order_date"].dt.year
        self.df["month"]   = self.df["order_date"].dt.month
        self.df["month_name"] = self.df["order_date"].dt.strftime("%b")
        self.df["quarter"] = self.df["order_date"].dt.quarter
        self.df["week"]    = self.df["order_date"].dt.isocalendar().week.astype(int)
        self.df["day_of_week"] = self.df["order_date"].dt.day_name()
        self.df["is_weekend"] = self.df["order_date"].dt.dayofweek >= 5

        # Delivery flag
        self.df["is_delivered"] = (self.df["order_status"] == "Delivered").astype(int)
        self.df["is_returned"]  = (self.df["order_status"] == "Returned").astype(int)

        print(f"  ✔ Feature engineering complete — {self.df.shape[1]} total columns")
        return self

    # ── 5. Save ───────────────────────────────────────────────────────────────
    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.df.to_csv(path, index=False)
        print(f"\n✅ Cleaned data saved → {path}")
        print(f"   Shape: {self._original_shape} → {self.df.shape}")
        return self.df


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cleaner = DataCleaner(RAW_PATH)
    df_clean = (
        cleaner
        .fix_dtypes()
        .handle_missing()
        .handle_outliers()
        .engineer_features()
        .save(CLEANED_PATH)
    )
    print(f"\n📊 Sample:\n{df_clean[['order_id','customer_id','revenue','quarter','month_name']].head()}")
