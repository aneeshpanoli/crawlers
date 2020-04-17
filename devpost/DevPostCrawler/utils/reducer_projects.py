import pandas as pd

# Read JSON lines and get rid of some text-heavy columns
df = pd.read_json('../projects.jl', lines=True).drop(['storyText', 'storyHTML'], axis=1)

# Export to Tab-separated File
df.to_csv('../projects.tsv', sep='\t', encoding='utf-8', index=False)

