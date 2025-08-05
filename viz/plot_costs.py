import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Replace these with your actual data loading! ---

# Example modalities for 10 queries (replace with your sequence)
query_modalities = [
    "DEMONSTRATION", "PREFERENCE", "PREFERENCE", "CORRECTION", "BINARY",
    "DEMONSTRATION", "PREFERENCE", "CORRECTION", "BINARY", "PREFERENCE"
]

# Example costs per modality (update as needed)
costs = {
    "DEMONSTRATION": 20,
    "PREFERENCE": 10,
    "CORRECTION": 15,
    "BINARY": 5,
}

# Example info gain values per query (replace with your actual info gains)
# You should compute information gain after each query in your main experiment!
info_gains = np.cumsum(np.random.uniform(0.01, 0.1, size=len(query_modalities))) # Just for demo

# --- Compute total cost after each query ---
total_costs = []
cost_accum = 0
for modality in query_modalities:
    cost_accum += costs[modality]
    total_costs.append(cost_accum)

# --- Save data to CSV (optional, for later plotting or reproducibility) ---
df = pd.DataFrame({
    'total_cost': total_costs,
    'info_gain': info_gains,
    'modality': query_modalities
})
df.to_csv("output/info_vs_cost.csv", index=False)

# --- Plotting ---
plt.figure(figsize=(8,5))
plt.plot(df['total_cost'], df['info_gain'], marker='o', linewidth=2)
for i, txt in enumerate(df['modality']):
    plt.annotate(txt, (df['total_cost'][i], df['info_gain'][i]), fontsize=8, alpha=0.7)
plt.xlabel("Total Cost")
plt.ylabel("Cumulative Information Gain")
plt.title("Information Gain vs Total Cost")
plt.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load your data
# Replace with your actual CSV path
df = pd.read_csv('output/info_vs_cost.csv')

# If you only have cumulative columns, compute per-query deltas
if 'cumulative_info_gain' in df.columns and 'cumulative_cost' in df.columns:
    df['info_gain'] = df['cumulative_info_gain'].diff().fillna(df['cumulative_info_gain'])
    df['cost'] = df['cumulative_cost'].diff().fillna(df['cumulative_cost'])
elif not {'info_gain', 'cost'}.issubset(df.columns):
    raise ValueError("CSV must contain either per-query info_gain and cost, or cumulative versions.")

# Compute per-query info gain per unit cost
df['info_gain_per_unit_cost'] = df['info_gain'] / df['cost']

# Plot 1: Per-Query Info Gain
plt.figure(figsize=(8, 5))
plt.plot(df.index, df['info_gain'], marker='o')
plt.xlabel('Query Index')
plt.ylabel('Info Gain')
plt.title('Per-Query Info Gain')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 2: Per-Query Info Gain per Unit Cost
plt.figure(figsize=(8, 5))
plt.plot(df.index, df['info_gain_per_unit_cost'], marker='o', color='orange')
plt.xlabel('Query Index')
plt.ylabel('Info Gain per Unit Cost')
plt.title('Per-Query Info Gain per Unit Cost')
plt.grid(True)
plt.tight_layout()
plt.show()