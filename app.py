import os
import time
import PyPDF2
import pandas as pd
import plotly.express as px
from urllib.parse import quote

# Protobuf compatibility fix
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st

# Custom ML and Services
from model_matching import calculate_ats_match_score
from sheets_logger import log_to_google_sheet
from live_job_fetcher import fetch_live_jobs

# Executive corporate configuration
st.set_page_config(page_title="Auto Apply AI Agent", page_icon="💼", layout="wide")

# Modern Styling
st.markdown("""
    <style>
    .main { background: radial-gradient(circle at 50% 10%, #1e1e2f 0%, #0c0c14 70%) !important; color: #f1f5f9 !important; }
    .stButton>button { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: #ffffff; border-radius: 8px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 1. Title Updated
st.markdown("<h1 style='margin-bottom: 5px;'>Auto Apply AI Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 25px;'>Automated Recruitment Pipeline & Deep Learning Match Engine</p>", unsafe_allow_html=True)

# Sidebar Operational Controls
st.sidebar.markdown("### System Parameters")
target_threshold = st.sidebar.slider("Compliance Threshold (%)", min_value=50, max_value=90, value=65)
search_profile = st.sidebar.selectbox("Job Sector Mapping", ["Data Science Internship", "Full-Stack Developer", "Machine Learning Engineer"])
job_location = st.sidebar.text_input("Target Location", value="India")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### Applicant Profile")
    uploaded_file = st.file_uploader("Upload Document (PDF Format)", type=["pdf"])

with col_right:
    st.markdown("### Platform Scope")
    st.write("Dynamic job matching engine fetching real-time market data directly from targeted endpoints.")

# 2. Button Text Updated to "Fetch Role"
if st.button("Fetch Role"):
    if uploaded_file is None:
        st.error("System Exception: Upload a target PDF profile first.")
    else:
        resume_text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"
        except Exception as e:
            st.error(f"Error reading PDF stream: {e}")

        if not resume_text.strip():
            st.error("Profile Extraction Failure: Parsed text was empty.")
        else:
            with st.spinner("Fetching Live Opportunities..."):
                scaled_job_directory = fetch_live_jobs(query=search_profile, location=job_location)

            st.success(f"Successfully fetched {len(scaled_job_directory)} live listings for '{search_profile}'!")

            evaluated_jobs = []
            qualified_count = 0
            total_scanned = len(scaled_job_directory)
            
            ui_progress = st.progress(0)
            status_container = st.empty()
            
            for idx, job in enumerate(scaled_job_directory):
                status_container.markdown(f"Processing Match Model: **{job['title']}** at {job['company']}")
                
                score = calculate_ats_match_score(resume_text, job["desc"])
                percentage_score = score * 100
                
                action = "Below Threshold"
                if percentage_score >= target_threshold:
                    action = "Synchronized to Cloud"
                    qualified_count += 1
                    log_to_google_sheet(job["title"], job["company"], score, status="Applied")
                
                # Link Fallback Safety (Prevents self-redirection to localhost)
                raw_url = job.get("url")
                if not raw_url or raw_url == "#" or not raw_url.startswith("http"):
                    search_query = quote(f"{job['title']} {job['company']} apply jobs")
                    job_url = f"https://www.google.com/search?q={search_query}"
                else:
                    job_url = raw_url
                
                evaluated_jobs.append({
                    "Job Title": job["title"],
                    "Organization": job["company"],
                    "Location": job["location"],
                    "ATS Match Value": f"{percentage_score:.2f}%",
                    "Raw_Score": percentage_score,
                    "Execution Status": "Logged to Ledger" if action == "Synchronized to Cloud" else "Filtered Out",
                    "Apply_Link": job_url
                })
                
                time.sleep(0.2)
                ui_progress.progress((idx + 1) / total_scanned)
                
            status_container.empty()
            
            # Results Table with Dynamic External Links
            df_display = pd.DataFrame(evaluated_jobs)
            st.markdown("### Recruitment Pipeline Synchronization Ledger")
            
            st.dataframe(
                df_display[["Job Title", "Organization", "Location", "ATS Match Value", "Execution Status", "Apply_Link"]],
                column_config={
                    "Apply_Link": st.column_config.LinkColumn(
                        "Apply Link", 
                        display_text="Apply Now ↗"
                    )
                },
                use_container_width=True
            )