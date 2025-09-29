import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/aei_cleaned.csv")

# get collaboration data
df_collab = df[
    (df['facet'] == 'collaboration') &
    (df['variable'] == 'collaboration_pct')
]

# pivot to get NC vs other states
df_pivot = df_collab.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()

# calc US avg without NC
state_cols = [col for col in df_pivot.columns if col not in ['cluster_name', 'NC']]
df_pivot['US_avg'] = df_pivot[state_cols].mean(axis=1)

# difference from baseline
df_pivot['difference'] = df_pivot['NC'] - df_pivot['US_avg']
df_pivot = df_pivot.sort_values('difference')

# plot
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#d62728' if x < 0 else '#2ca02c' for x in df_pivot['difference']]
ax.barh(df_pivot['cluster_name'], df_pivot['difference'], color=colors)
ax.axvline(0, color='black', linewidth=1.2)
ax.set_xlabel('percentage points vs US average')
ax.set_title('How NC differs: Collaboration Patterns')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig("figures/chart1_collaboration_difference.png", dpi=200, bbox_inches='tight')
plt.show()

print("saved chart1")