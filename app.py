
import streamlit as st
import io, re, os, csv
from collections import Counter
import pandas as pd

# Optional imports that must be in requirements:
try:
    import pdfplumber
except Exception:
    pdfplumber = None
try:
    import docx
except Exception:
    docx = None

st.set_page_config(page_title="Match-o-Matic 3000", layout="wide")
st.title("Match-o-Matic 3000")
st.markdown(
    """
<style>
[alt=Logo] {
    height: 8rem; /* Adjust this value as needed */
}
</style>
""",
    unsafe_allow_html=True,
)

#st.logo("logo.jpeg")
st.logo("logo.jpeg", icon_image="logo.jpeg", link="https://www.siet.ac.in")

st.markdown(
    """
Match-o-Matic 3000 is an intelligent resume evaluation system that automatically analyzes and ranks uploaded resumes based on how closely they match a provided job description. When a user pastes a JD into the platform, system extracts key skills, qualifications, experience levels, and role-specific requirements using advanced text analysis. It then compares these criteria against the content of each resume to generate a detailed compatibility score. This process helps hiring teams quickly identify the most suitable candidates without manually screening every application. By offering objective, consistent, and data-driven ranking, system enhances the efficiency, accuracy, and fairness of the recruitment and shortlisting process.

Scoring method (simple, explainable):
- Extract text from each resume (PDF / DOCX / TXT).
- Extract keywords from the JD (split by non-word characters, remove short words).
- Score = keyword overlap ratio + normalized keyword frequency bonus.
You can download results as CSV.
"""
)

with st.sidebar:
    st.header("Resume Ranker")
    uploaded_files = st.file_uploader("Upload resumes (PDF / DOCX / TXT)", accept_multiple_files=True)
    jd_text = st.text_area("Paste Job Description (JD) here", height=220)
    min_score = st.slider("Minimum score to show", 0, 100, 0)
    analyze_btn = st.button("Analyze & Rank")

def extract_text_from_pdf(file_bytes):
    if pdfplumber is None:
        return ""
    text = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception:
        return ""
    return "\n".join(text)

def extract_text_from_docx(file_bytes):
    if docx is None:
        return ""
    text = []
    try:
        from docx import Document
        bio = io.BytesIO(file_bytes)
        doc = Document(bio)
        for p in doc.paragraphs:
            text.append(p.text)
    except Exception:
        return ""
    return "\n".join(text)

def extract_text(file):
    filename = file.name
    data = file.getvalue()
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(data)
    if lower.endswith(".docx") or lower.endswith(".doc"):
        return extract_text_from_docx(data)
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def jd_keywords(jd):
    # Simple keyword extractor: words longer than 2 chars, lowercased, excluding common stopwords.
    stop = set(["and","the","for","with","that","this","from","are","use","using","will","must","should","a","an","to","of","in","on"])
    #tokens = re.split(r'W+', jd.lower())
    tokens = re.findall(r'\b\w+\b', jd.lower())

    tokens = [t for t in tokens if len(t) > 2 and t not in stop]
    return Counter(tokens)

def score_resume(res_text, jd_kw_counts):
    if not jd_kw_counts:
        return 0.0, 0, 0
    #tokens = re.split(r'\W+', res_text.lower())
    tokens = re.findall(r'\b\w+\b', res_text.lower())

    tokens = [t for t in tokens if len(t) > 2]
    token_counts = Counter(tokens)
    matched = 0
    freq_bonus = 0
    for kw, jd_count in jd_kw_counts.items():
        if token_counts.get(kw,0) > 0:
            matched += 1
            freq_bonus += min(token_counts[kw], jd_count)
    total_kw = sum(jd_kw_counts.values())
    if total_kw == 0:
        return 0.0, matched, freq_bonus
    overlap_ratio = matched / len(jd_kw_counts)  # fraction of distinct JD keywords present
    normalized_bonus = freq_bonus / (total_kw * 2)  # scaled down
    raw_score = overlap_ratio * 0.8 + normalized_bonus * 0.2
    return raw_score * 100, matched, freq_bonus

if analyze_btn:
    if not uploaded_files:
        st.warning("Please upload at least one resume file.")
    elif not jd_text.strip():
        st.warning("Please paste the job description (JD) to compare against.")
    else:
        st.info("Analyzing... (this runs locally in your browser/server)")
        jd_counts = jd_keywords(jd_text)
        results = []
        for f in uploaded_files:
            text = extract_text(f)
            score, matched, bonus = score_resume(text, jd_counts)
            results.append({
                "filename": f.name,
                "score": round(score,2),
                "matched_keywords": matched,
                "freq_bonus": bonus,
                "char_count": len(text),
            })
        df = pd.DataFrame(results).sort_values("score", ascending=False).reset_index(drop=True)
        df["rank"] = df["score"].rank(method="dense", ascending=False).astype(int)
        df = df[["rank","filename","score","matched_keywords","freq_bonus","char_count"]]
        df = df[df["score"] >= min_score]
        st.success(f"Found {len(df)} resumes matching filter (>= {min_score}%).")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV results", data=csv, file_name="resume_ranks.csv", mime="text/csv")

        # Show top candidate details
        if not df.empty:
            top = df.iloc[0]
            st.markdown("### Top candidate")
            st.write(f"**{top['filename']}** — Score: {top['score']}% — Rank {top['rank']}")
            # Show resume text preview
            top_file = next((f for f in uploaded_files if f.name == top['filename']), None)
            if top_file:
                preview_text = extract_text(top_file)[:10000]
                st.text_area("Top resume preview (first 10k chars)", value=preview_text, height=300)
