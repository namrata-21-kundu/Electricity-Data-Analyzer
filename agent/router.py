from analysis.trends import get_data, calculate_summary
from analysis.cost import get_cost_summary
from analysis.peak_hours import get_peak_hours
from analysis.anomalies import detect_anomalies

def route_query(question):
    question = question.lower()

    if "bill" in question or "cost" in question:
        return get_cost_summary()
    elif "peak" in question or "hour" in question:
        return get_peak_hours()
    elif "anomaly" in question or "spike" in question:
        return detect_anomalies()
    elif "trend" in question or "usage" in question:
        df = get_data()
        return calculate_summary(df)
    else:
        return{
            "message" : "sorry, could not understand the question"
        }
    
    