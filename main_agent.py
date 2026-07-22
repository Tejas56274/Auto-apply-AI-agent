import time
from data_ingestion import extract_text_from_resume, fetch_live_jobs
from model_matching import calculate_ats_match_score
from sheets_logger import log_to_google_sheet

def run_autonomous_agent():
    print("🚀 === INITIALIZING AI PLACEMENT AGENT === 🚀\n")
    
    resume_path = "my_resume.pdf"
    resume_text = extract_text_from_resume(resume_path)
    
    if not resume_text:
        print("❌ Termination: Unable to process pipeline execution without resume source text.")
        return
        
    live_jobs = fetch_live_jobs(query="Data Science Intern India")
    
    if not live_jobs:
        print("❌ Termination: Active job openings database empty or inaccessible.")
        return
        
    print("\n🧠 === STARTING DEEP LEARNING MATCHING ENGINE === 🧠")
    print(f"Total structured listings to evaluate: {len(live_jobs)}\n")
    
    for index, job in enumerate(live_jobs, start=1):
        job_title = job.get('job_title', 'N/A')
        company = job.get('employer_name', 'N/A')
        job_description = job.get('job_description', '')
        
        if not job_description:
            continue
            
        print(f"--- [{index}] Evaluating Parameters: {job_title} at {company} ---")
        
        score = calculate_ats_match_score(resume_text, job_description)
        percentage_score = score * 100
        
        print(f"🎯 Evaluated ATS Match Metric: {percentage_score:.2f}%")
        
        if percentage_score >= 65.0:
            print(f"🟢 Target profile qualified. Initiating Google Sheets Cloud logging routine...")
            log_to_google_sheet(job_title, company, score, status="Applied")
        else:
            print(f"🔴 Score below matching standard. Skipping automated workflow.")
            
        print("-" * 65)
        time.sleep(1)

if __name__ == "__main__":
    run_autonomous_agent()