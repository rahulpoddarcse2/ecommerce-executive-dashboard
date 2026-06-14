"""
run_pipeline.py
---------------
Master script — runs the full end-to-end BI pipeline in order:
  1. generate_raw_data.py         → raw CSV
  2. data_cleaning.py             → cleaned CSV
  3. kmeans_clv_segmentation.py   → customer segments + plots
  4. star_schema_builder.py       → fact & dimension tables
  5. power_query_automation.py    → Power BI-ready output tables
"""

import subprocess, sys, time, os

SCRIPTS = [
    ("1/5  Generating raw e-commerce data …",     "scripts/generate_raw_data.py"),
    ("2/5  Running data-cleaning module …",         "scripts/data_cleaning.py"),
    ("3/5  K-Means CLV segmentation …",             "scripts/kmeans_clv_segmentation.py"),
    ("4/5  Building Star Schema …",                 "scripts/star_schema_builder.py"),
    ("5/5  Power Query automations …",              "scripts/power_query_automation.py"),
]

BASE = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("  E-COMMERCE EXECUTIVE DASHBOARD — BI PIPELINE")
print("=" * 60)
t0 = time.time()

for label, script in SCRIPTS:
    print(f"\n🔄 {label}")
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, script)],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"❌ FAILED: {script}")
        sys.exit(1)

elapsed = time.time() - t0
print(f"\n{'='*60}")
print(f"  ✅ Pipeline complete in {elapsed:.1f}s")
print(f"  📁 Outputs → ecommerce_dashboard/outputs/")
print(f"  📁 Data    → ecommerce_dashboard/data/")
print("=" * 60)
