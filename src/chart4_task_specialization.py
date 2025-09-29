import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/processed/aei_cleaned.csv")

# get task data
df_task_pct = df[(df['facet'] == 'onet_task') & (df['variable'] == 'onet_task_pct')]
df_task_count = df[(df['facet'] == 'onet_task') & (df['variable'] == 'onet_task_count')]

# pivot both
df_pct_pivot = df_task_pct.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()
df_count_pivot = df_task_count.pivot(index='cluster_name', columns='geo_id', values='value').reset_index()

# calc US averages
state_cols_pct = [col for col in df_pct_pivot.columns if col not in ['cluster_name', 'NC']]
df_pct_pivot['US_avg_pct'] = df_pct_pivot[state_cols_pct].mean(axis=1)

# merge pct and counts
df_merged = pd.merge(
    df_pct_pivot[['cluster_name', 'NC', 'US_avg_pct']], 
    df_count_pivot[['cluster_name', 'NC']], 
    on='cluster_name',
    suffixes=('_pct', '_count')
)

# filter: need at least 30 NC occurrences to be meaningful
df_filtered = df_merged[
    (df_merged['NC_count'] >= 30) & 
    (df_merged['US_avg_pct'] > 0)
].copy()

# specialization index = NC / US average
df_filtered['spec_index'] = df_filtered['NC_pct'] / df_filtered['US_avg_pct']

# get top 5 over and under indexed
top_over = df_filtered.nlargest(5, 'spec_index')
top_under = df_filtered.nsmallest(5, 'spec_index')
df_viz = pd.concat([top_under, top_over]).sort_values('spec_index')

# shorten long task names
def shorten_task(task, max_len=50):
    if len(task) <= max_len:
        return task
    return task[:max_len-3] + '...'

df_viz['short_name'] = df_viz['cluster_name'].apply(shorten_task)

# plot
fig, ax = plt.subplots(figsize=(12, 7))
colors = ['#d62728' if x < 1 else '#2ca02c' for x in df_viz['spec_index']]
y_pos = range(len(df_viz))

ax.barh(y_pos, df_viz['spec_index'], color=colors, alpha=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(df_viz['short_name'], fontsize=10)
ax.axvline(1.0, color='black', linewidth=1.2, linestyle='--', label='US baseline')
ax.set_xlabel('specialization index (NC/US average)', fontsize=12)
ax.set_title('Task Specialization: Where NC over/under-indexes', fontsize=14)
ax.legend(fontsize=10)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig("figures/chart4_task_specialization.png", dpi=200, bbox_inches='tight')
plt.show()

print("saved chart4")