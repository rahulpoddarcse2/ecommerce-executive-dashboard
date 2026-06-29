<div align="center">

# 📊 E-Commerce Executive Dashboard

**End-to-end BI pipeline with Python, ML Segmentation & Power BI**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

![GitHub last commit](https://img.shields.io/github/last-commit/rahulpoddarcse2/ecommerce-executive-dashboard?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/rahulpoddarcse2/ecommerce-executive-dashboard?style=flat-square)

</div>

---

## 📌 Project Overview

A **complete Business Intelligence pipeline** built from raw e-commerce transaction data to an executive-level Power BI dashboard. Includes customer segmentation using **K-Means CLV clustering** and a **Star Schema** data model for optimized BI performance.

> **Business Problem:** E-commerce companies need to identify their high-value customers, understand sales trends, and make data-driven decisions. This project delivers those insights through an automated pipeline — from raw CSV to interactive Power BI dashboard.

---

## 🏗️ Pipeline Architecture

```
Raw CSV Data
     │
     ▼
┌─────────────────┐
│  Data Cleaning  │  → Python (Pandas, NumPy)
│  & Validation   │    Handle nulls, duplicates,
└────────┬────────┘    type casting
         │
         ▼
┌─────────────────┐
│  Feature        │  → RFM Analysis
│  Engineering    │    Recency, Frequency, Monetary
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ML Clustering  │  → K-Means (Scikit-learn)
│  CLV Segments   │    Customer Lifetime Value
└────────┬────────┘    segmentation into tiers
         │
         ▼
┌─────────────────┐
│  Star Schema    │  → Fact & Dimension tables
│  Data Modeling  │    Optimized for Power BI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Power BI       │  → Executive Dashboard
│  Dashboard      │    KPIs, trends, segments
└─────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **K-Means Clustering** | Segments customers into CLV tiers (High / Mid / Low) |
| 📐 **Star Schema** | Fact + Dimension tables for optimized Power BI queries |
| 🔁 **Full ETL Pipeline** | Raw CSV → cleaned → modeled → visualized |
| 📈 **RFM Analysis** | Recency, Frequency, Monetary scoring per customer |
| 📊 **Executive KPIs** | Revenue trends, top products, regional analysis |
| 🐍 **Pure Python** | No paid tools in pipeline — fully reproducible |

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Data Processing | Python, Pandas, NumPy | ETL & feature engineering |
| ML Segmentation | Scikit-learn (K-Means) | Customer CLV clustering |
| Data Modeling | Python | Star schema construction |
| Visualization | Power BI Desktop | Executive dashboard |
| Version Control | Git + GitHub | Code management |

---

## 📊 Dashboard Insights

The final Power BI dashboard delivers:

- **Revenue KPIs** — total revenue, MoM growth, average order value
- **Customer Segments** — CLV tiers with segment-wise revenue share
- **Product Analysis** — top 10 products by revenue & volume
- **Regional Breakdown** — sales distribution by geography
- **Time Series** — monthly/quarterly trend analysis

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### Run the Pipeline
```bash
# Clone the repo
git clone https://github.com/rahulpoddarcse2/ecommerce-executive-dashboard.git
cd ecommerce-executive-dashboard

# Run ETL + clustering
python src/etl_pipeline.py

# Open the notebook for step-by-step walkthrough
jupyter notebook notebooks/analysis.ipynb
```

Then open `dashboard/ecommerce_dashboard.pbix` in Power BI Desktop.

---

## 📁 Project Structure

```
ecommerce-executive-dashboard/
├── data/
│   ├── raw/                  # Raw transaction CSV
│   └── processed/            # Cleaned & modeled data
├── src/
│   ├── etl_pipeline.py       # Main ETL script
│   ├── clustering.py         # K-Means CLV segmentation
│   └── star_schema.py        # Data modeling
├── notebooks/
│   └── analysis.ipynb        # Step-by-step EDA
├── dashboard/
│   └── ecommerce_dashboard.pbix  # Power BI file
└── README.md
```

---

## 📊 Results

| Customer Segment | % of Customers | Revenue Contribution |
|-----------------|---------------|---------------------|
| 🥇 High CLV | ~15% | ~60% of revenue |
| 🥈 Mid CLV | ~35% | ~30% of revenue |
| 🥉 Low CLV | ~50% | ~10% of revenue |

> *Typical Pareto distribution — top 15% of customers drive 60% of revenue*

---

<div align="center">

**⭐ If this project helped you, consider giving it a star!**

[![LinkedIn](https://img.shields.io/badge/Connect-Rahul_Poddar-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/rahulpoddar-2eab5)

</div>
