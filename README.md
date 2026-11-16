# UPI Analytics Platform – India's Digital Payments Intelligence Platform

An end-to-end data analytics and AI-powered platform for exploring India's Unified Payments Interface (UPI) transaction trends, growth patterns, and future activity.

## Project Overview

UPI Analytics Platform is an end-to-end data analytics project built using publicly available UPI transaction statistics.

The platform analyzes monthly UPI transaction volume and value from April 2024 to March 2026, using Python, MySQL, Excel, Power BI, Machine Learning, and Generative AI.

It transforms raw payment statistics into meaningful business insights through interactive dashboards, exploratory data analysis, forecasting, and an AI-powered question-answering assistant.

## Business Objectives

- Analyze monthly UPI transaction volume and value.
- Identify transaction growth patterns and trends.
- Examine changes in average transaction value.
- Analyze the number of banks live on UPI.
- Perform exploratory data analysis and identify unusual growth patterns.
- Explore future transaction trends using machine learning.
- Build an AI-powered assistant that answers questions using project knowledge.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Database | MySQL 8.0 |
| Spreadsheet Analysis | Microsoft Excel |
| Business Intelligence | Power BI, DAX |
| Machine Learning | Scikit-learn |
| Generative AI | Google Gemini |
| RAG | ChromaDB, Sentence Transformers |
| Application | Streamlit |
| Version Control | Git, GitHub |

## Project Architecture

1. **Data Collection** – Collect publicly available UPI statistics.
2. **Data Cleaning** – Process and prepare monthly transaction data using Python.
3. **Exploratory Data Analysis** – Analyze transaction trends and growth patterns.
4. **SQL Analysis** – Store and query structured data using MySQL.
5. **Excel Analysis** – Build PivotTables, charts, and KPI summaries.
6. **Power BI** – Develop interactive dashboards and DAX measures.
7. **Machine Learning** – Explore transaction forecasting and anomaly detection.
8. **AI Integration** – Build a RAG-based assistant using Gemini and ChromaDB.
9. **Application Interface** – Integrate project insights into a Streamlit application.

## Dataset Information

- **Coverage:** April 2024 – March 2026
- **Records:** 24 monthly observations
- **Geographic Scope:** India (national-level statistics)
- **Primary Source:** National Payments Corporation of India (NPCI)

### Key Dataset Fields

- Month
- Number of Banks Live on UPI
- Transaction Volume (Millions)
- Transaction Value (Crores)
- Volume Growth (%)
- Value Growth (%)
- Average Transaction Value (₹)

## Machine Learning

The project explores:

- Linear Regression for transaction volume forecasting.
- Linear Regression for transaction value forecasting.
- IQR-based anomaly detection.
- Statistical analysis of monthly transaction growth.

**Note:** The dataset contains only 24 monthly observations. Forecasting and anomaly detection are exploratory and should not be interpreted as production-grade predictions or fraud detection.

## AI-Powered Assistant

The platform includes a Retrieval-Augmented Generation (RAG) assistant.

It uses:

- Sentence Transformers for text embeddings.
- ChromaDB for vector storage and retrieval.
- Google Gemini for answer generation.
- Streamlit for the user interface.

Users can ask questions about the project and retrieve answers grounded in its knowledge base.

## Key Project Deliverables

- Python exploratory data analysis.
- MySQL database and SQL analysis.
- Excel analytical workbook and dashboard.
- Power BI interactive dashboard.
- Machine learning forecasting notebook.
- RAG-based AI assistant.
- Streamlit web application.

## Project Status

**Core development completed.**

The analytics, database, dashboards, exploratory machine learning, and AI assistant components have been implemented.

Further improvements may include AI response-time optimisation, interface polishing, and expanded datasets.

## Data Sources

- National Payments Corporation of India (NPCI)
- Reserve Bank of India (RBI)

## Author

**Sanjay Renukuntla**

---

# 📸 Project Screenshots

## 1. Overview Dashboard

![Overview 1](screenshots/overview%281%29.png)

![Overview 2](screenshots/overview%282%29.png)

![Overview 3](screenshots/overview%283%29.png)

## 2. Transaction Trends

![Transaction Trends 1](screenshots/transaction%20trends%281%29.png)

![Transaction Trends 2](screenshots/transaction%20trends%282%29.png)

![Transaction Trends 3](screenshots/transaction%20trends%283%29.png)

![Transaction Trends 4](screenshots/transaction%20trends%284%29.png)

## 3. Forecast Analysis

![Forecast Analysis 1](screenshots/forecast%20analysis%281%29.png)

![Forecast Analysis 2](screenshots/forecast%20analysis%282%29.png)

## 4. Raw Data Explorer

![Raw Data](screenshots/raw%20data.png)

## 5. AI Assistant

![AI Assistant](screenshots/AI%20Assistant.png)
