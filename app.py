import streamlit as st
import pandas as pd
import plotly.express as px
import time
from data_ingestion import fetch_live_jobs
from model_matching import calculate_ats_match_score
from sheets_logger import log_to_google_sheet
import PyPDF2

# Executive corporate configuration mirroring premium SaaS dashboards
st.set_page_config(page_title="Auto Apply AI Agent", page_icon="💼", layout="wide")

# 🔥 PREMIUM DARK GLASSMORPHISM UI/UX DESIGN SYSTEM (SaaS Vibe)
st.markdown("""
    <style>
    /* Global Canvas Dark Radial Glow Gradient */
    .main { 
        background: radial-gradient(circle at 50% 10%, #1e1e2f 0%, #0c0c14 70%) !important; 
        color: #f1f5f9 !important; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
    }
    
    /* Buttons with standard glowing neon tech blue mapping */
    .stButton>button { 
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); 
        color: #ffffff; 
        font-weight: 600; 
        font-size: 15px; 
        width: 100%; 
        border-radius: 8px; 
        border: none; 
        height: 44px; 
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
        transition: all 0.3s ease; 
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%); 
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
        color: #ffffff; 
    }
    
    /* Clean Semi-Transparent Glassmorphism Cards */
    .metric-card { 
        background: rgba(255, 255, 255, 0.03); 
        padding: 22px; 
        border-radius: 12px; 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
    }
    .metric-title { 
        font-size: 12px; 
        color: #94a3b8; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 0.75px; 
    }
    .metric-value { 
        font-size: 32px; 
        color: #ffffff; 
        font-weight: 700; 
        margin-top: 5px; 
    }
    
    /* Refined structural neon typography rules */
    h1 { color: #ffffff !important; font-size: 32px !important; font-weight: 800 !important; letter-spacing: -0.5px; }
    h3 { color: #f1f5f9 !important; font-size: 19px !important; font-weight: 600 !important; margin-bottom: 15px !important; border-left: 4px solid #6366f1; padding-left: 10px; }
    p { color: #cbd5e1 !important; }
    
    /* Custom dark theme layout adjustments for file uploaders & data frames */
    div.stDataFrame { border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; background-color: #0c0c14; }
    .stFileUploader { background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 10px; }
    
    /* Sidebar Modern Restyling */
    section[data-testid="stSidebar"] {
        background-color: #09090e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Top Bar Header Architecture
st.markdown("<h1 style='margin-bottom: 5px;'>TalentStream AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 15px; margin-bottom: 25px;'>Automated Recruitment Pipeline & Deep Learning Match Engine</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 0; margin-bottom: 25px;'>", unsafe_allow_html=True)

# Sidebar Operational Controls
st.sidebar.markdown("<h3 style='margin-top: 0;'>System Parameters</h3>", unsafe_allow_html=True)
target_threshold = st.sidebar.slider("Compliance Threshold (%)", min_value=50, max_value=90, value=65)
search_profile = st.sidebar.selectbox("Job Sector Mapping", ["Data Science & Analytics", "Full-Stack Engineering", "Cloud Infrastructure"])

st.sidebar.markdown("<hr style='border-top: 1px solid rgba(255, 255, 255, 0.08);'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #94a3b8; font-size: 12px;'><strong>Infrastructure Layer Architecture:</strong><br>• Parsing System: PyPDF2 Binary Extractor<br>• Logic Layer: TensorFlow Sequential MLP<br>• Cloud Sync: Asynchronous Serverless Webhook</p>", unsafe_allow_html=True)

# Main Grid Partition
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("<h3>Applicant Profile</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Document (PDF Format Only)", type=["pdf"], help="Parses matrix structural attributes out of standard PDF streams.")
    
    if uploaded_file is not None:
        st.markdown("<p style='color: #34d399; font-size: 13px; font-weight: 500;'>✓ System Document Verification Complete</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #fbbf24; font-size: 13px; font-weight: 500;'>! Action Required: Please provide a target profile</p>", unsafe_allow_html=True)

with col_right:
    st.markdown("<h3>Platform Operational Scope</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 14px; line-height: 1.6;'>This intelligence automation framework scans active employment endpoints, maps data streams to high-dimensional feature vectors via statistical arrays, processes match indicators locally using a proprietary Multi-Layer Perceptron network, and logs evaluation metrics directly to centralized cloud environments via structural webhooks.</p>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# Dataset Structure
scaled_job_directory = [
    {"title": "Data Science Intern", "company": "Deloitte India", "location": "Bengaluru", "desc": "Requirements: Hands-on experience building stock prediction systems, Machine Learning modeling, Neural Networks, TensorFlow, and Python scripting. Experience with dashboard tools like Tableau is a huge plus."},
    {"title": "Junior Data Analyst", "company": "TCS Bangalore", "location": "Bengaluru", "desc": "Looking for fresh graduates with proficiency in Core Python, SQL databases, and Excel dashboards. Understanding of deep learning or NLP model deployment is good to have."},
    {"title": "Machine Learning Engineer", "company": "NVIDIA India", "location": "Hyderabad", "desc": "Deep Learning optimization primitives, CUDA, Core TensorFlow neural networks processing pipeline architecture, computer vision deployment algorithms optimization."},
    {"title": "AI Research Intern", "company": "Juspay", "location": "Bengaluru", "desc": "Functional programming paradigms, algorithmic data processing, graph theory modeling pipelines, and full-stack integration frameworks."},
    {"title": "Data Engineer", "company": "Micron Technology", "location": "Hyderabad", "desc": "Data orchestration systems setup, big data indexing, analytics pipeline infrastructure tracking, Python database engines integration architecture."},
    {"title": "Business Intelligence Analyst", "company": "Tech Mahindra", "location": "Pune", "desc": "Enterprise reporting models development, data management visualization dashboards compilation using commercial analytics metrics layouts."},
    {"title": "Java Backend Developer", "company": "Wipro", "location": "Mumbai", "desc": "Hiring software developers. Excellent command over Core Java, Spring Boot microservices, Hibernate, AWS cloud infrastructure architecture."}
]

# Action Pipeline Execution Control
if st.button("Execute Core Evaluation Pipeline"):
    if uploaded_file is None:
        st.error("System Exception: Cannot initialize vector analysis maps without a source document matrix.")
    else:
        resume_text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    resume_text += page_text + "\n"
        except Exception as e:
            st.error(f"Error reading document stream: {e}")
            
        if resume_text == "":
            st.error("Profile Extraction Failure: The parsed text object returned zero indices.")
        else:
            evaluated_jobs = []
            qualified_count = 0
            total_scanned = len(scaled_job_directory)
            
            ui_progress = st.progress(0)
            status_container = st.empty()
            
            for idx, job in enumerate(scaled_job_directory):
                status_container.markdown(f"<p style='color: #cbd5e1; font-size: 13px;'>Processing Model Inference Layers: <strong style='color:#a5b4fc;'>{job['title']}</strong> at {job['company']}</p>", unsafe_allow_html=True)
                
                score = calculate_ats_match_score(resume_text, job["desc"])
                percentage_score = score * 100
                
                action = "Below Threshold"
                if percentage_score >= target_threshold:
                    action = "Synchronized to Cloud"
                    qualified_count += 1
                    log_to_google_sheet(job["title"], job["company"], score, status="Applied")
                
                evaluated_jobs.append({
                    "Job Title": job["title"],
                    "Organization": job["company"],
                    "Location": job["location"],
                    "ATS Match Value": f"{percentage_score:.2f}%",
                    "Raw_Score": percentage_score,
                    "Execution Status": "Logged to Ledger" if action == "Synchronized to Cloud" else "Filtered Out"
                })
                
                time.sleep(0.25)
                ui_progress.progress((idx + 1) / total_scanned)
                
            status_container.empty()
            
            # Premium Geometric Metric Display Cards Section (Dark Glassmorphic style)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Profiles Aggregated</div><div class='metric-value'>{total_scanned}</div></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Pipeline Deployments</div><div class='metric-value' style='color: #34d399;'>{qualified_count}</div></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Automation Efficiency</div><div class='metric-value' style='color: #fbbf24;'>{(qualified_count/total_scanned)*100:.1f}%</div></div>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
            
            # Ledger Dataframe
            st.markdown("<h3>Recruitment Pipeline Synchronization Ledger</h3>", unsafe_allow_html=True)
            df_display = pd.DataFrame(evaluated_jobs)
            st.dataframe(df_display[["Job Title", "Organization", "Location", "ATS Match Value", "Execution Status"]], use_container_width=True)
            
            # High-Fidelity Analytics Plotly Render Panels (Fully Optimized for Dark Theme)
            st.markdown("<h3>System Compliance Data Analytics Visualization</h3>", unsafe_allow_html=True)
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                fig_bar = px.bar(df_display, x="Organization", y="Raw_Score", color="Execution Status",
                                 title="Match Score Densities Across Selected Enterprises",
                                 labels={"Raw_Score": "ATS Density Score (%)"},
                                 color_discrete_map={"Logged to Ledger": "#34d399", "Filtered Out": "rgba(255,255,255,0.15)"})
                # Making background transparent and text crisp white
                fig_bar.update_layout(
                    template="plotly_dark", 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color="#f1f5f9"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with chart_col2:
                fig_pie = px.pie(df_display, names="Execution Status", title="Pipeline Conversion Structural Breakdowns",
                                 color="Execution Status",
                                 color_discrete_map={"Logged to Ledger": "#34d399", "Filtered Out": "rgba(255,255,255,0.15)"})
                fig_pie.update_layout(
                    template="plotly_dark", 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color="#f1f5f9"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.markdown("<p style='color: #94a3b8; font-size: 13px; text-align: center;'>Configure the parameters in the control board and trigger execution to initialize matching metrics arrays.</p>", unsafe_allow_html=True)