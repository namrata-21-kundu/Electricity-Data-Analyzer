import os
import sys
import tempfile
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Ensure environment variables from .env take precedence
load_dotenv(override=True)
#if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
  #  os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Backend imports (unchanged backend logic)
from db.connection import connect_db
from utils.loader import load_csv
from analysis.trends import get_data, calculate_summary, plot_trend
from analysis.peak_hours import get_peak_hours
from analysis.cost import get_cost_summary
from analysis.anomalies import detect_anomalies
from assistant.router import route_query
from assistant.explain import explain
from config import RATE_PER_UNIT, GEMINI_MODEL

# Configure Streamlit Page
st.set_page_config(
    page_title="Electricity Data Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 1.8rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.25);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #ffffff !important;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.05rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .metric-card {
        background-color: var(--background-color, #ffffff);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.25rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    
    .ai-response-box {
        background: linear-gradient(180deg, rgba(248, 250, 252, 0.8) 0%, rgba(241, 245, 249, 0.8) 100%);
        border: 1px solid #cbd5e1;
        border-left: 5px solid #3b82f6;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .chart-container {
        background-color: #ffffff;
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 14px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .badge-status {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-success {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
    }
</style>
""", unsafe_allow_html=True)


def check_db_health():
    """Verify database connection and return record count."""
    try:
        conn = connect_db()
        if conn is None:
            return False, 0
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM readings")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return True, count
    except Exception as e:
        return False, 0


# Header Banner
st.markdown("""
<div class="main-header">
    <h1>⚡ Electricity Data Analyzer</h1>
    <p>Upload consumption readings, explore usage trends, and get AI-powered energy insights powered by MySQL & Google Gemini.</p>
</div>
""", unsafe_allow_html=True)

# Check DB health
db_ok, row_count = check_db_health()

# Sidebar
with st.sidebar:
    st.subheader("⚙️ System Status")
    if db_ok:
        st.markdown('<span class="badge-status badge-success">● MySQL Connected</span>', unsafe_allow_html=True)
        st.caption(f"Current Records in DB: **{row_count:,} rows**")
    else:
        st.markdown('<span class="badge-status badge-warning">⚠ MySQL Disconnected</span>', unsafe_allow_html=True)
        st.warning("Please ensure MySQL server is running and database `electricity_analytics` exists.")

    st.markdown("---")
    st.subheader("💡 Configuration")
    st.info(f"**Tariff Rate:** ₹{RATE_PER_UNIT} per kWh\n\n**AI Model:** `{GEMINI_MODEL}`")
    
    st.markdown("---")
    st.subheader("⚡ Quick Load Sample Data")
    sample_file_path = os.path.join("data", "sample_usage.csv")
    if os.path.exists(sample_file_path):
        if st.button("📥 Load Built-in sample_usage.csv", use_container_width=True):
            try:
                load_csv(sample_file_path)
                st.success("Successfully loaded sample_usage.csv into MySQL!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load sample data: {e}")
    
    st.markdown("---")
    st.caption("Electricity Data Analyzer v2.0 • Streamlit Edition")

# Navigation Tabs matching requested architecture
tab_upload, tab_options, tab_assistant = st.tabs([
    "📁 1. Upload CSV",
    "📊 2. Select Option (Analytics)",
    "🤖 3. Ask Question (AI Assistant)"
])

# ==========================================
# TAB 1: UPLOAD CSV
# ==========================================
with tab_upload:
    st.subheader("Upload Electricity Consumption Data")
    st.write("Upload a CSV file containing electricity meter readings. Expected format: `timestamp` and `usage_kwh` columns.")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            help="File must contain timestamp and usage_kwh headers."
        )

        if uploaded_file is not None:
            try:
                # Read uploaded file for preview
                df_preview = pd.read_csv(uploaded_file)
                st.markdown("#### 📋 Data Preview")
                st.dataframe(df_preview.head(10), use_container_width=True)

                # Validation
                required_cols = {"timestamp", "usage_kwh"}
                has_cols = required_cols.issubset(set(df_preview.columns))

                if not has_cols:
                    st.error(f"❌ Missing required columns! Found: {list(df_preview.columns)}. Expected: ['timestamp', 'usage_kwh']")
                else:
                    st.success(f"✅ Valid format! {len(df_preview)} rows ready for insertion.")
                    
                    if st.button("🚀 Load into MySQL Database", type="primary", use_container_width=True):
                        with st.spinner("Inserting records into MySQL database..."):
                            # Save to temporary file to pass to backend load_csv without modifying loader.py
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                                uploaded_file.seek(0)
                                tmp.write(uploaded_file.read())
                                tmp_path = tmp.name

                            try:
                                load_csv(tmp_path)
                                st.success(f"🎉 Successfully inserted {len(df_preview)} rows into the MySQL database!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error executing load_csv: {e}")
                            finally:
                                if os.path.exists(tmp_path):
                                    os.remove(tmp_path)

            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

    with col2:
        st.markdown("#### ℹ️ Expected CSV Format")
        st.code("""timestamp,usage_kwh
2026-01-01 00:00:00,0.42
2026-01-01 01:00:00,0.38
2026-01-01 02:00:00,0.45
2026-01-01 03:00:00,0.40""", language="csv")

        st.markdown("#### 🗄️ Database Quick View")
        if db_ok and row_count > 0:
            st.metric("Total Stored Readings", f"{row_count:,} rows")
            with st.expander("View latest 5 rows in database"):
                try:
                    df_current = get_data()
                    st.dataframe(df_current.tail(5), use_container_width=True)
                except Exception as e:
                    st.error(f"Could not fetch current data: {e}")
        else:
            st.warning("Database currently has 0 rows. Upload a CSV or use the sample data from sidebar.")


# ==========================================
# TAB 2: SELECT OPTION (ANALYTICS)
# ==========================================
with tab_options:
    st.subheader("Select Analytical Option")
    
    if not db_ok or row_count == 0:
        st.warning("⚠️ No data found in the database. Please upload a CSV in Step 1 first!")
    else:
        option = st.selectbox(
            "Choose analysis module to execute:",
            [
                "📈 Summary Statistics",
                "📉 Electricity Usage Trend",
                "⏰ Peak Usage Hours",
                "💰 Cost & Bill Estimation",
                "🚨 Anomaly Detection",
                "🔍 All-in-One Analytics View"
            ],
            index=0
        )

        st.markdown("---")

        if option == "📈 Summary Statistics":
            st.markdown("### 📈 Consumption Summary")
            with st.spinner("Calculating summary from MySQL readings..."):
                df = get_data()
                summary = calculate_summary(df)

                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                kpi1.metric("Total Consumption", f"{summary['total_usage']:.2f} kWh")
                kpi2.metric("Average Usage", f"{summary['average_usage']:.2f} kWh")
                kpi3.metric("Peak Single Reading", f"{summary['maximum_usage']:.2f} kWh")
                kpi4.metric("Lowest Reading", f"{summary['minimum_usage']:.2f} kWh")

                st.markdown("#### 📄 Detailed Readings")
                st.dataframe(df, use_container_width=True)

        elif option == "📉 Electricity Usage Trend":
            st.markdown("### 📉 Usage Trend Analysis")
            with st.spinner("Generating trend visualization..."):
                df = get_data()
                plot_trend(df)
                
                chart_path = os.path.join("charts", "trend.png")
                if os.path.exists(chart_path):
                    st.image(chart_path, caption="Electricity Usage Trend Over Time", use_container_width=True)
                else:
                    st.error("Chart could not be found.")

        elif option == "⏰ Peak Usage Hours":
            st.markdown("### ⏰ Peak Usage Hours")
            with st.spinner("Analyzing peak consumption hours..."):
                peak_result = get_peak_hours()
                
                p_col1, p_col2 = st.columns(2)
                p_col1.metric("Peak Hour of the Day", f"{peak_result['peak_hour']}:00 hrs")
                p_col2.metric("Average Peak Usage", f"{peak_result['average_usage']:.2f} kWh")

                chart_path = os.path.join("charts", "peak_hours.png")
                if os.path.exists(chart_path):
                    st.image(chart_path, caption="Average Hourly Electricity Usage", use_container_width=True)

        elif option == "💰 Cost & Bill Estimation":
            st.markdown("### 💰 Cost & Bill Estimation")
            with st.spinner("Calculating cost summary..."):
                cost_result = get_cost_summary()

                c_col1, c_col2, c_col3 = st.columns(3)
                c_col1.metric("Total Units (kWh)", f"{cost_result['total_units']:.2f} kWh")
                c_col2.metric("Tariff Rate", f"₹{cost_result['rate_per_unit']} / unit")
                c_col3.metric("Estimated Total Bill", f"₹{cost_result['estimated_cost']:.2f}")

                chart_path = os.path.join("charts", "cost_breakdown.png")
                if os.path.exists(chart_path):
                    st.image(chart_path, caption="Consumption vs Estimated Cost", use_container_width=True)

        elif option == "🚨 Anomaly Detection":
            st.markdown("### 🚨 Consumption Anomaly Detection")
            with st.spinner("Scanning readings for anomalies..."):
                anomaly_result = detect_anomalies()
                anomalies = anomaly_result["anomalies"]
                threshold = anomaly_result["threshold"]

                a_col1, a_col2 = st.columns(2)
                a_col1.metric("Anomaly Threshold (Mean + 2σ)", f"{threshold:.2f} kWh")
                a_col2.metric("Detected Anomalies", f"{len(anomalies)} events")

                if anomalies:
                    st.warning(f"⚠️ Detected {len(anomalies)} abnormal consumption spike(s) exceeding {threshold:.2f} kWh:")
                    df_anomalies = pd.DataFrame(anomalies)
                    st.dataframe(df_anomalies, use_container_width=True)
                else:
                    st.success("✅ No consumption anomalies detected above threshold.")

                chart_path = os.path.join("charts", "anomalies.png")
                if os.path.exists(chart_path):
                    st.image(chart_path, caption="Anomaly Detection Plot", use_container_width=True)

        elif option == "🔍 All-in-One Analytics View":
            st.markdown("### 🔍 Comprehensive Analytics Overview")
            with st.spinner("Loading comprehensive analysis..."):
                df = get_data()
                summary = calculate_summary(df)
                cost = get_cost_summary()
                peak = get_peak_hours()
                anom = detect_anomalies()

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Total Usage", f"{summary['total_usage']:.2f} kWh")
                k2.metric("Estimated Bill", f"₹{cost['estimated_cost']:.2f}")
                k3.metric("Peak Hour", f"{peak['peak_hour']}:00")
                k4.metric("Anomalies", f"{len(anom['anomalies'])}")

                col_left, col_right = st.columns(2)
                with col_left:
                    plot_trend(df)
                    st.image(os.path.join("charts", "trend.png"), caption="Trend", use_container_width=True)
                    st.image(os.path.join("charts", "peak_hours.png"), caption="Peak Hours", use_container_width=True)

                with col_right:
                    st.image(os.path.join("charts", "cost_breakdown.png"), caption="Cost Breakdown", use_container_width=True)
                    st.image(os.path.join("charts", "anomalies.png"), caption="Anomalies", use_container_width=True)


# ==========================================
# TAB 3: ASK QUESTION (GEMINI AI ASSISTANT)
# ==========================================
with tab_assistant:
    st.subheader("🤖 AI Electricity Consumption Assistant")
    st.write("Ask natural language questions about your electricity consumption, costs, peak hours, or anomalies. Gemini AI will analyze the backend data and explain the results.")

    # Quick prompt buttons
    st.markdown("**Quick Prompts:**")
    prompt_cols = st.columns(4)
    quick_questions = [
        "Why was my electricity bill high?",
        "When are my peak hours?",
        "Were there any abnormal usage spikes?",
        "What is my overall consumption trend?"
    ]
    
    selected_quick_q = None
    for i, col in enumerate(prompt_cols):
        if col.button(quick_questions[i], key=f"q_{i}", use_container_width=True):
            selected_quick_q = quick_questions[i]

    # Question Input
    default_text = selected_quick_q if selected_quick_q else ""
    question = st.text_input(
        "Enter your question:",
        value=default_text,
        placeholder="e.g. Why is my electricity bill so high?"
    )

    if st.button("💬 Ask Assistant", type="primary"):
        if not question.strip():
            st.warning("Please type a question or choose one of the quick prompts above.")
        else:
            with st.spinner("Analyzing consumption data and querying Google Gemini..."):
                try:
                    # Backend routing and AI explanation (calling existing unchanged logic)
                    analysis = route_query(question)
                    answer = explain(question, analysis)

                    st.markdown("### 🤖 AI Explanation")
                    st.markdown(f"""
<div class="ai-response-box">
    {answer}
</div>
""", unsafe_allow_html=True)

                    with st.expander("🔍 View Raw Backend Analysis Data"):
                        st.json(analysis)

                except Exception as e:
                    st.error(f"Failed to generate explanation: {e}")
                    st.info("Tip: Verify your Gemini API credentials and database status.")
