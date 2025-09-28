import pandas as pd

def preprocess():
    # Hardcoding paths for simplicity sake
    input_path = "data/raw/aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv"
    output_path = "data/processed/aei_cleaned.csv"

    df = pd.read_csv(input_path)

    # Filter to NC and US
    df = df[
        ((df['geography'] == 'state_us') & (df['geo_id'] == 'NC')) |
        ((df['geography'] == 'country') & (df['geo_id'] == 'US'))
    ]

    # Keep collaboration and onet_task facets.
    # Help us distinguish the types of tasks done and 5 collaboration metrics between US states and North Carolina
    keep_facets = ['collaboration', 'onet_task']
    keep_vars = ['collaboration_pct', 'onet_task_pct', 'onet_task_count']
    df = df[df['facet'].isin(keep_facets) & df['variable'].isin(keep_vars)]

    # Drop not_classified and none
    df = df[~df['cluster_name'].isin(['not_classified', 'none'])]

    # Save to output path
    df.to_csv(output_path, index=False)
    print(f"✅ Preprocessing complete. Cleaned data saved to {output_path}")

if __name__ == "__main__":
    preprocess()
