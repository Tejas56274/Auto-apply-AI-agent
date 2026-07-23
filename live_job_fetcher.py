import requests
import random
import re
from urllib.parse import quote

def clean_html(text):
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def fetch_live_jobs(query="Data Science", location="India"):
    live_jobs = []
    
    # Remotive API
    url = "https://remotive.com/api/remote-jobs"
    params = {"search": query, "limit": 10}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            job_list = data.get("jobs", [])
            
            for job in job_list:
                desc_text = clean_html(job.get("description", ""))
                short_desc = desc_text[:500] if desc_text else "No detailed description."
                
                # Dynamic Google Search URL fallback agar original link na ho
                company_name = job.get("company_name", "")
                title_name = job.get("title", "")
                search_query = quote(f"{title_name} {company_name} apply jobs")
                fallback_url = f"https://www.google.com/search?q={search_query}"
                
                job_url = job.get("url")
                if not job_url or job_url == "#":
                    job_url = fallback_url
                
                live_jobs.append({
                    "title": title_name if title_name else "Software Role",
                    "company": company_name if company_name else "Tech Startup",
                    "location": job.get("candidate_required_location", location),
                    "desc": f"Role: {title_name}. Required skills & description: {short_desc}",
                    "url": job_url
                })
    except Exception as e:
        print(f"Error fetching live feed: {e}")

    # Backup Feed (Jobicy)
    if len(live_jobs) < 3:
        try:
            url_backup = "https://jobicy.com/api/v2/remote-jobs"
            res_backup = requests.get(url_backup, params={"count": 10, "industry": "engineering"}, timeout=10)
            if res_backup.status_code == 200:
                backup_data = res_backup.json().get("jobs", [])
                for b_job in backup_data:
                    desc_text = clean_html(b_job.get("jobDescription", ""))
                    
                    title_name = b_job.get("jobTitle", "Data Engineer")
                    company_name = b_job.get("companyName", "Tech Corp")
                    search_query = quote(f"{title_name} {company_name} apply jobs")
                    fallback_url = f"https://www.google.com/search?q={search_query}"
                    
                    job_url = b_job.get("url")
                    if not job_url or job_url == "#":
                        job_url = fallback_url

                    live_jobs.append({
                        "title": title_name,
                        "company": company_name,
                        "location": b_job.get("jobGeo", location),
                        "desc": desc_text[:500],
                        "url": job_url
                    })
        except Exception as e:
            print(f"Backup feed error: {e}")

    random.shuffle(live_jobs)
    return live_jobs[:8]