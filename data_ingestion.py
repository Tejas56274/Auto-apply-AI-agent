import PyPDF2
import requests

def extract_text_from_resume(pdf_path):
    """
    Extracts raw text content from a local resume PDF file.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
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
    """
    Fetches active job openings from JSearch V2 API with a mock fallback 
    mechanism to ensure uninterrupted demo presentation.
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
        print(f"🔍 Fetching jobs for query: '{query}'...")
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            job_data = response.json()
            jobs_list = job_data.get('data', [])
            print(f"✅ Successfully fetched {len(jobs_list)} jobs from Live API!")
            return jobs_list
        else:
            print(f"⚠️ Live API Status {response.status_code}. Activating Secure Mock Job Directory for Demo...")
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
            
    except Exception as e:
        print(f"❌ Error connecting to network: {e}")
        return []