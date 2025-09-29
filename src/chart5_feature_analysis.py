import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_augmentation_ratio_chart():
    df = pd.read_csv("data/processed/aei_with_features.csv")
    collab_df = df[df['facet'] == 'collaboration'].copy()
    state_ratios = collab_df[['geo_id', 'augmentation_ratio', 'region']].drop_duplicates()
    state_ratios = state_ratios.sort_values('augmentation_ratio', ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    region_colors = {
        'Southeast': '#1f77b4',
        'Northeast': '#ff7f0e', 
        'Midwest': '#2ca02c',
        'West': '#d62728'
    }
    
    colors = [region_colors.get(region, '#808080') for region in state_ratios['region']]
    colors = ['#FFD700' if state == 'NC' else color for state, color in zip(state_ratios['geo_id'], colors)]
    
    bars = ax.barh(state_ratios['geo_id'], state_ratios['augmentation_ratio'], color=colors)
    
    nc_idx = list(state_ratios['geo_id']).index('NC')
    bars[nc_idx].set_edgecolor('black')
    bars[nc_idx].set_linewidth(2)
    
    ax.set_xlabel('Augmentation Ratio (Higher = More Augmentation Style)')
    ax.set_title('AI Collaboration Style: Augmentation vs Automation Across States')
    ax.grid(axis='x', alpha=0.3)
    ax.axvline(1.0, color='black', linestyle='--', alpha=0.5, label='Equal Aug/Auto')
    
    legend_elements = [plt.Rectangle((0,0),1,1, color=color, label=region) 
                      for region, color in region_colors.items()]
    legend_elements.append(plt.Rectangle((0,0),1,1, color='#FFD700', label='North Carolina'))
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig("figures/chart5_augmentation_ratios.png", dpi=200, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("generating feature visualizations...")
    
    # Run feature engineering first if needed
    try:
        df_test = pd.read_csv("data/processed/aei_with_features.csv")
        print("using existing data...")
    except FileNotFoundError:
        print("running feature engineering first...")
        import subprocess
        subprocess.run(["python", "src/feature_engineering.py"])
    
    # Create visualizations
    create_augmentation_ratio_chart()
    
    print("charts saved to figures/")
