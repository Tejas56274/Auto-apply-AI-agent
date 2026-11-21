import PyPDF2
import requests
import logging
from typing import Optional, List, Dict

# Configure a basic logger for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_resume(pdf_path: str) -> Optional[str]:
    """Extract raw text from a local PDF resume.

    Args:
        pdf_path: Filesystem path to the PDF file.

    Returns:
        The concatenated text of all pages, or ``None`` if extraction fails.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        logger.info("✅ Resume text successfully extracted!")
        return text
    except Exception as e:
        logger.error(f"❌ Error reading PDF: {e}")
        return None

def fetch_live_jobs(query: str = "Data Scientist in India", num_pages: int = 1) -> List[Dict]:
    """Fetch active job listings from the JSearch V2 API with a mock fallback.

    The function first attempts a live API request. If the request fails or returns a
    non‑200 status, a static mock dataset is provided to keep the demo functional.

    Args:
        query: Search query string.
        num_pages: Number of result pages to request.

    Returns:
        A list of job dictionaries containing ``job_title``, ``employer_name`` and
        ``job_description`` keys.
    """
    url = "https://jsearch.p.rapidapi.com/search-v2"
    querystring = {
        "query": query,
        "num_pages": str(num_pages),
        "country": "us",
        "date_posted": "all"
    }
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": "12d6ada391mshe26b809a454445e7p1579d3jsn6b6a207220b9"
    }
    try:
        logger.info(f"🔍 Fetching jobs for query: '{query}'...")
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            job_data = response.json()
            jobs_list = job_data.get('data', [])
            logger.info(f"✅ Successfully fetched {len(jobs_list)} jobs from Live API!")
            return jobs_list
        else:
            logger.warning(f"⚠️ Live API returned status {response.status_code}. Using mock data.")
    except Exception as e:
        logger.error(f"❌ Network error while fetching jobs: {e}")

    # Mock fallback – ensures the demo runs without external connectivity
    mock_jobs = [
        {
            "job_title": "Data Science Intern",
            "employer_name": "Deloitte India",
            "job_description": "We are seeking a 3rd year engineering student for a Data Science role. Requirements: Hands-on experience building stock prediction systems, Machine Learning modeling, Neural Networks, TensorFlow, and Python scripting. Experience with dashboard tools like Tableau is a huge plus."
        },
        {
            "job_title": "Junior Data Analyst",
            "employer_name": "TCS Bangalore",
            "job_description": "Looking for fresh graduates with proficiency in Core Python, SQL databases, and Excel dashboards. Understanding of deep learning or NLP model deployment is good to have but not mandatory."
        },
        {
            "job_title": "Java Backend Developer",
            "employer_name": "Tech Mahindra",
            "job_description": "Hiring core software development engineers. Must have excellent command over Core Java, Spring Boot microservices, Hibernate, AWS cloud infrastructure architecture, and system integration patterns."
        }
    ]
    return mock_jobs
