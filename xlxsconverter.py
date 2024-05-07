import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Loop over the columns and strip whitespaces
for col in df.columns:
    # Check if the column's data type is object (text)
    if df[col].dtype == 'object':
        df[col] = df[col].str.strip()

# Save the cleaned data back to a CSV file
df.to_csv('data.csv', index=False)