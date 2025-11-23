
# AI Resume Ranker — Prototype (Streamlit)

 his is a minimal, local prototype of an AI Resume Ranker. It uses a simple keyword-overlap scoring method to rank uploaded resumes against a pasted Job Description (JD).

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
