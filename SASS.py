# ============================================================
# SaaS / Telco Customer Analysis using Real Dataset
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
print(os.getcwd())
# ============================================================
# STEP 1: Load Dataset
# ============================================================

df = pd.read_csv("D:\saasprojectpython\SAAS DATA SET.CSV.csv")

print("Dataset Loaded Successfully\n")
print(df.head())

# ============================================================
# STEP 2: Data Cleaning
# ============================================================

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Drop null values
df.dropna(inplace=True)

# Convert MonthlyCharges as Subscription Price
df["Subscription_Price"] = df["MonthlyCharges"]

# Create churn column (Yes=1, No=0)
df["Churn_Flag"] = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

# ============================================================
# STEP 3: Monthly Simulation (since dataset not monthly)
# ============================================================

months = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

np.random.seed(42)

new_customers = np.random.randint(80, 200, 12)
churned_customers = np.random.randint(20, 100, 12)

active_customers = []
current = 300

for i in range(12):
    current = current + new_customers[i] - churned_customers[i]
    active_customers.append(current)

subscription_price = np.random.choice(df["Subscription_Price"], 12)

# ============================================================
# STEP 4: MRR & LTV
# ============================================================

mrr = np.array(active_customers) * subscription_price

churn_rate = churned_customers / np.maximum(active_customers, 1)

ltv = subscription_price / churn_rate

# ============================================================
# STEP 5: DataFrame
# ============================================================

final_df = pd.DataFrame({
    "Month": months,
    "New_Customers": new_customers,
    "Churned_Customers": churned_customers,
    "Subscription_Price": subscription_price,
    "Active_Customers": active_customers,
    "MRR": mrr.round(2),
    "LTV": ltv.round(2)
})

# Save CSV
final_df.to_csv("output.csv", index=False)

print("\nFinal Dataset Created:\n")
print(final_df.head())

# ============================================================
# STEP 6: Visualization
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# MRR Line
axes[0,0].plot(final_df["Month"], final_df["MRR"], marker="o")
axes[0,0].set_title("MRR Growth")

# Bar Chart
x = np.arange(len(months))
axes[0,1].bar(x-0.2, final_df["New_Customers"], width=0.4, label="New")
axes[0,1].bar(x+0.2, final_df["Churned_Customers"], width=0.4, label="Churn")
axes[0,1].set_xticks(x)
axes[0,1].set_xticklabels(months)
axes[0,1].legend()
axes[0,1].set_title("New vs Churn")

# Scatter
axes[1,0].scatter(final_df["MRR"], final_df["LTV"])
axes[1,0].set_title("MRR vs LTV")

# Histogram
axes[1,1].hist(final_df["Active_Customers"])
axes[1,1].set_title("Active Customers Distribution")

plt.tight_layout()
plt.savefig("D:\saas project python")
plt.show()

print("\nDashboard saved as dashboard.png")