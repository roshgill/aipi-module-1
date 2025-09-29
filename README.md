# AIPI 510 Project 1: Data Storytelling - AI Usage in North Carolina

Our project analyzes Claude AI usage data from the Antrhopic Economic Index (AEI) to compare collaboration patterns and tasks in North Carolina vs the US avg. As part of our keys findings, NC shows higher "tasks interation" and augmentatin-style use of AI, which suggests more creative use with human-input collaboration to reach goals. 

## Citation
A public dataset of Claude AI (Free/Pro) from Anthropic Economic Index was used for this analysis with an usage rangr from Aug-11, 2025.
Includes:
- Facets like collaboration (5 patterns)
- ONET tasks (multi-label)
- Filtered to US states

Raw file: ~100k rows, 10 columns (e.g., geo_id, facet, value).

**Citation**: Anthropic Economic Index (AEI) - Claude AI Usage Data. Sourced from Anthropic's Sep 15, 2025 raw CSV (via direct download). Link: [Anthropic AEI Dataset](https://www-cdn.anthropic.com/2a6b74e3f9a0e12b61b08d43337622b05da641dc.zip).


## Steps to Reproduce Analysis
1. **Setup**: Install dependencies from `requirements.txt`.
2. **Preprocessing**: Run `src/preprocess.py` to filter raw data (saved in `data/processed/aei_cleaned.csv`).
3. **Exploratory Data Analysis**: Available in `notebooks/01_eda.ipynb`.
4. **Generate Visualizations**:
   - Run `src/firstvisualization.py` for collaboration bar chart.
   - Run `src/secondvisualization.py` for automation vs. augmentation.
   - Run `src/plot_task_visualization.py` for task specialization index.
   Outputs saved to `figures/`.

## Limitations
Data:
- One-week snapshot; 
- Biased toward tech users (e.g., underrepresents non-digital workers).
