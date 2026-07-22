import requests
from datetime import datetime

def log_to_google_sheet(job_title, company, ats_score, status="Applied"):
    """
    Dispatches parsed job profile information directly to the Google Sheet using Apps Script Webhook URL.
    """
    # ✅ Paste your real script URL exactly like this inside the quotes
    WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbz8FJBKLMDJ_F6NrPzA4bcW5JDMHYgpDVj-2x73QtAfRfj9eNMGFb5ybz7e2y0cLPlOKg/exec"
    
    if WEBHOOK_URL == "https://script.google.com/macros/s/AKfycbzUpSZRD1pq4-3fVqW8Q5xg2GtEzrFN042RREOeLSBF/dev":
        print("❌ Error: Missing Google Apps Script Web App URL in sheets_logger.py.")
        return False

    current_date = datetime.now().strftime("%d/%m/%Y")
    
    payload = {
        "task_name": f"{job_title} at {company}",
        "task_type": "Automated Apply",
        "assigned_to": "Tejas AI Agent",
        "planned_date": current_date,
        "actual_date": current_date,
        "status": status,
        "score": f"{ats_score * 100:.2f}%"
    }
    
    try:
        print("📤 Sending tracking data to Google Sheet ledger via Webhook...")
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            print(f"📊 Cloud Sync Success! Logged entry for {job_title} into Google Sheets.")
            return True
        else:
            print(f"❌ Cloud Sheet Synchronization Failed. HTTP Status Code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets Endpoint: {e}")
        return False