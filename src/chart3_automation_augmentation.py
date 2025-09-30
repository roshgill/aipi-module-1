# Citation:
# AI Tool Used: Claude Code Agent
# Prompt: Create a python file which retrieves aei_cleaned.csv from data/processed/aei_cleaned.csv pathway.
# Next, create a group map set containing directive (key): Automation (value), feedback loop (key): Automation (value)
# validation (key): Augmentation, task iteration: Augmentation, learning: Augmentation
# Again, separate collaboration and collaboration_pct rows from cleaned database.
# Then map cluster name to groups and group them by automation/augmentation and geo_id, and create a bar chart
# to compare NC vs US group averages. Make it look simple and comprehendable.
# Rationale: Our goal was to label the collaboration patterns as either automated or augmented, retrieve collaboration data
# from cleaned dataset and create the metric comparison between NC and US.

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/processed/aei_cleaned.csv")

# group collaboration patterns into automation vs augmentation
group_map = {
    'directive': 'Automation',
    'feedback loop': 'Automation',
    'validation': 'Augmentation',
    'task iteration': 'Augmentation',
    'learning': 'Augmentation'
}

df_collab = df[
    (df['facet'] == 'collaboration') &
    (df['variable'] == 'collaboration_pct')
].copy()

df_collab['group'] = df_collab['cluster_name'].map(group_map)
df_grouped = df_collab.groupby(['group', 'geo_id'])['value'].sum().unstack()

# US average
state_cols = [col for col in df_grouped.columns if col != 'NC']
df_grouped['US_avg'] = df_grouped[state_cols].mean(axis=1)
df_grouped = df_grouped[['NC', 'US_avg']]

# plot grouped bars
fig, ax = plt.subplots(figsize=(8, 6))
df_grouped.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e'], width=0.7)

# add percentages on bars
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=3)

ax.set_title('automation vs augmentation: NC vs US', fontsize=14)
ax.set_ylabel('share of Claude usage (%)', fontsize=12)
ax.set_xlabel('')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(['North Carolina', 'US average'], loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("figures/chart3_automation_vs_augmentation.png", dpi=200, bbox_inches='tight')
plt.show()

print("saved chart3")
