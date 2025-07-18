# Wallet Score Analysis

This document provides a clear analysis of the credit scores assigned to Aave V2 wallet addresses based on their transaction behaviors.

## 📊 Visualization

Run `score_distribution_plot.py` to generate a histogram of scores:

* File saved to: `output/score_distribution.png`

## Wallet Behavior by Score Range

### Low Score (0 - 200)

* Frequent liquidation events
* Low or no repayment activity
* Irregular usage or short lifespan
* High borrow amounts with little deposit backing

### Mid Score (400 - 600)

* Balanced mix of deposits and borrows
* Moderate repayment history
* Some wallets may have minor liquidation incidents
* Generally consistent but not highly active

### High Score (800 - 1000)

* Strong deposit behavior with low or no borrowing
* Excellent repayment record
* Long-term wallet activity with minimal risk
* High participation without triggering liquidation

## Summary
* **Lower scores** often reflect wallets with poor repayment or aggressive borrowing.
* **Higher scores** are reserved for wallets showing long-term, consistent, and low-risk usage patterns.

