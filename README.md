# Anomaly-Based Fraud Prevention in Transaction Monitoring

### 🧾 Project Overview

As a **Proof of Concept (PoC)**, this data science project focuses on detecting potentially fraudulent transactions. It reflects my growing interest in **Financial Crime Prevention**, particularly under conditions of heightened **geopolitical risk**, where abnormal payment activity may increase.

---
## 🔍 🎯 Objectives

1. **Generate realistic Nordic transaction data:** (Nordea API schema)

🕒 Simulation Context

| Item           | Detail                                                                                      |
|----------------|---------------------------------------------------------------------------------------------|
| **Date range** | **2025‑04‑02 → 2025‑07‑02**                                                                |
| **Scenario**   | A hypothetical trade tension escalation in mid-2025 triggers increased abnormal payment behavior. |
| **Currencies** | SEK, DKK, NOK → **converted to EUR** in-flight using the **Riksbanken API**.       |
| **Volume**     | **10,716** transactions (31 Categorical, 9 Numeric). Formatted according to the **PSD2 Open Banking API.                 |

2. **Develop domain expertise in Transaction Monitoring Systems.**

- Developed an understanding of how **Transaction Monitoring Systems (TMS)** function within financial institutions.  
- Discovered how **AI can enhance traditional TMS** by addressing key challenges:

| ⚠️ **Challenge**                               | ✅ **Takeaway**                                                                                      |
|------------------------------------------------|------------------------------------------------------------------------------------------------------|
| Static rule-based systems                      | Combine rule-based logic with AI models for personalization and self-learning → lower false positives. |
| Outdated monitoring scenarios                  | Use AI to automatically learn and suggest scenario tuning based on evolving transaction behavior.    |
| Manual reporting & long investigation times    | Automate alerts with clear explanations, aligned with SAR standards to speed up investigations.      |

3. **Document a repeatable workflow:**

![Workflow](images/visual-selection.png)
---

## 🔧 Tools and Technologies

- **Python** (Pandas, NumPy, Scikit-learn) for data processing and modeling  
- **SQL** (SQLite3) for transaction aggregation and analysis  
- **Riksbanken API** for dynamic currency conversion to EUR  
- **Jupyter Notebooks** for EDA and model development  
- **Nordea Open Banking API** data format for realistic transaction simulation  
