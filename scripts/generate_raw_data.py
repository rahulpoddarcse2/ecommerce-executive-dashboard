"""
generate_raw_data.py
--------------------
Simulates raw e-commerce transactional data with realistic noise,
missing values, and outliers — mimicking a real ingestion scenario.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
N_ORDERS      = 5000
N_CUSTOMERS   = 800
START_DATE    = datetime(2024, 1, 1)
END_DATE      = datetime(2024, 12, 31)

CATEGORIES    = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports", "Beauty"]
SUBCATEGORIES = {
    "Electronics":    ["Smartphones", "Laptops", "Headphones", "Tablets", "Cameras"],
    "Clothing":       ["Men's Wear", "Women's Wear", "Kids", "Footwear", "Accessories"],
    "Home & Kitchen": ["Cookware", "Furniture", "Decor", "Appliances", "Bedding"],
    "Books":          ["Fiction", "Non-Fiction", "Academic", "Comics", "Self-Help"],
    "Sports":         ["Fitness", "Cricket", "Football", "Swimming", "Cycling"],
    "Beauty":         ["Skincare", "Haircare", "Makeup", "Fragrances", "Tools"],
}
CITIES = [
    ("Mumbai",    "Maharashtra", "West"),
    ("Delhi",     "Delhi",       "North"),
    ("Bengaluru", "Karnataka",   "South"),
    ("Hyderabad", "Telangana",   "South"),
    ("Chennai",   "Tamil Nadu",  "South"),
    ("Kolkata",   "West Bengal", "East"),
    ("Pune",      "Maharashtra", "West"),
    ("Ahmedabad", "Gujarat",     "West"),
    ("Jaipur",    "Rajasthan",   "North"),
    ("Lucknow",   "Uttar Pradesh","North"),
]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery", "Wallet"]
SHIPPING_MODES  = ["Standard", "Express", "Same Day", "Economy"]
STATUS_LIST     = ["Delivered", "Delivered", "Delivered", "Returned", "Cancelled", "Pending"]

# ── Generate ──────────────────────────────────────────────────────────────────
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

customer_ids   = [f"CUST{str(i).zfill(4)}" for i in range(1, N_CUSTOMERS + 1)]
customer_names = [f"Customer_{i}" for i in range(1, N_CUSTOMERS + 1)]
customer_map   = dict(zip(customer_ids, customer_names))

rows = []
for i in range(1, N_ORDERS + 1):
    cat     = random.choice(CATEGORIES)
    subcat  = random.choice(SUBCATEGORIES[cat])
    city, state, region = random.choice(CITIES)
    cust_id = random.choice(customer_ids)
    order_date = random_date(START_DATE, END_DATE)
    qty     = random.randint(1, 5)
    price   = round(random.uniform(50, 50000), 2)
    discount= round(random.uniform(0, 0.4), 2)
    shipping= round(random.uniform(0, 500), 2)

    # Inject noise
    if random.random() < 0.04:   price    = None          # missing price
    if random.random() < 0.03:   qty      = None          # missing qty
    if random.random() < 0.02:   discount = None          # missing discount
    if random.random() < 0.015:  price    = round(random.uniform(500000, 2000000), 2)  # price outlier
    if random.random() < 0.01:   qty      = random.randint(500, 1000)                  # qty outlier

    rows.append({
        "order_id":       f"ORD{str(i).zfill(5)}",
        "customer_id":    cust_id,
        "customer_name":  customer_map[cust_id],
        "order_date":     order_date.strftime("%Y-%m-%d"),
        "product_category": cat,
        "product_subcategory": subcat,
        "product_name":   f"{subcat} Item {random.randint(1,50)}",
        "quantity":       qty,
        "unit_price":     price,
        "discount":       discount,
        "shipping_cost":  shipping,
        "payment_method": random.choice(PAYMENT_METHODS),
        "shipping_mode":  random.choice(SHIPPING_MODES),
        "city":           city,
        "state":          state,
        "region":         region,
        "order_status":   random.choice(STATUS_LIST),
        "customer_age":   random.randint(18, 65) if random.random() > 0.02 else None,
        "customer_gender":random.choice(["Male", "Female", "Other"]) if random.random() > 0.01 else None,
    })

df = pd.DataFrame(rows)
out = "/home/claude/ecommerce_dashboard/data/raw/raw_ecommerce_data.csv"
df.to_csv(out, index=False)
print(f"✅ Raw data generated: {len(df)} rows → {out}")
print(f"   Missing values:\n{df.isnull().sum()[df.isnull().sum()>0]}")
