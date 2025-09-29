import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/processed/aei_cleaned.csv")

# Define collaboration pattern groupings
group_map = {
    'directive': 'automation',
    'feedback_loop': 'automation',
    'validation': 'augmentation',
    'task_iteration': 'augmentation',
    'learning': 'augmentation'
}

# Filter to collaboration facet and collaboration_pct variable
df_collab = df[
    (df['facet'] == 'collaboration') &
    (df['variable'] == 'collaboration_pct') &
    (df['cluster_name'].isin(group_map.keys()))
]

# Map each pattern to its group
df_collab['group'] = df_collab['cluster_name'].map(group_map)

# Group by automation/augmentation and geo_id
df_grouped = df_collab.groupby(['group', 'geo_id'])['value'].sum().unstack()

# Calculate US average from other states (excluding NC)
state_cols = [col for col in df_grouped.columns if col != 'NC']
df_grouped['US_avg'] = df_grouped[state_cols].mean(axis=1)

# Keep only NC and US average
df_grouped = df_grouped[['NC', 'US_avg']]

# Plot
ax = df_grouped.plot(kind='bar', figsize=(8, 5), color=['#1f77b4', '#ff7f0e'])

# Add percentage labels on top of bars
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='edge', padding=3)

plt.title("Automation vs Augmentation: NC vs U.S. Average")
plt.ylabel("Share of Claude Usage")
plt.xticks(rotation=0)
plt.legend(["North Carolina", "US Average (Other States)"])
plt.tight_layout()

# Save figure
plt.savefig("figures/chart1_collab_automation_vs_augmentation.png")
plt.show()
