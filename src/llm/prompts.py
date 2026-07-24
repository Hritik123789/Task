def log_summary_prompt(logs):
    """Generate plain-English summary of log entries."""
    log_text = "\n".join([f"- {log['plate_number']} at {log['timestamp']} (confidence: {log['confidence']:.2f})" for log in logs])
    return f"""Summarize these vehicle entries in plain English:

{log_text}

Provide a clear, concise summary."""

def whitelist_alert_prompt(violations):
    """Alert for vehicles not on whitelist."""
    violation_text = "\n".join([f"- {v['plate_number']} at {v['timestamp']}" for v in violations])
    return f"""These vehicles are NOT on the whitelist:

{violation_text}

Flag them as security alerts."""

def qa_prompt(question, relevant_logs):
    """Answer user question based on log data."""
    log_text = "\n".join([f"- {log['plate_number']} at {log['timestamp']}" for log in relevant_logs])
    return f"""Based on these vehicle log entries:

{log_text}

Question: {question}

Answer the question directly using only the information provided."""
