import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('historia_oglądania.csv', sep=',')

# Display the DataFrame to check the structure and contents
print(df)

# Save to CSV file with specific columns
df.to_csv('output.csv', columns=['Source', 'Title', 'Subtitle', 'Details', 'Timestamp', 'Products', 'Reason'], index=False)