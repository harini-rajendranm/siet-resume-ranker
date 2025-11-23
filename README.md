
# Match-o-Matic 3000 - Sample Project

Match-o-Matic 3000 is an intelligent resume evaluation system that automatically analyzes and ranks uploaded resumes based on how closely they match a provided job description. When a user pastes a JD into the platform, system extracts key skills, qualifications, experience levels, and role-specific requirements using advanced text analysis. It then compares these criteria against the content of each resume to generate a detailed compatibility score. This process helps hiring teams quickly identify the most suitable candidates without manually screening every application. By offering objective, consistent, and data-driven ranking, system enhances the efficiency, accuracy, and fairness of the recruitment and shortlisting process.
.

## Files
- `app.py` — Streamlit app you can run locally.
- `requirements.txt` — Python packages required.
- `README.md` — this file.

## How to run
1. Create a virtual environment (recommended) and activate it.
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. In the app, upload resumes (PDF, DOCX, or TXT) and paste the job description. Click **Analyze & Rank**.

## Notes & Next steps
- This is a prototype with an explainable scoring function. For production:
  - Use robust resume parsers (e.g., resume-parser libraries, OCR for scanned PDFs).
  - Use NLP models (spaCy, transformers, or OpenAI embeddings) for semantic matching.
  - Add authentication, storage, and audit logs for HR compliance.
