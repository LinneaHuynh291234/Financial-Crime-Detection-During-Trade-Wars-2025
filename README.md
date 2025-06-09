# Anomaly-Based Fraud Prevention in Transaction Monitoring Systems

### 🧾 Project Overview

As a **Proof of Concept (PoC)**, this data science project focuses on detecting potentially fraudulent transactions. It reflects my growing interest in **Financial Crime Prevention**, particularly under conditions of heightened **geopolitical risk**, where abnormal payment activity may increase.

### 🕒 Simulation Context

| Item           | Detail                                                                                      |
|----------------|---------------------------------------------------------------------------------------------|
| **Date range** | **2025‑04‑02 → 2025‑07‑02**                                                                |
| **Scenario**   | A hypothetical trade tension escalation in mid-2025 triggers increased abnormal payment behavior. |
| **Currencies** | SEK, DKK, NOK → **converted to EUR** in-flight using the **Riksbanken API**.                |
| **Volume**     | **10,716** transactions.                                                                    |

---

## 🎯 Objectives

1. **Generate realistic Nordic transaction data:** (Nordea API schema)

- Simulate 10,716 Nordic banking transactions in the Nordea Open Banking API format.  
- Convert currencies using the Riksbanken API to maintain consistent transaction values.

2. **Gain domain knowledge in TMS workflow:**

- Developed an understanding of how Transaction Monitoring Systems operate in financial institutions.  
- Learned key steps in transaction data processing, anomaly detection, and alert generation.  
- Explored how risk indicators and scoring models integrate into daily monitoring workflows.  
- Studied regulatory requirements and compliance considerations affecting TMS design.  
- Applied this knowledge to improve feature engineering and model tuning for better fraud detection.

3. **Document a repeatable workflow:**

- Data Collection: Merge data from transactional records, KYC customer profiles, and summary statistics into a unified dataset.  
- Data Cleaning: Currency conversion and duplicate removal.  
- Exploratory Data Analysis: Descriptive statistics, uni- and bivariate analyses.  
- Feature Engineering: Handle missing values, create new features, apply transformations and scaling.  
- Anomaly Scoring: Apply tree-based anomaly detection models.  
- Score Combination: Combine individual anomaly scores using ensemble methods.  
- Evaluation: Use metrics such as Precision-Recall curves, ROC-AUC, confusion matrix, and analyze feature importance.

---

## 🔧 Tools and Technologies

- **Python** (Pandas, NumPy, Scikit-learn) for data processing and modeling  
- **SQL** (SQLite3) for transaction aggregation and analysis  
- **Riksbanken API** for dynamic currency conversion to EUR  
- **Jupyter Notebooks** for EDA and model development  
- **Nordea Open Banking API** data format for realistic transaction simulation  
