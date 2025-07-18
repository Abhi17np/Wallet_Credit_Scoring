import json
import pandas as pd

json_file = "data/user_transactions.json"
with open(json_file, "r") as f:
    data = json.load(f)

df = pd.json_normalize(data)
unique_wallets = df["userWallet"].nunique()
total_rows = len(df)

print(f" Total transactions: {total_rows}")
print(f" Unique wallets: {unique_wallets}")
