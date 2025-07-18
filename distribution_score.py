import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the scored wallet CSV
csv_path = "output/wallet_scores.csv"
df = pd.read_csv(csv_path)

# Plot configuration
plt.figure(figsize=(10, 6))
sns.histplot(df['score'], bins=range(0, 1100, 100), kde=False, color="#007acc", edgecolor="black")

# Labels and title
plt.title("Wallet Credit Score Distribution", fontsize=16)
plt.xlabel("Credit Score Range", fontsize=12)
plt.ylabel("Number of Wallets", fontsize=12)
plt.xticks(ticks=range(0, 1100, 100))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig("output/score_distribution.png")
plt.show()

print("✅ Score distribution plot saved as 'output/score_distribution.png'")
