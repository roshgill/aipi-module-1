import pandas as pd
import numpy as np

def add_regional_features(df):
    # add regions for states
    region_mapping = {
        # Southeast
        'NC': 'Southeast', 'SC': 'Southeast', 'VA': 'Southeast', 'WV': 'Southeast',
        'KY': 'Southeast', 'TN': 'Southeast', 'GA': 'Southeast', 'FL': 'Southeast',
        'AL': 'Southeast', 'MS': 'Southeast', 'LA': 'Southeast', 'AR': 'Southeast',
        
        # Northeast
        'ME': 'Northeast', 'NH': 'Northeast', 'VT': 'Northeast', 'MA': 'Northeast',
        'RI': 'Northeast', 'CT': 'Northeast', 'NY': 'Northeast', 'NJ': 'Northeast',
        'PA': 'Northeast',
        
        # Midwest
        'OH': 'Midwest', 'MI': 'Midwest', 'IN': 'Midwest', 'IL': 'Midwest',
        'WI': 'Midwest', 'MN': 'Midwest', 'IA': 'Midwest', 'MO': 'Midwest',
        'ND': 'Midwest', 'SD': 'Midwest', 'NE': 'Midwest', 'KS': 'Midwest',
        
        # West
        'MT': 'West', 'WY': 'West', 'CO': 'West', 'NM': 'West', 'ID': 'West',
        'UT': 'West', 'NV': 'West', 'AZ': 'West', 'WA': 'West', 'OR': 'West',
        'CA': 'West', 'AK': 'West', 'HI': 'West'
    }
    
    df_with_regions = df.copy()
    df_with_regions['region'] = df_with_regions['geo_id'].map(region_mapping)
    return df_with_regions



def create_collaboration_indices(df):
    # calculate augmentation vs automation ratios
    # Get collaboration data only
    collab_df = df[df['facet'] == 'collaboration'].copy()
    
    if collab_df.empty:
        return df
    
    # Pivot to get collaboration patterns as columns
    collab_pivot = collab_df.pivot_table(
        index='geo_id', 
        columns='cluster_name', 
        values='value',
        fill_value=0
    ).reset_index()
    
    # Calculate augmentation vs automation indices
    augmentation_cols = ['task iteration', 'learning', 'feedback loop']
    automation_cols = ['directive', 'validation']
    
    # Check which columns actually exist
    existing_aug_cols = [col for col in augmentation_cols if col in collab_pivot.columns]
    existing_auto_cols = [col for col in automation_cols if col in collab_pivot.columns]
    
    if existing_aug_cols:
        collab_pivot['augmentation_score'] = collab_pivot[existing_aug_cols].sum(axis=1)
    else:
        collab_pivot['augmentation_score'] = 0
        
    if existing_auto_cols:
        collab_pivot['automation_score'] = collab_pivot[existing_auto_cols].sum(axis=1)
    else:
        collab_pivot['automation_score'] = 0
    
    # Calculate augmentation ratio (avoid division by zero)
    collab_pivot['augmentation_ratio'] = np.where(
        collab_pivot['automation_score'] > 0,
        collab_pivot['augmentation_score'] / collab_pivot['automation_score'],
        collab_pivot['augmentation_score']
    )
    
    # Merge back with original dataframe
    feature_cols = ['geo_id', 'augmentation_ratio']
    
    df_with_collab = df.merge(
        collab_pivot[feature_cols],
        on='geo_id',
        how='left'
    )
    
    return df_with_collab


def engineer_features(df):
    # add regions and augmentation ratios
    df_features = add_regional_features(df)
    df_features = create_collaboration_indices(df_features)
    return df_features

if __name__ == "__main__":
    df = pd.read_csv("data/processed/aei_cleaned.csv")
    df_with_features = engineer_features(df)
    df_with_features.to_csv("data/processed/aei_with_features.csv", index=False)
