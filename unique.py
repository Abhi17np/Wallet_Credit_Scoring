import json
import pandas as pd

# Replace with your actual JSON path
json_file = "data/user_transactions.json"

# Load the data
with open(json_file, "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.json_normalize(data)

# Count unique wallets
unique_wallets = df["userWallet"].nunique()
total_rows = len(df)

print(f"📦 Total transactions: {total_rows}")
print(f"👛 Unique wallets: {unique_wallets}")
