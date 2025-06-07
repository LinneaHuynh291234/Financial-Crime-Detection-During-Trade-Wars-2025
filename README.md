# Fraud Detection - Corporate Banking Transactions

### 🧾 Project Overview

This project is a **Proof of Concept (PoC)** aimed at detecting potential financial crime in corporate banking transactions. It reflects my growing interest in financial crime prevention, particularly in the context of evolving geopolitical risks. 

### 🕒 Simulation Context

| Item           | Detail                                                                                      |
|----------------|---------------------------------------------------------------------------------------------|
| **Date range** | **2025‑04‑02 → 2025‑12‑31**                                                                |
| **Scenario**   | A hypothetical trade tension escalation in mid-2025 triggering abnormal payment behavior.  |
| **Currencies** | SEK, DKK, NOK → **converted to EUR** in-flight using the **Riksbanken API**.                |
| **Volume**     | **10,716** transactions (≈ 3% labeled as suspicious).                                       |
| **Risk Scoring** | Not included in this PoC; dataset uses binary `is_fraud` labels to indicate suspicious transactions.|                                                     

---

## 🎯 Objectives

1. **Generate** realistic Nordic transaction data (Nordea API schema).  
2. **Engineer risk indicators:**  
   - Turnover jump %  
   - Payments to risky countries  
   - Payment splitting detection:  
     - Multiple payments within a single day  
     - Repeated or similar transaction amounts  
     - High frequency of payments above a threshold  
3. **Detect** suspicious payments using:  
   - Logistic Regression & Random Forest (supervised)  
   - Isolation Forest (unsupervised)  
4. **Document** a repeatable workflow:  
   - Data Collection: AML_KYC_risk_assessment_report & Nordic_transaction_report  
   - Data Cleaning: Currency conversion, duplicate removal  
   - EDA: Descriptive and uni-/bivariate analysis  
   - Feature Engineering: Handling missing data, feature creation, transformation, scaling  
   - Model Training: Logistic Regression, Random Forest, Isolation Forest  
   - Evaluation: Precision-Recall, ROC-AUC, confusion matrix, feature importance  

---

## 🔧 Tools and Technologies

- **Python** (Pandas, NumPy, Scikit-learn) for data processing and modeling  
- **SQL** (SQLite3) for transaction aggregation and analysis  
- **Riksbanken API** for dynamic currency conversion to EUR  
- **Jupyter Notebooks** for EDA and model development  
- **Nordea Open Banking API** data format for realistic transaction simulation  
