# ⚡ Electricity Data Analyzer

A Python-based data analytics application that helps users understand their electricity consumption through data analysis and AI-powered insights. Users can upload electricity usage data, store it in MySQL, visualize consumption patterns, estimate electricity costs, detect unusual usage, and ask natural-language questions using an AI assistant.

---

# 📖 Description

Electricity Data Analyzer is a CLI-based analytics tool built using Python. It allows users to upload electricity consumption data in CSV format, store it in a MySQL database, and generate useful insights through data analysis and visualization.

The project uses SQL, Pandas, NumPy, and Matplotlib to analyze electricity usage and integrates the Gemini API to explain results in simple, natural language. The goal is to transform raw electricity data into meaningful insights that help users better understand their consumption patterns.

---

# ✨ Features

- Upload electricity usage data from CSV files
- Store data in a MySQL database
- Analyze electricity consumption trends
- Identify peak usage hours
- Estimate electricity costs
- Detect unusual consumption spikes
- Generate charts automatically
- Ask questions in natural language using AI
- Modular and easy-to-expand project structure

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Database | MySQL |
| Data Analysis | Pandas, NumPy |
| Data Visualization | Matplotlib |
| AI Integration | Google Gemini API |
| Environment Variables | python-dotenv |
| Version Control | Git & GitHub |

---

# ⚙️ Project Workflow

```
CSV File
    ↓
Load data into MySQL
    ↓
Python retrieves the data
    ↓
Pandas & NumPy perform analysis
    ↓
Matplotlib generates charts
    ↓
User asks a question
    ↓
Gemini API generates a natural-language explanation
```

---

# 📁 Project Structure

```
electricity-intelligence-agent/
│
├── main.py
├── db/
│   ├── connection.py
│   └── schema.sql
├── analysis/
│   ├── trends.py
│   ├── peak_hours.py
│   ├── cost.py
│   └── anomalies.py
├── agent/
│   ├── router.py
│   └── explain.py
├── charts/
├── requirements.txt
└── README.md
```

---

# 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/electricity-intelligence-agent.git

cd electricity-intelligence-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up MySQL

```bash
mysql -u root -p < db/schema.sql
```

### 4. Configure environment variables

Create a `.env` file in the project folder.

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=electricity_agent

GEMINI_API_KEY=your_api_key
```

---

# ▶️ Usage

### Load electricity usage data

```bash
python main.py load usage_data.csv
```

### View consumption trends

```bash
python main.py trend
```

### Find peak usage hours

```bash
python main.py peak
```

### Generate estimated cost

```bash
python main.py cost
```

### Detect unusual electricity usage

```bash
python main.py anomalies
```

### Ask the AI assistant

```bash
python main.py ask "Why was my electricity bill high this month?"
```

---

# 📂 Expected CSV Format

```csv
timestamp,usage_kwh
2026-01-01 00:00:00,0.42
2026-01-01 01:00:00,0.38
2026-01-01 02:00:00,0.45
...
```

---

# 📈 Sample Output

```
$ python main.py trend

Chart saved to charts/monthly_trend.png

Total Usage: 342 kWh
Estimated Cost: ₹2,850
```

```
$ python main.py peak

Chart saved to charts/peak_hours.png

Peak Usage Hours:
7 PM – 9 PM
Average Consumption: 2.1 kWh/hour
```

---

# 🚀 Future Enhancements

- Convert the CLI application into a web application using Flask or FastAPI
- Add an interactive dashboard for real-time visualization
- Support multiple users and electricity meters
- Improve the AI agent with tool calling and conversation memory
- Add electricity usage forecasting and bill prediction
- Deploy the application to a cloud platform

---

# 👨‍💻 Autho

**Namrata Kundu**

**LinkedIn:** *https://www.linkedin.com/in/namrata-21-kundu/*

**GitHub:** *https://github.com/namrata-21-kundu*
