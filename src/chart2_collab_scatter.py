# Citation:
# AI Tool: Claude Code
# Prompt: make a scatter plot comparing NC vs US average for each collaboration pattern. 
# add a diagonal line where they'd be equal and label each point
# Rationale: scatter plot makes it easier to see which patterns NC over/under indexes on


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/aei_cleaned.csv")

df_collab = df[
    (df['facet'] == 'collaboration') &
    (df['variable'] == 'collaboration_pct')
]

df_pivot = df_collab.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()

state_cols = [col for col in df_pivot.columns if col not in ['cluster_name', 'NC']]
df_pivot['US_avg'] = df_pivot[state_cols].mean(axis=1)

# scatter plot showing NC vs US
fig, ax = plt.subplots(figsize=(8, 8))

ax.scatter(df_pivot['US_avg'], df_pivot['NC'], s=200, alpha=0.6, color='#1f77b4')

# diagonal line where NC = US
lims = [0, max(df_pivot['NC'].max(), df_pivot['US_avg'].max()) + 2]
ax.plot(lims, lims, 'k--', alpha=0.4, linewidth=1, label='NC = US average')

# label points
for _, row in df_pivot.iterrows():
    ax.annotate(row['cluster_name'], 
                 (row['US_avg'], row['NC']),
                 fontsize=10, alpha=0.8,
                 xytext=(5, 5), textcoords='offset points')

ax.set_xlabel('US average (%)', fontsize=12)
ax.set_ylabel('North Carolina (%)', fontsize=12)
ax.set_title('collaboration patterns: NC vs US', fontsize=14)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.set_xlim(lims[0], lims[1])
ax.set_ylim(lims[0], lims[1])

plt.tight_layout()
plt.savefig("figures/chart2_collaboration_scatter.png", dpi=200, bbox_inches='tight')
plt.show()

print("saved chart2")