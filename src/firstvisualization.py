import pandas as pd
import matplotlib.pyplot as plt

# Load data from cleaned csv
df = pd.read_csv("data/processed/aei_cleaned.csv")

# Filter collaboration facet and collaboration_pct
df_collab = df[
    (df['facet'] == 'collaboration') &
    (df['variable'] == 'collaboration_pct')
]

# Get NC and US side-by-side
df_pivot = df_collab.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()
df_pivot = df_pivot.sort_values(by='NC', ascending=False)

plt.figure(figsize=(10, 6))
bar_width = 0.35
x = range(len(df_pivot))

plt.bar(x, df_pivot['NC'], width=bar_width, label='North Carolina', color='#1f77b4')
plt.bar([i + bar_width for i in x], df_pivot['US'], width=bar_width, label='United States', color='#ff7f0e')

plt.xticks([i + bar_width / 2 for i in x], df_pivot['cluster_name'], rotation=45)
plt.ylabel("Share of Claude Usage")
plt.title("Collaboration Styles: NC vs U.S.")
plt.legend()
plt.tight_layout()

plt.savefig("figures/chart1_collaboration_comparison.png")
plt.show()
