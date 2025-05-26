# Fraud Detection on Trade-Based Money Laundering (TBML)  
### 🧾 Project Overview

This data science project simulates and detects **Trade-Based Money Laundering (TBML)** in corporate banking transactions, focusing on behavioral patterns that emerge during **tariff and sanctions-related tension** (e.g., China vs US).

### 🕒 Simulation Context

- **Date Range**: Simulated data covers the period from **2025-04-02 to 2025-12-31**
- **Scenario Assumption**:  In mid-2025, a trade war escalation introduces new tariffs and restrictions, leading to unusual or suspicious transaction patterns.

### Project Inspiration
This project is inspired by the study:  
**Ferwerda, Joras (2019). "Tariffs, Sanctions and the Problem of Trade-Based Money Laundering". European Studies on Crime and Criminal Justice.**

---

### Key Goals:
- Simulate more than 10,000 corporate transactions in the Nordic banking market (SEK, DKK, NOK).
- Use the *Riksbanken API* to convert transaction amounts to EUR for consistency in analysis and decision-making.
- Identify red flags linked to trade-based money laundering (TBML) such as:
  - Unusual turnover spikes
  - Payments made to sanctioned or high-risk counterparties
  - Splitting Payment
- Perform EDA using various statistical and visualization techniques
- Feature Engineering.
-Baseline Model Training.

---

## 🔧 Tools and Technologies

- **Python** (Pandas, NumPy, Scikit-learn) for data processing and modeling.
- **SQL** (SQLite3) for transaction aggregation and analysis.
- **Riksbanken API** for dynamic currency conversion to EUR.
- **Jupyter Notebooks** for exploratory data analysis (EDA) and model development.
- **Nordea Open Banking API** data format used for simulating realistic transactions.

---

## 🔍 Features Engineered
- **Turnover Jump %**: Detect sudden increases in transaction amounts for a given account.
- **Risky Country Flag**: Identify payments made to high-risk countries (e.g., US, countries under sanction).
- **Payment Splitting**: Identify patterns of multiple payments to the same counterpart within a short timeframe.

---
