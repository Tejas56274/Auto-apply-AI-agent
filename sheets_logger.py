import requests
from datetime import datetime

def _is_valid_webhook(url: str) -> bool:
    """Return True if *url* looks like a Google Apps Script webhook URL.

    The expected pattern is:
        https://script.google.com/macros/s/<SCRIPT_ID>/exec
    This simple check avoids accidental usage of placeholder strings while
    keeping the function lightweight and dependency‑free.
    """
    return isinstance(url, str) and url.startswith("https://script.google.com/macros/s/") and url.rstrip("/").endswith("/exec")

def log_to_google_sheet(job_title: str, company: str, ats_score: float, status: str = "Applied") -> bool:
    """Send a job application record to a Google Sheet via Apps Script webhook.

    Parameters
    ----------
    job_title: str
        Title of the job being logged.
    company: str
        Name of the hiring company.
    ats_score: float
        Matching score (0.0‑1.0) produced by the ATS model.
    status: str, optional
        Current status of the application; defaults to "Applied".

    Returns
    -------
    bool
        ``True`` if the request succeeded (HTTP 200), ``False`` otherwise.
    """
    # ✅ Paste your real script URL exactly like this inside the quotes
    WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbz8FJBKLMDJ_F6NrPzA4bcW5JDMHYgpDVj-2x73QtAfRfj9eNMGFb5ybz7e2y0cLPlOKg/exec"

    if not _is_valid_webhook(WEBHOOK_URL):
        print("❌ Error: Invalid or missing Google Apps Script Webhook URL in sheets_logger.py.")
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
        print(f"❌ Cloud Sheet Synchronization Failed. HTTP Status Code: {response.status_code}")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets Endpoint: {e}")
        return False
    