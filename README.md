# ⚡ Electricity Data Analyzer

>  A Python-based electricity consumption analytics application with CLI and Streamlit interfaces, MySQL data storage, Pandas-based analysis, Matplotlib visualizations, and Google Gemini AI assistance.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-purple)
![Status](https://img.shields.io/badge/Status-v1.0-success)

---

# 📖 Project Overview

Electricity Data Analyzer is a Python-based application that transforms raw electricity usage data into meaningful insights.

Users can upload electricity consumption data from CSV files, store it in a MySQL database, analyze usage patterns, visualize trends, estimate electricity costs, detect anomalies, and receive AI-powered explanations using the Google Gemini API.

The project provides both a *command-line interface (CLI)* and a *Streamlit web interface*, allowing users to perform the same analytics through either the terminal or an interactive dashboard.

---

# ✨ Features

- Upload electricity usage data from CSV files
- Replace the existing dataset when a new CSV is loaded, to avoid redundancy
- Store and retrieve electricity data using MySQL
- Analyze electricity consumption trends
- Detect peak usage hours
- Estimate electricity bills
- Detect unusual consumption spikes
- Generate charts using Matplotlib
- Interactive Streamlit dashboard
- AI-powered natural language explanations using Google Gemini
- CLI-based analytics commands
- Modular and scalable project architecture
- Environment-based configuration using `.env`

---
# 🖥 Interfaces

## Command-Line Interface

The original CLI allows users to perform analytics directly from the terminal.

### Load CSV
```bash
python main.py load data/sample_usage.csv
```
## Summary
```bash
python main.py summary
```
## Trend Analysis
```bash
python main.py trend
```
## Peak Hours
```bash
python main.py peak
```
## Cost Estimation
```bash
python main.py cost
```
## Detect Anomalies
```bash
python main.py anomalies
```
## Ask the AI Assistant
```bash
python main.py ask "Why was my electricity bill high?"
```
## 🌐 Streamlit Interface

The project also includes an interactive Streamlit interface.

Run the application with:
```bash
streamlit run app.py
```

# 📂 Project Structure

```text
ElectricityDataAnalyser/
│
├── analysis/
│   ├── __init__.py
│   ├── anomalies.py
│   ├── cost.py
│   ├── peak_hours.py
│   └── trends.py
│
├── assistant/
│   ├── __init__.py
│   ├── explain.py
│   └── gemini_client.py
│
├── assets/
├── charts/
├── data/
├── db/
│   ├── __init__.py
│   ├── connection.py
│   └── schema.sql
│
├── tests/
│   ├── __init__.py
│   ├── test_explain.py
│   └── test_gemini.py
│
├── utils/
│   ├── __init__.py
│   └── loader.py
│
├── .env.example
├── config.py
├── main.py
├── app.py
├── requirements.txt
└── README.md
```
---
# ⚙️ Project Workflow

```text
                    CSV File
                       │
                       ▼
                Load into MySQL
                       │
                       ▼
                Retrieve Data
                       │
                       ▼
              Pandas / NumPy
                       │
                       ▼
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
    Data Analytics            Matplotlib
          │                    Visualizations
          │
          ▼
    Analysis Results
          │
          ▼
     Google Gemini
          │
          ▼
   Natural Language
      Explanation

The application can be accessed through either:
CLI ────────────────┐
                    │
                    ▼
              Shared Backend
                    ▲
                    │
Streamlit ──────────┘
```
---
# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Database | MySQL |
| Data Analysis | Pandas |
| Data Visualization | Matplotlib |
| AI | Google Gemini API |
| Configuration | python-dotenv |
| Version Control | Git & GitHub |

---

# 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/namrata-21-kundu/ElectricityDataAnalyser.git

cd ElectricityDataAnalyser
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Copy:

```text
.env.example
```

to

```text
.env
```

Then fill in your database credentials and Gemini API key.

### Create the database

```bash
mysql -u root -p < db/schema.sql
```

---

# 📄 Expected CSV Format

```csv
timestamp,usage_kwh
2026-01-01 00:00:00,0.42
2026-01-01 01:00:00,0.38
2026-01-01 02:00:00,0.45
```

---

# 🧠 AI Integration

The project integrates the Google Gemini API to generate human-readable explanations for electricity usage analysis.

The AI assistant can explain:

- Cost summaries
- Consumption trends
- Peak usage hours
- Anomaly detection results

It also suggests practical ways to reduce electricity consumption based on the analysis.

---

# 🚀 Roadmap

## ✅ Version 1.0 — Current

- CLI application
- Streamlit interface
- CSV upload
- MySQL integration
- Data analytics
- Trend analysis
- Peak usage detection
- Cost estimation
- Anomaly detection
- Chart generation
- AI-powered explanations using Gemini
- Environment-based configuration

## 🔄 Future Improvements

- Explore ML-based anomaly detection instead of relying only on statistical thresholds
- Interactive and more advanced visualizations
- Support for comparing multiple datasets
- Additional electricity consumption insights
---

# 👨‍💻 Author

**Namrata Kundu**    

Contact:
- GitHub: https://github.com/namrata-21-kundu
- LinkedIn: https://www.linkedin.com/in/namrata-21-kundu/

---

# 📜 License

This project is licensed under the MIT License.
