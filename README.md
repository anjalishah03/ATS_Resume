# ATS Resume Scorer

An AI-assisted web app that reviews resumes and compares them with a job description. It returns an overall ATS-oriented score, a breakdown across five categories, and practical feedback to help users improve how their experience and skills are presented.

Built with **FastAPI** and **Streamlit**, the project combines Python-based scoring checks, spaCy, Sentence Transformers, and the Groq API. Supabase provides sign-in and optional analysis history.

## What It Does

1. Upload a resume and optionally paste a job description.
2. Extract text from the resume and use Groq to structure resume details and, when provided, job requirements.
3. Analyze formatting signals, keywords, content, ATS compatibility, and whether listed skills are supported by experience or project details.
4. Review the score, job match, strengths, issues, and suggested improvements. Export a PDF report or text summary, and revisit saved analyses when history storage is configured.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn, Python
- **NLP and matching:** spaCy (`en_core_web_md`), Sentence Transformers (`all-MiniLM-L6-v2` by default), RapidFuzz
- **Structured parsing:** Groq API (`openai/gpt-oss-120b`)
- **Authentication and optional history:** Supabase
- **PDF reports:** WeasyPrint and Jinja2

## Project Structure

```text
backend/
  api/                 API routes and authentication
  core/                Application configuration
  database/            Supabase history storage
  models/              API data schemas
  services/            Parsing, scoring, matching, feedback, and reports
  templates/           PDF report templates
  utils/               File and matching helpers
  main.py              FastAPI application entry point
frontend/
  components/           Streamlit result components
  services/             Backend API and Supabase clients
  views/                Home, scorer, history, and resources pages
  streamlit_app.py      Streamlit application entry point
jupyter notebooks/      Model training and data exploration notebooks
ml_model/               Local model artifacts; not loaded by default
requirements.txt        Backend and frontend Python dependencies
```

## How It Works

```text
Resume and optional job description
                |
                v
       Streamlit frontend
                |
                v
          FastAPI backend
                |
      +---------+----------+
      |                    |
 Text extraction      Groq parsing
      |                    |
      +---------+----------+
                v
     Scoring and matching
                |
                v
 Results, feedback, and exports
```

The backend uses spaCy and a Sentence Transformer model for NLP and semantic matching. Resume and job-description text are sent to Groq for structured parsing. Supabase handles authentication and can store analysis history. The default Sentence Transformer is loaded by model name; the local artifact under `ml_model/` is not selected automatically.

> Scores and feedback are heuristic and model-generated. They are intended as resume-improvement guidance, not a hiring prediction or a guarantee of how any employer's ATS will rank a resume.

## Notes

- Resume uploads are limited to 5 MB. PDF and DOCX are supported; legacy `.doc` files are rejected by the backend.
- Job descriptions can be pasted or uploaded as `.txt` files.
- Analysis requires a configured Groq API key. Supabase is needed for sign-in; history also requires the Supabase `analyses` table.
- Resume text and optional job-description text are sent to Groq. Avoid submitting sensitive information unless that data processing is acceptable to you.
