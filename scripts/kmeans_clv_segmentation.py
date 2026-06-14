"""
kmeans_clv_segmentation.py
--------------------------
Segments customers by Customer Lifetime Value (CLV) using K-Means Clustering.
Outputs:
  • customer_segments.csv  – per-customer cluster labels + RFM metrics
  • segment_summary.csv    – aggregate stats per segment
  • elbow_plot.png         – optimal K selection
  • cluster_plot.png       – 2-D cluster scatter
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings, os
warnings.filterwarnings("ignore")

CLEANED_PATH  = "/home/claude/ecommerce_dashboard/data/cleaned/cleaned_ecommerce_data.csv"
OUTPUT_DIR    = "/home/claude/ecommerce_dashboard/data/cleaned/"
MODELS_DIR    = "/home/claude/ecommerce_dashboard/models/"
PLOTS_DIR     = "/home/claude/ecommerce_dashboard/outputs/"
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR,  exist_ok=True)

# ── 1. Load & filter delivered orders ─────────────────────────────────────────
df = pd.read_csv(CLEANED_PATH, parse_dates=["order_date"])
df = df[df["order_status"] == "Delivered"].copy()
print(f"📥 Delivered orders: {len(df):,}")

# ── 2. Build RFM + CLV features per customer ──────────────────────────────────
snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg(
    recency   = ("order_date",  lambda x: (snapshot_date - x.max()).days),
    frequency = ("order_id",    "nunique"),
    monetary  = ("revenue",     "sum"),
    avg_order_value  = ("revenue", "mean"),
    total_quantity   = ("quantity", "sum"),
    unique_categories= ("product_category", "nunique"),
    avg_discount     = ("discount", "mean"),
    last_order_date  = ("order_date", "max"),
).reset_index()

# CLV proxy: monetary weighted by frequency & recency decay
rfm["clv_score"] = (
    rfm["monetary"] * np.log1p(rfm["frequency"])
    / np.log1p(rfm["recency"] + 1)
).round(2)

print(f"✅ RFM table built for {len(rfm):,} customers")
print(rfm[["customer_id","recency","frequency","monetary","clv_score"]].describe().round(2))

# ── 3. Scale features ─────────────────────────────────────────────────────────
FEATURES = ["recency", "frequency", "monetary", "avg_order_value", "clv_score"]
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(rfm[FEATURES])

# ── 4. Elbow + Silhouette to pick K ───────────────────────────────────────────
inertias, sil_scores = [], []
K_RANGE = range(2, 9)

for k in K_RANGE:
    km  = KMeans(n_clusters=k, random_state=42, n_init=10)
    lbl = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, lbl))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.patch.set_facecolor("#0F1117")
for ax in axes:
    ax.set_facecolor("#1A1D2E")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")

axes[0].plot(K_RANGE, inertias, "o-", color="#00D4FF", lw=2)
axes[0].axvline(x=4, color="#FF6B6B", ls="--", lw=1.5, label="Chosen K=4")
axes[0].set_title("Elbow Method — Inertia vs K"); axes[0].set_xlabel("K"); axes[0].set_ylabel("Inertia")
axes[0].legend(facecolor="#1A1D2E", labelcolor="white")

axes[1].plot(K_RANGE, sil_scores, "s-", color="#7BFF7B", lw=2)
axes[1].axvline(x=4, color="#FF6B6B", ls="--", lw=1.5, label="Chosen K=4")
axes[1].set_title("Silhouette Score vs K"); axes[1].set_xlabel("K"); axes[1].set_ylabel("Score")
axes[1].legend(facecolor="#1A1D2E", labelcolor="white")

plt.suptitle("K-Means Optimal Cluster Selection", color="white", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}elbow_plot.png", dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"📈 Elbow plot saved")

# ── 5. Final model — K = 4 ────────────────────────────────────────────────────
BEST_K = 4
km_final = KMeans(n_clusters=BEST_K, random_state=42, n_init=20)
rfm["cluster"] = km_final.fit_predict(X_scaled)

# Label clusters by mean CLV
cluster_means  = rfm.groupby("cluster")["clv_score"].mean().sort_values(ascending=False)
label_map      = {old: new for new, old in enumerate(cluster_means.index)}
rfm["cluster"] = rfm["cluster"].map(label_map)

SEGMENT_NAMES  = {0: "Champions", 1: "Loyal Customers", 2: "At-Risk", 3: "Lost / Dormant"}
SEGMENT_COLORS = {0: "#00D4FF", 1: "#7BFF7B", 2: "#FFD700", 3: "#FF6B6B"}
rfm["segment"] = rfm["cluster"].map(SEGMENT_NAMES)

sil = silhouette_score(X_scaled, rfm["cluster"])
print(f"\n✅ K-Means (K={BEST_K}) — Silhouette Score: {sil:.4f}")

# ── 6. Cluster scatter plot ───────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#0F1117")
for ax in axes:
    ax.set_facecolor("#1A1D2E")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")

for seg, color in SEGMENT_COLORS.items():
    mask = rfm["cluster"] == seg
    axes[0].scatter(rfm.loc[mask, "recency"], rfm.loc[mask, "monetary"],
                    c=color, label=SEGMENT_NAMES[seg], alpha=0.7, s=40, edgecolors="none")
axes[0].set_xlabel("Recency (days)"); axes[0].set_ylabel("Monetary (₹)")
axes[0].set_title("Customer Segments: Recency vs Monetary")
axes[0].legend(facecolor="#1A1D2E", labelcolor="white", fontsize=8)

for seg, color in SEGMENT_COLORS.items():
    mask = rfm["cluster"] == seg
    axes[1].scatter(rfm.loc[mask, "frequency"], rfm.loc[mask, "clv_score"],
                    c=color, label=SEGMENT_NAMES[seg], alpha=0.7, s=40, edgecolors="none")
axes[1].set_xlabel("Frequency (orders)"); axes[1].set_ylabel("CLV Score")
axes[1].set_title("Customer Segments: Frequency vs CLV Score")
axes[1].legend(facecolor="#1A1D2E", labelcolor="white", fontsize=8)

plt.suptitle("K-Means Customer Segmentation (K=4)", color="white", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{PLOTS_DIR}cluster_plot.png", dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"📊 Cluster scatter plot saved")

# ── 7. Segment summary ────────────────────────────────────────────────────────
summary = rfm.groupby("segment").agg(
    n_customers     = ("customer_id", "count"),
    avg_clv         = ("clv_score", "mean"),
    avg_recency     = ("recency", "mean"),
    avg_frequency   = ("frequency", "mean"),
    avg_monetary    = ("monetary", "mean"),
    total_revenue   = ("monetary", "sum"),
).round(2).reset_index()

summary["revenue_share_%"] = (summary["total_revenue"] / summary["total_revenue"].sum() * 100).round(1)

MARKETING_ACTIONS = {
    "Champions":        "Reward with loyalty points; upsell premium products; request reviews.",
    "Loyal Customers":  "Offer membership perks; cross-sell complementary categories.",
    "At-Risk":          "Win-back email with 15% discount; survey for pain-points.",
    "Lost / Dormant":   "Aggressive re-engagement campaign; last-chance offer before removal.",
}
summary["marketing_action"] = summary["segment"].map(MARKETING_ACTIONS)

print("\n📋 Segment Summary:")
print(summary[["segment","n_customers","avg_clv","avg_monetary","revenue_share_%"]].to_string(index=False))

# ── 8. Save outputs ───────────────────────────────────────────────────────────
rfm.to_csv(f"{OUTPUT_DIR}customer_segments.csv", index=False)
summary.to_csv(f"{OUTPUT_DIR}segment_summary.csv", index=False)
print(f"\n✅ Outputs saved:\n  {OUTPUT_DIR}customer_segments.csv\n  {OUTPUT_DIR}segment_summary.csv")
