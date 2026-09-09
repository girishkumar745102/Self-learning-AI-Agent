import pandas as pd
df = pd.read_csv("data/intent_dataset.csv")
print(df.head())
print(list(df.columns))
print(df.shape)
print(df['label'].value_counts())
