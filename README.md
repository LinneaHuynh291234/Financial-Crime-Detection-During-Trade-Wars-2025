# Fraud Detection - Corporate Banking Transactions

### 🧾 Project Overview

As a **Proof of Concept (PoC)**, this data science project aims to detect potential fraudulent transactions in corporate banking. It reflects my deepening interest in **Financial Crime Prevention**, especially in the context of evolving geopolitical risks that may increase suspicious transaction activities.

### 🕒 Simulation Context

| Item           | Detail                                                                                      |
|----------------|---------------------------------------------------------------------------------------------|
| **Date range** | **2025‑04‑02 → 2025‑12‑31**                                                                |
| **Scenario**   | A hypothetical trade tension escalation in mid-2025 triggers increased abnormal payment behavior. |
| **Currencies** | SEK, DKK, NOK → **converted to EUR** in-flight using the **Riksbanken API**.                |
| **Volume**     | **10,716** transactions (≈ 3% labeled as suspicious).                                       |
| **Risk Scoring** | Not included in this PoC project; dataset uses binary `is_fraud` labels to indicate suspicious transactions.|                                                     

---

## 🎯 Objectives

1. **Generate realistic Nordic transaction data** (Nordea API schema).  
2. **Engineer risk indicators:**  
   - Turnover jump %.  
   - Payments to risky countries.  
   - Payment splitting detection:  
     - Multiple payments within a single day.  
     - Repeated or similar transaction amounts.  
     - High frequency of payments above a threshold.  
3. **Detect suspicious payments using:**  
   - Logistic Regression & Random Forest (supervised).  
   - Isolation Forest (unsupervised).  
4. **Document a repeatable workflow:**  
   - Data Collection: Gather data from `AML_KYC_risk_assessment_report` and `Nordic_transaction_report`, then merge them into a unified dataset for analysis.
   - Data Cleaning: Currency conversion, duplicate removal.  
   - EDA: Descriptive and uni-/bivariate analysis.  
   - Feature Engineering: Handling missing data, feature creation, transformation, scaling.  
   - Model Training: Logistic Regression, Random Forest, Isolation Forest.  
   - Evaluation: Precision-Recall, ROC-AUC, confusion matrix, feature importance.  

---

## 🔧 Tools and Technologies

- **Python** (Pandas, NumPy, Scikit-learn) for data processing and modeling  
- **SQL** (SQLite3) for transaction aggregation and analysis  
- **Riksbanken API** for dynamic currency conversion to EUR  
- **Jupyter Notebooks** for EDA and model development  
- **Nordea Open Banking API** data format for realistic transaction simulation  
