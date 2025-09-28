import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Ensure output folder exists
os.makedirs("figures", exist_ok=True)

# Load cleaned data
df = pd.read_csv("data/processed/aei_cleaned.csv")

# Filter to onet_task facet and relevant variables
df_pct = df[(df['facet'] == 'onet_task') & (df['variable'] == 'onet_task_pct')]
df_count = df[(df['facet'] == 'onet_task') & (df['variable'] == 'onet_task_count')]

# Pivot to get NC and US side-by-side
df_pct_pivot = df_pct.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()
df_count_pivot = df_count.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()

# Merge pct and count data
df_merged = pd.merge(df_pct_pivot, df_count_pivot, on='cluster_name', suffixes=('_pct', '_count'))

# Filter out low-volume tasks
min_nc_count = 30
df_filtered = df_merged[df_merged['NC_count'] >= min_nc_count].copy()

# Avoid divide-by-zero
df_filtered = df_filtered[df_filtered['US_pct'] > 0].copy()

# Compute specialization index
df_filtered['specialization_index'] = df_filtered['NC_pct'] / df_filtered['US_pct']

# Sort and select top/bottom tasks
top_n = 5
df_sorted = df_filtered.sort_values('specialization_index', ascending=False)
top_over = df_sorted.head(top_n)
top_under = df_sorted.tail(top_n)
df_final = pd.concat([top_over, top_under])
df_final = df_final.sort_values('specialization_index')


# Specialization Index (NC vs US baseline)
fig, ax = plt.subplots(figsize=(12, 6))
y = np.arange(len(df_final))
bar_color = "#1f77b4"  # NC blue

ax.barh(y, df_final['specialization_index'], color=bar_color)
ax.axvline(1.0, color='gray', linestyle='--', linewidth=1.2, label='US baseline (=1.0)')

ax.set_yticks(y)
ax.set_yticklabels(df_final['cluster_name'])
ax.set_xlabel("Specialization Index (NC_pct / US_pct)")
ax.set_title("Task Specialization: North Carolina vs U.S. ")

# Legend
legend_items = [
    Patch(facecolor=bar_color, edgecolor='none', label='NC specialization (index)'),
    Line2D([0], [0], color='gray', linestyle='--', label='US baseline (=1.0)')
]
ax.legend(handles=legend_items, loc='lower right')

# Fix for long labels
plt.tight_layout()

plt.savefig("figures/chart2_task_specialization_index.png", dpi=200)
plt.show()

