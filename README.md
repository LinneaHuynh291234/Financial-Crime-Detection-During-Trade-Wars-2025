# Fraud Detection on Trade-Based Money Laundering (TBML)  
**Simulated Data – Nordea Open Banking Format**

A data science project simulating and detecting trade-based money laundering (TBML) in Nordic banking transactions. This project uses simulated data based on the **Nordea Open Banking API** format and integrates dynamic currency conversion through the **Riksbanken API**.

### Project Inspiration
This project is inspired by the study:  
**Ferwerda, Joras (2019). "Tariffs, Sanctions and the Problem of Trade-Based Money Laundering". European Studies on Crime and Criminal Justice.**

---

## 🧾 Project Overview

This project aims to simulate real-world trade-based money laundering activities in corporate cross-border payments. Key objectives include detecting patterns of illicit trade using transactional data and applying fraud detection methods for suspicious behavior in banking.

### Key Goals:
- Simulate 10,000 corporate transactions in the Nordic banking market (SEK, DKK, NOK).
- Identify red flags linked to trade-based money laundering (TBML) such as:
  - Unusual turnover spikes
  - Payments made to sanctioned or high-risk counterparties
  - Splitting Payment
- Feature Engineering: Turnover jump %, payment splitting, risky country exposure, and more.
- Use the *Riksbanken API* to convert transaction amounts to EUR for consistency in analysis and decision-making.

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

## 💾 Data Collection

The data used in this project is simulated and represents typical corporate transactions across Nordic countries. The following fields are included:
- `transaction_id`
- `currency`
- `booking_date`, `transaction_date`, `payment_date`
- `type_description`, `narrative`, `counterparty_name`
- `amount` (converted to EUR using Riksbanken API)
- **Additional engineered features** such as turnover jump %, risk_flag, and more.
