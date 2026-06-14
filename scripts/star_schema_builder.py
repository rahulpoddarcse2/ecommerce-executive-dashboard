"""
star_schema_builder.py
-----------------------
Architects a Star Schema data model from cleaned data:
  Fact Table  : fact_orders.csv
  Dimensions  : dim_product.csv, dim_geography.csv, dim_time.csv, dim_customer.csv
"""

import pandas as pd
import numpy as np
import os

CLEANED_PATH = "/home/claude/ecommerce_dashboard/data/cleaned/cleaned_ecommerce_data.csv"
SEGMENTS_PATH= "/home/claude/ecommerce_dashboard/data/cleaned/customer_segments.csv"
STAR_DIR     = "/home/claude/ecommerce_dashboard/data/star_schema/"
os.makedirs(STAR_DIR, exist_ok=True)

df  = pd.read_csv(CLEANED_PATH, parse_dates=["order_date"])
seg = pd.read_csv(SEGMENTS_PATH)[["customer_id","segment","clv_score","recency","frequency","monetary"]]

# ── Dim: Product ──────────────────────────────────────────────────────────────
dim_product = (
    df[["product_name","product_category","product_subcategory"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_product.insert(0, "product_key", range(1, len(dim_product)+1))
df = df.merge(dim_product, on=["product_name","product_category","product_subcategory"], how="left")

# ── Dim: Geography ────────────────────────────────────────────────────────────
dim_geography = (
    df[["city","state","region"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_geography.insert(0, "geo_key", range(1, len(dim_geography)+1))
df = df.merge(dim_geography, on=["city","state","region"], how="left")

# ── Dim: Time ─────────────────────────────────────────────────────────────────
dim_time = (
    df[["order_date","year","month","month_name","quarter","week","day_of_week","is_weekend"]]
    .drop_duplicates(subset=["order_date"])
    .reset_index(drop=True)
    .sort_values("order_date")
)
dim_time.insert(0, "date_key", dim_time["order_date"].dt.strftime("%Y%m%d").astype(int))
df = df.merge(dim_time[["order_date","date_key"]], on="order_date", how="left")

# ── Dim: Customer ─────────────────────────────────────────────────────────────
dim_customer = (
    df[["customer_id","customer_name","customer_age","customer_gender"]]
    .drop_duplicates(subset=["customer_id"])
    .reset_index(drop=True)
)
dim_customer = dim_customer.merge(seg, on="customer_id", how="left")
dim_customer["segment"] = dim_customer["segment"].fillna("New Customer")

# ── Fact Table ────────────────────────────────────────────────────────────────
FACT_COLS = [
    "order_id", "customer_id", "product_key", "geo_key", "date_key",
    "quantity", "unit_price", "discount", "shipping_cost",
    "gross_revenue", "discount_amount", "revenue", "net_revenue",
    "profit_margin", "is_delivered", "is_returned",
    "payment_method", "shipping_mode", "order_status",
]
fact_orders = df[[c for c in FACT_COLS if c in df.columns]].copy()

# ── Save ──────────────────────────────────────────────────────────────────────
tables = {
    "fact_orders":    fact_orders,
    "dim_product":    dim_product,
    "dim_geography":  dim_geography,
    "dim_time":       dim_time,
    "dim_customer":   dim_customer,
}
for name, tbl in tables.items():
    path = f"{STAR_DIR}{name}.csv"
    tbl.to_csv(path, index=False)
    print(f"  💾 {name:20s} → {tbl.shape[0]:,} rows × {tbl.shape[1]} cols  [{path}]")

print(f"\n✅ Star Schema built in {STAR_DIR}")
print("""
  ┌─────────────────────────────────────┐
  │           STAR SCHEMA               │
  │                                     │
  │  dim_product   ──┐                  │
  │  dim_geography ──┤                  │
  │  dim_time      ──┼──► fact_orders   │
  │  dim_customer  ──┘                  │
  └─────────────────────────────────────┘
""")
