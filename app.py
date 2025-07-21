

import streamlit as st
import io 
import os
import json
import PyPDF2 as pdf
from dotenv import load_dotenv
import requests

from db import create_table, insert_analysis, get_all_analysis
# Run this once when app starts
create_table()


# Load .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Base URL for Groq API
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"

# Title
st.title("🤖 AI Resume Analyzer")
st.markdown("Analyze your resume against a job description using LLMs!")

# Upload and Input
job_description = st.text_area("📋 Paste Job Description")
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])

# Extract Resume Text
def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    return ""

# Build Prompt for LLM
def build_prompt(resume_text, job_description):
    return f"""
    Act like an experienced ATS (Applicant Tracking System) specialized in tech hiring.
    Compare the candidate's resume with the job description below.

Instructions:
- Compare resume and JD.
- Count how many relevant keywords from JD are present in resume.
- Match percentage = (matched_keywords / total_keywords_from_JD) * 100 (rounded to nearest integer).
- Be honest — do not give high % if resume lacks important skills, and act like strict ATS.
- Always respond in ONLY valid JSON in the following structure:

{{
  "JD Match": "percentage (e.g. 76%)",
  "MatchedKeywords": ["keyword1", "keyword2"],
  "MissingKeywords": ["keyword1", "keyword2"],
  "Profile Summary": "summary of candidate's strengths and weaknesses"
}}

RESUME:
\"\"\"{resume_text}\"\"\"

JOB DESCRIPTION:
\"\"\"{job_description}\"\"\"
"""



# Call Groq API
def query_groq_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return content
        else:
            return {"error": f"❌ Error: {response.status_code} - {response.json()}"}
    except Exception as e:
        return {"error": str(e)}

# Parse JSON string safely
import re

def parse_llm_json(raw_response):
    try:
        # Extract first JSON object from text using regex
        json_str = re.search(r'\{.*\}', raw_response, re.DOTALL).group()
        return json.loads(json_str)
    except Exception as e:
        return {"error": f"❌ Failed to parse LLM response. {str(e)}"}

# Extract Job Role (first line of JD)
def extract_job_role(jd_text):
    lines = jd_text.strip().split('\n')
    if lines:
        return lines[0][:100]  # Limit to 100 chars just in case
    return "Unknown Role"



import pandas as pd
import io

# Submit Button
if st.button("🚀 Analyze"):
    if uploaded_file and job_description:
        resume_text = extract_text_from_pdf(uploaded_file)
        with st.spinner("Analyzing..."):
            prompt = build_prompt(resume_text, job_description)
            llm_response = query_groq_llm(prompt)

            if isinstance(llm_response, dict) and "error" in llm_response:
                st.error(llm_response["error"])
            else:
                result = parse_llm_json(llm_response)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("✅ Analysis Complete")

                    # Extract job role and resume file name
                    job_role = extract_job_role(job_description)
                    resume_filename = uploaded_file.name

                    # Display JD match and profile summary
                    st.markdown(f"**🎯 JD Match:** {result['JD Match']}")
                    st.markdown(f"**🧠 Profile Summary:**\n\n{result['Profile Summary']}")

                    # Display visual comparison table
                    data = {
                        "Resume File": [resume_filename],
                        "Job Role": [job_role],
                        "JD Match %": [result['JD Match']],
                        "Matched Keywords": [", ".join(result['MatchedKeywords'])],
                        "Missing Keywords": [", ".join(result['MissingKeywords'])]
                    }
                    df = pd.DataFrame(data)
                    st.subheader("📊 Visual Comparison Table")
                    st.table(df)

                    # Downloadable CSV report
                    csv_data = {
                        "Resume File": [resume_filename],
                        "Job Role": [job_role],
                        "JD Match (%)": [result['JD Match']],
                        "Matched Keywords": [", ".join(result['MatchedKeywords'])],
                        "Missing Keywords": [", ".join(result['MissingKeywords'])],
                        "Profile Summary": [result['Profile Summary']]
                    }
                    df_csv = pd.DataFrame(csv_data)
                    csv_buffer = io.StringIO()
                    df_csv.to_csv(csv_buffer, index=False)

                    st.download_button(
                        label="⬇️ Download CSV Report",
                        data=csv_buffer.getvalue(),
                        file_name="resume_analysis_report.csv",
                        mime="text/csv"
                    )

                    # Save to DB
                    insert_analysis(
                        resume_filename=resume_filename,
                        job_role=job_role,
                        jd_match=result['JD Match'],
                        matched_keywords=", ".join(result['MatchedKeywords']),
                        missing_keywords=", ".join(result['MissingKeywords']),
                        profile_summary=result['Profile Summary']
                    )
                    st.success("✅ Data saved to database successfully.")


    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")



# Sidebar: View All Analyses and Download All CSV
if st.sidebar.button("📂 View Top 10 Analyses"):
    with st.spinner("Fetching data..."):
        all_rows = get_all_analysis(fetch_all=True)  # ✅ renamed from 'all=True'
        if all_rows:
            df_all = pd.DataFrame(all_rows, columns=[
                "ID", "Resume File", "Job Role", "JD Match", "Matched Keywords", "Missing Keywords", "Profile Summary", "Created At"
            ])

            # Show only latest 10 entries
            st.subheader("📋 Latest 10 Resume Analyses (for preview)")
            st.dataframe(df_all.tail(10))

            # Download full CSV
            csv_buffer = io.StringIO()
            df_all.to_csv(csv_buffer, index=False)

            st.download_button(
                label="⬇️ Download All Analyses as CSV",
                data=csv_buffer.getvalue(),
                file_name="all_resume_analyses.csv",
                mime="text/csv"
            )
        else:
            st.info("No analysis records found yet.")


