# DeFi Wallet Credit Scoring - Aave V2

## Objective

Build a machine learning pipeline to assign a **credit score (0–1000)** to DeFi wallets based on their historical activity in the Aave V2 protocol. Higher scores indicate safer, more trustworthy wallets. Lower scores may represent risky, bot-like, or malicious behavior.

## 🔗 Input File Link

[👉 Download user\_transactions.json (ZIP)](https://drive.google.com/file/d/14ceBCLQ-BTcydDrFJauVA_PKAZ7VtDor/view?usp=sharing)


## Processing Architecture

```
Raw JSON Data
     ↓
Load & Normalize (Pandas)
     ↓
Preprocess (USD Conversion, Timestamp parsing)
     ↓
Group by Wallet & Extract Features
     ↓
Score Wallets (Rule-based + Normalization)
     ↓
Export CSV (wallet, score)
```

## 🧮 Scoring Logic

### Normalized Positive Factors:

* total_deposit_usd
* total_repay_usd
* repay_rate
* deposit_to_withdraw_ratio
* activity_span_days

These are scaled to the range 0–1000 using MinMaxScaler.

### Penalty Factors:

* liquidation_count × 30
* borrow_to_repay_ratio × 10

### Final Score:

```
raw_score = scaled_features.sum(axis=1) - penalty
score = MinMaxScaler((0, 1000)).fit_transform(raw_score)
```

## Output
* File: `wallet_scores.csv`

