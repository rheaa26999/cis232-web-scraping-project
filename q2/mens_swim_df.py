import pandas as pd

# Men's Swimming DataFrame (Member 1 responsibility)
data = [
    {"school": "College of Staten Island", "name": "Sample Swimmer A", "height": "6-1"},
    {"school": "York College", "name": "Sample Swimmer B", "height": "5-11"},
    {"school": "Baruch College", "name": "Sample Swimmer C", "height": "6-3"},
]

df_mens_swim = pd.DataFrame(data)

print("Men's Swimming DataFrame:")
print(df_mens_swim)

# Save dataframe to CSV
df_mens_swim.to_csv("data/mens_swim_sample.csv", index=False)
print("Saved CSV to data/mens_swim_sample.csv")
