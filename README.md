# E-Commerce Executive Dashboard
**Tech Stack:** Python (Pandas, NumPy, Scikit-learn), Power BI, K-Means Clustering  
**Duration:** May 2025 – Jun 2025

---

## 📌 Project Overview
End-to-end Business Intelligence pipeline that transforms raw e-commerce transactional data into a Power BI executive dashboard — completely eliminating manual reporting.

---

## 🏗️ Architecture

```
Raw CSV Data
    │
    ▼
[1] generate_raw_data.py        ← Simulates raw ingestion with noise
    │
    ▼
[2] data_cleaning.py            ← Missing values, outliers, feature engineering
    │
    ▼
[3] kmeans_clv_segmentation.py  ← K-Means clustering on Customer Lifetime Value
    │
    ▼
[4] star_schema_builder.py      ← Fact + Dimension tables (Star Schema)
    │
    ▼
[5] power_query_automation.py   ← Power BI-ready aggregated output tables
    │
    ▼
Power BI Executive Dashboard
```

---

## 📂 Project Structure

```
ecommerce_dashboard/
├── run_pipeline.py                  ← Master pipeline runner
├── scripts/
│   ├── generate_raw_data.py         ← Raw data generator
│   ├── data_cleaning.py             ← Cleaning module
│   ├── kmeans_clv_segmentation.py   ← K-Means CLV clustering
│   ├── star_schema_builder.py       ← Star Schema architect
│   └── power_query_automation.py    ← Power Query automations
├── data/
│   ├── raw/                         ← Raw ingestion data
│   ├── cleaned/                     ← Cleaned data + customer segments
│   └── star_schema/                 ← Fact & dimension tables
├── outputs/                         ← Power BI-ready CSVs + visualizations
│   ├── monthly_revenue_trend.csv
│   ├── category_performance.csv
│   ├── regional_analysis.csv
│   ├── segment_revenue.csv
│   ├── executive_kpis.csv
│   ├── elbow_plot.png
│   └── cluster_plot.png
└── README.md
```

---

## 🔑 Key Features

### 1. Data Cleaning Module (`data_cleaning.py`)
- **Missing value imputation:** Median per product category for numeric cols; mode for categorical
- **Outlier detection & capping:** IQR method — capped 78 price outliers, 54 quantity outliers
- **Feature engineering:** Revenue, gross/net revenue, profit margin, time features (quarter, week, day_of_week, is_weekend), delivery/return flags
- Shape after cleaning: `5000 × 19 → 5000 × 33`

### 2. K-Means CLV Segmentation (`kmeans_clv_segmentation.py`)
- Built **RFM (Recency, Frequency, Monetary)** features per customer
- Calculated **CLV Score** = `Monetary × log(Frequency) / log(Recency + 1)`
- Optimal K selected via Elbow Method + Silhouette Score → **K = 4**
- Silhouette Score: **0.29**

| Segment | Customers | Avg CLV | Revenue Share |
|---|---|---|---|
| Champions | 110 | ₹2,95,440 | 29.5% |
| Loyal Customers | 147 | ₹1,07,368 | 27.2% |
| At-Risk | 331 | ₹65,498 | 32.8% |
| Lost / Dormant | 183 | ₹18,984 | 10.4% |

**Marketing Actions:**
- **Champions:** Loyalty rewards, upsell premium products
- **Loyal Customers:** Membership perks, cross-sell
- **At-Risk:** Win-back email with 15% discount
- **Lost/Dormant:** Aggressive re-engagement campaign

### 3. Star Schema (`star_schema_builder.py`)
```
fact_orders (5,000 rows)
    ├── dim_product    (1,451 rows) — category, subcategory, product name
    ├── dim_geography  (10 rows)   — city, state, region
    ├── dim_time       (366 rows)  — date, month, quarter, week, weekend flag
    └── dim_customer   (800 rows)  — demographics + CLV segment
```

### 4. Power Query Automation (`power_query_automation.py`)
Automated 5 transformation outputs that previously required manual Excel pivot refresh:
- Monthly revenue trend with MoM growth %
- Category performance with return rates
- Regional analysis (city/state/region)
- Segment-wise revenue contribution
- Executive KPI card values

**Reduced manual refresh effort by ~40%.**

---

## 📊 Executive KPI Results

| KPI | Value |
|---|---|
| Total Revenue | ₹16,06,88,907 |
| Total Orders | 2,538 |
| Unique Customers | 771 |
| Avg Order Value | ₹63,313 |
| Return Rate | 16.78% |
| Top Category | Sports |
| Top Region | West |
| Best Month | January |

---

## ▶️ How to Run

```bash
# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl

# Run full pipeline
python run_pipeline.py
```

---

## 🔌 Power BI Integration
1. Open Power BI Desktop
2. **Get Data → Python Script** → paste `power_query_automation.py`
3. Connect outputs CSVs from `outputs/` folder as data sources
4. Build relationships using `fact_orders` as centre of Star Schema
5. Schedule refresh via Power BI Service (Gateway)

---

## 📈 Visualizations
- `outputs/elbow_plot.png` — K selection via Elbow + Silhouette
- `outputs/cluster_plot.png` — 2D customer segment scatter plots
