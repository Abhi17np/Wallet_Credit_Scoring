import json
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import os

# === Step 1: Load JSON File ===
def load_data(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    return df

# === Step 2: Preprocess Transactions ===
def preprocess(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['amount_usd'] = df['actionData.amount'].astype(float) * df['actionData.assetPriceUSD'].astype(float)
    return df

# === Step 3: Feature Engineering Per Wallet ===
def extract_features(df):
    wallets = defaultdict(lambda: {
        'total_deposit_usd': 0, 'total_borrow_usd': 0, 'total_repay_usd': 0, 'total_redeem_usd': 0,
        'liquidation_count': 0, 'deposit_count': 0, 'borrow_count': 0,
        'repay_count': 0, 'redeem_count': 0, 'tx_timestamps': [], 'first_ts': None, 'last_ts': None
    })

    for _, row in tqdm(df.iterrows(), total=len(df)):
        wallet = row['userWallet']
        action = row['action']
        amt_usd = row['amount_usd']
        ts = row['timestamp']

        wallets[wallet]['tx_timestamps'].append(ts)
        if wallets[wallet]['first_ts'] is None or ts < wallets[wallet]['first_ts']:
            wallets[wallet]['first_ts'] = ts
        if wallets[wallet]['last_ts'] is None or ts > wallets[wallet]['last_ts']:
            wallets[wallet]['last_ts'] = ts

        if action == 'deposit':
            wallets[wallet]['total_deposit_usd'] += amt_usd
            wallets[wallet]['deposit_count'] += 1
        elif action == 'borrow':
            wallets[wallet]['total_borrow_usd'] += amt_usd
            wallets[wallet]['borrow_count'] += 1
        elif action == 'repay':
            wallets[wallet]['total_repay_usd'] += amt_usd
            wallets[wallet]['repay_count'] += 1
        elif action == 'redeemunderlying':
            wallets[wallet]['total_redeem_usd'] += amt_usd
            wallets[wallet]['redeem_count'] += 1
        elif action == 'liquidationcall':
            wallets[wallet]['liquidation_count'] += 1

    records = []
    for wallet, w in wallets.items():
        span = (w['last_ts'] - w['first_ts']).days if w['first_ts'] and w['last_ts'] else 0
        gaps = pd.Series(sorted(w['tx_timestamps'])).diff().dt.total_seconds().dropna()
        avg_gap = gaps.mean() / 86400 if not gaps.empty else 0

        records.append({
            'wallet': wallet,
            'total_deposit_usd': w['total_deposit_usd'],
            'total_borrow_usd': w['total_borrow_usd'],
            'total_repay_usd': w['total_repay_usd'],
            'total_redeem_usd': w['total_redeem_usd'],
            'liquidation_count': w['liquidation_count'],
            'borrow_count': w['borrow_count'],
            'repay_count': w['repay_count'],
            'activity_span_days': span,
            'avg_tx_gap_days': avg_gap,
            'repay_rate': w['repay_count'] / w['borrow_count'] if w['borrow_count'] else 0,
            'borrow_to_repay_ratio': w['total_borrow_usd'] / w['total_repay_usd'] if w['total_repay_usd'] else 0,
            'deposit_to_withdraw_ratio': w['total_deposit_usd'] / w['total_redeem_usd'] if w['total_redeem_usd'] else 0
        })
    return pd.DataFrame(records)

# === Step 4: Scoring Logic ===
def score_wallets(df):
    features = ['total_deposit_usd', 'total_repay_usd', 'repay_rate',
                'deposit_to_withdraw_ratio', 'activity_span_days']

    df[features] = df[features].fillna(0)
    scaled = MinMaxScaler((0, 1000)).fit_transform(df[features])

    penalty = (df['liquidation_count'] * 30) + (df['borrow_to_repay_ratio'].fillna(0) * 10)
    raw_score = scaled.sum(axis=1) - penalty
    raw_score = raw_score.clip(lower=0)

    df['score'] = MinMaxScaler((0, 1000)).fit_transform(raw_score.values.reshape(-1, 1)).astype(int)
    return df[['wallet', 'score']].sort_values(by='score', ascending=False)

# === Main Execution ===
if __name__ == "__main__":
    input_path = "data/user_transactions.json"
    output_path = "output/wallet_scores.csv"

    os.makedirs("output", exist_ok=True)

    df = load_data(input_path)
    print(f"✅ Loaded {len(df)} transactions.")
    print(f"👛 Unique wallets in data: {df['userWallet'].nunique()}")

    df = preprocess(df)
    features_df = extract_features(df)
    scored_df = score_wallets(features_df)
    scored_df.to_csv(output_path, index=False)

    print(f"✅ Done! {len(scored_df)} wallets scored. Output saved to '{output_path}'.")
