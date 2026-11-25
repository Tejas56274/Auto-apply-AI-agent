import os
import PyPDF2
import requests


def extract_text_from_resume(pdf_path):
    """Extract raw text from a local PDF resume.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str | None: Extracted text on success, otherwise ``None``.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        print("✅ Resume text successfully extracted!")
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None


def fetch_live_jobs(query="Data Scientist in India", num_pages=1):
    """Fetch active job listings from the JSearch V2 API.

    The function first attempts a live API call. If the request fails or the
    response is not successful, a static mock list is returned so that the demo
    continues to work without exposing credentials.

    Args:
        query (str): Search query string.
        num_pages (int): Number of result pages to request.

    Returns:
        list[dict]: A list of job dictionaries.
    """
    url = "https://jsearch.p.rapidapi.com/search-v2"

    querystring = {
        "query": query,
        "num_pages": str(num_pages),
        "country": "us",
        "date_posted": "all",
    }

    # Retrieve the RapidAPI key from the environment instead of hard‑coding it.
    api_key = os.getenv("JSEARCH_API_KEY")
    if not api_key:
        print(
            "⚠️ JSEARCH_API_KEY not set in environment. "
            "Falling back to mock job data."
        )
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": api_key or "",
    }

    try:
        print(f"🔍 Fetching jobs for query: '{query}'...")
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            job_data = response.json()
            jobs_list = job_data.get("data", [])
            print(f"✅ Successfully fetched {len(jobs_list)} jobs from Live API!")
            return jobs_list
        else:
            print(
                f"⚠️ Live API returned status {response.status_code}. "
                "Activating mock job directory for demo..."
            )
    except Exception as e:
        print(f"❌ Network error while contacting JSearch API: {e}")

    # Mock fallback – static demo data
    mock_jobs = [
        {
            "job_title": "Data Science Intern",
            "employer_name": "Deloitte India",
            "job_description": (
                "We are seeking a 3rd year engineering student for a Data Science role. "
                "Requirements: Hands‑on experience building stock prediction systems, "
                "Machine Learning modeling, Neural Networks, TensorFlow, and Python scripting. "
                "Experience with dashboard tools like Tableau is a huge plus."
            ),
        },
        {
            "job_title": "Junior Data Analyst",
            "employer_name": "TCS Bangalore",
            "job_description": (
                "Looking for fresh graduates with proficiency in Core Python, SQL databases, "
                "and Excel dashboards. Understanding of deep learning or NLP model deployment "
                "is good to have but not mandatory."
            ),
        },
        {
            "job_title": "Java Backend Developer",
            "employer_name": "Tech Mahindra",
            "job_description": (
                "Hiring core software development engineers. Must have excellent command over "
                "Core Java, Spring Boot microservices, Hibernate, AWS cloud infrastructure "
                "architecture, and system integration patterns."
            ),
        },
    ]
    return mock_jobs
