import pandas as pd
import matplotlib.pyplot as plt

# Load data from cleaned csv
df = pd.read_csv("data/processed/aei_cleaned.csv")

# Filter collaboration facet and collaboration_pct
df_collab = df[
    (df['facet'] == 'collaboration') &
    (df['variable'] == 'collaboration_pct')
]

# Get NC and calculate US average from other states
df_pivot = df_collab.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()

# Calculate US average excluding NC
state_cols = [col for col in df_pivot.columns if col not in ['cluster_name', 'NC']]
df_pivot['US_avg'] = df_pivot[state_cols].mean(axis=1)

# Keep only NC and US average
df_pivot = df_pivot[['cluster_name', 'NC', 'US_avg']].copy()
df_pivot = df_pivot.sort_values(by='NC', ascending=False)

plt.figure(figsize=(10, 6))
bar_width = 0.35
x = range(len(df_pivot))

plt.bar(x, df_pivot['NC'], width=bar_width, label='North Carolina', color='#1f77b4')
plt.bar([i + bar_width for i in x], df_pivot['US_avg'], width=bar_width, label='US Average (Other States)', color='#ff7f0e')

plt.xticks([i + bar_width / 2 for i in x], df_pivot['cluster_name'], rotation=45)
plt.ylabel("Share of Claude Usage")
plt.title("Collaboration Styles: NC vs U.S.")
plt.legend()
plt.tight_layout()

plt.savefig("figures/chart1_collaboration_comparison.png")
plt.show()
