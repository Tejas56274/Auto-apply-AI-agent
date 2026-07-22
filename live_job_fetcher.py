# live_job_fetcher.py
import requests

def fetch_live_jobs(query="data science internship", location="India"):
    """
    SerpAPI ya direct web endpoints se live jobs fetch karta hai.
    Sahi API Key setup na hone par fallback live demo data deta hai.
    """
    # Agar aapke paas SerpAPI key hai toh yahan daalein (Optional):
    api_key = "YOUR_SERPAPI_KEY"
    
    if api_key and api_key != "YOUR_SERPAPI_KEY":
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": api_key
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            job_results = data.get("jobs_results", [])
            
            live_jobs = []
            for job in job_results:
                live_jobs.append({
                    "title": job.get("title", "N/A"),
                    "company": job.get("company_name", "N/A"),
                    "location": job.get("location", location),
                    "desc": job.get("description", "No detailed description available.")
                })
            if live_jobs:
                return live_jobs
        except Exception as e:
            print(f"Error fetching live jobs: {e}")

    # Fallback / Dynamic Simulated Feed agar Live API setup nahi hai
    return [
        {
            "title": f"Live {query.title()} Trainee", 
            "company": "Analytics Live Corp", 
            "location": location, 
            "desc": f"Looking for candidates skilled in {query}, Python, Machine Learning, and SQL databases."
        },
        {
            "title": "AI & ML Data Science Intern", 
            "company": "TechVision Labs", 
            "location": "Remote - India", 
            "desc": "Hands-on experience with Neural Networks, TensorFlow, Scikit-Learn, and Python scripting is required."
        },
        {
            "title": "Junior Data Scientist", 
            "company": "Innovate Analytics", 
            "location": "Bengaluru", 
            "desc": "Freshers with solid foundation in Data Pipeline architecture, Deep Learning, and pandas manipulation."
        }
    ]