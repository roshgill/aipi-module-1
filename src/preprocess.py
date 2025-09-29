import pandas as pd
from feature_engineering import engineer_features

def preprocess():
    # Hardcoding paths for simplicity sake
    input_path = "data/raw/aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv"
    cleaned_path = "data/processed/aei_cleaned.csv"
    featured_path = "data/processed/aei_with_features.csv"

    df = pd.read_csv(input_path)

    # Filter to all US states
    df = df[df['geography'] == 'state_us']

    # Keep collaboration and onet_task facets.
    # Help us distinguish the types of tasks done and 5 collaboration metrics between US states and North Carolina
    keep_facets = ['collaboration', 'onet_task']
    keep_vars = ['collaboration_pct', 'onet_task_pct', 'onet_task_count']
    df = df[df['facet'].isin(keep_facets) & df['variable'].isin(keep_vars)]

    # Drop not_classified and none
    df = df[~df['cluster_name'].isin(['not_classified', 'none'])]

    # Save cleaned data
    df.to_csv(cleaned_path, index=False)
    
    # Apply feature engineering
    df_with_features = engineer_features(df)
    df_with_features.to_csv(featured_path, index=False)

    print(f"Preprocessing complete. Cleaned data saved to {cleaned_path} and featured data saved to {featured_path}")

if __name__ == "__main__":
    preprocess()
