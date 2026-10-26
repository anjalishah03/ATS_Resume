
# ATS Resume Scorer

An AI-assisted resume analysis tool built with **Streamlit**, **FastAPI**, and **Python**. It helps job seekers understand how clearly a resume presents its experience and skills, then offers practical feedback and an optional comparison with a target job description.

## Project Overview

This project demonstrates a complete application workflow: a user uploads a resume through a web interface, the backend extracts and analyzes its contents, and the results are presented as scores and actionable feedback. Supabase provides account authentication and can store analysis history. Groq is used to convert resume and job-description text into structured data; local NLP and embedding models support matching and skill-evidence checks.

**Who it is for:** job seekers who want a structured first review of a resume, and developers interested in an end-to-end AI application that combines a Python UI, REST API, NLP, third-party services, and optional persistence.

**What it provides:** an overall heuristic score, five component scores, strengths, detected issues, improvement suggestions, evidence checks for listed skills, and optional job-description match details. Reports can be downloaded as PDF or plain text.

> This is a decision-support project, not a hiring predictor. Scores are heuristic and model-generated; they are not affiliated with or guaranteed to match any employer's ATS.

## Features

- General resume analysis and optional job-description comparison.
- Five score dimensions: formatting, keywords, content, skill validation, and ATS compatibility.
- Structured feedback with issue severity, ATS impact, suggested fixes, strengths, and skill evidence.
- Resume parsing for selectable-text PDF and DOCX files, with PDF extraction fallback.
- Account sign-in, sign-up, and Google OAuth through Supabase.
- Per-account analysis history, when Supabase database storage is configured.
- PDF report and plain-text summary exports.
- A resources page with static resume guidance and ATS keyword examples.

## How It Works

1. **Upload:** The user signs in and uploads a PDF or DOCX resume. A job description can be pasted or provided as a text file.
2. **Extract and structure:** The API extracts readable text from the resume. Groq parses the resume and optional job description into structured fields.
3. **Analyze:** Python scoring rules check formatting signals, keywords, measurable achievements, ATS compatibility, and whether listed skills appear in project or experience evidence. spaCy and SentenceTransformer support text and semantic matching.
4. **Review and export:** The interface displays the overall score, component breakdown, strengths, issues, and suggestions. The user can download a report or revisit saved analyses.

At a glance: **Streamlit UI -> FastAPI API -> parsing and analysis services -> structured results -> Streamlit dashboard**. Supabase handles authentication and optional analysis history; Groq handles LLM-based parsing.

Resume text and, when provided, job-description text are sent to Groq. Do not use this application with sensitive documents unless that processing is acceptable under your organization's privacy requirements. Supabase is used for authentication and may store the analysis result and uploaded filename in the `analyses` table. The embedding model runs in the backend; the default model may be downloaded from Hugging Face the first time the service starts.

## Technology

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Resume parsing:** pdfplumber, PyPDF2, python-docx, python-magic
- **Analysis:** spaCy, SentenceTransformers, NumPy, RapidFuzz
- **LLM parsing:** Groq API (`openai/gpt-oss-120b`)
- **Authentication and optional persistence:** Supabase
- **PDF reports:** Jinja2 and WeasyPrint

## Repository Layout

```text
backend/
	api/              FastAPI routes and Supabase JWT validation
	core/             Runtime configuration
	database/         Supabase REST persistence
	models/           Pydantic API response schemas
	services/         Parsing, scoring, matching, feedback, and report generation
	templates/        HTML report templates
	utils/            File and keyword-matching helpers
	main.py           FastAPI application and model startup
frontend/
	components/       Streamlit result views
	services/         API client and Supabase authentication client
	views/            Landing, scorer, history, and resources pages
	streamlit_app.py  Streamlit entry point
ml_model/          Local research/model artifacts (not loaded by default)
jupyter notebooks/ Model training and data exploration notebooks
requirements.txt   Shared backend and frontend Python dependencies
```

The repository's `.gitignore` excludes `ml_model/` and `jupyter notebooks/`; these local assets are not required to run the default application. The backend loads `SENTENCE_TRANSFORMER_MODEL` (default `all-MiniLM-L6-v2`) rather than automatically loading the included fine-tuned artifact.

## Requirements

- Python 3.10 or newer.
- A Groq API key for resume parsing; this is required for every analysis.
- A Supabase project for sign-in and authenticated API access. Configure database access as well to retain history.
- Internet access on first startup to download spaCy/SentenceTransformer models, and at runtime for Groq and Supabase requests.
- Platform libraries required by WeasyPrint for PDF export. On Windows, the backend reports that a GTK/Pango runtime must be installed and available on `PATH` if PDF generation cannot load.

## Setup

Commands below use PowerShell from the repository root.

### 1. Create an environment and install dependencies

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

The backend tries `en_core_web_md` first and falls back to `en_core_web_sm` if the primary model is not installed. The setup above installs the primary model. `python-magic` may also require a compatible `libmagic` runtime on some platforms.

### 2. Configure environment variables

Create a `.env` file in the repository root for backend and local frontend settings. `.env` is ignored by Git; never commit API keys or service-role credentials.

```dotenv
GROQ_API_KEY=your-groq-api-key

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_KEY=your-supabase-service-role-key

# Configure this when your Supabase project uses HS256 JWT signing.
SUPABASE_JWT_SECRET=your-supabase-jwt-secret

# Optional: override the embedding model ID.
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2

# Optional: OAuth redirect target; must also be allowed in Supabase auth settings.
AUTH_REDIRECT_URL=http://localhost:8501
```

Keep `SUPABASE_KEY` and `SUPABASE_JWT_SECRET` on the backend only. `SUPABASE_KEY` is used as a service-role key by the database client and bypasses Row Level Security. The frontend uses `SUPABASE_ANON_KEY` for Supabase authentication. For asymmetric ES256/RS256 JWTs, the backend fetches signing keys from the Supabase JWKS endpoint using `SUPABASE_URL`; an HS256 secret is not needed for that verification path.

The frontend also supports Streamlit secrets. For a local setup, create `.streamlit/secrets.toml` in the repository root with:

```toml
[supabase]
url = "https://your-project.supabase.co"
anon_key = "your-supabase-anon-key"

[google_oauth]
redirect_uri = "http://localhost:8501"

[backend]
url = "http://localhost:8000"
```

Frontend auth configuration checks environment variables first and then `[supabase]` secrets. The API base URL is read from `[backend].url`; otherwise it defaults to `http://localhost:8000`. Set the OAuth redirect URL in Supabase's provider and redirect URL settings as well.

### 3. Create the Supabase history table

No database migration or table-creation script is included. To enable saved analyses, create an `analyses` table exposed through Supabase REST with at least these columns:

| Column | Suggested type | Notes |
|---|---|---|
| `id` | `uuid` | Primary key with a generated UUID; returned by history and delete operations |
| `user_id` | `uuid` | Supabase Auth user ID |
| `filename` | `text` | Uploaded resume filename |
| `ats_score` | `double precision` | Overall score |
| `keyword_match` | `double precision` | Keyword match value |
| `missing_keywords` | `jsonb` | Array of missing terms |
| `created_at` | `timestamptz` | Timestamp; the API supplies a value when saving |
| `analysis_result` | `jsonb` | Serialized analysis response |

The backend reads and deletes rows filtered by both `user_id` and the analysis ID. Since it uses the service-role key, the service bypasses RLS; keep that key private and do not expose it to the Streamlit client. If the table is absent or database writes fail, analysis can still succeed, but history may be empty or unavailable.

### 4. Run the application

Start the backend in one terminal:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start Streamlit in a second terminal:

```powershell
streamlit run frontend/streamlit_app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`. The API health endpoint is `http://localhost:8000/api/v1/health`; interactive API documentation is at `http://localhost:8000/docs` and `http://localhost:8000/redoc`.

## API Reference

All endpoints are under `/api/v1`. Except for health, routes require `Authorization: Bearer <supabase-access-token>`.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Reports API health and whether NLP and embedding models are loaded; no authentication required |
| `POST` | `/analyze-resume` | Multipart upload with required `resume` and optional `job_description` form fields |
| `GET` | `/history` | Lists the authenticated user's saved analyses |
| `DELETE` | `/history/{analysis_id}` | Deletes an analysis belonging to the authenticated user |
| `POST` | `/generate-pdf` | Generates a PDF from an `AnalysisResponse` JSON body |
| `GET` | `/history/{analysis_id}/pdf` | Generates a PDF for a saved analysis |

`POST /analyze-resume` returns an `AnalysisResponse`, including the overall score, component scores, issue summary, detailed feedback, skill-validation details, and optional job-description comparison. FastAPI's interactive schema is available at `/docs` while the backend is running.

## Scoring and Matching

The implementation evaluates these component dimensions, with the following component ceilings:

| Component | Component ceiling |
|---|---:|
| Formatting | 20 points |
| Keywords | 25 points |
| Content | 25 points |
| Skill validation | 15 points |
| ATS compatibility | 15 points |

The overall score is assembled separately: keyword and skill-validation percentages are combined, then combined with content, formatting, and ATS compatibility contributions; bonuses and penalties may also apply. A job-description comparison combines fuzzy keyword overlap and embedding similarity, and returns matched/missing terms and a skills gap.

**Known scoring caveat:** the current aggregation normalizes the ATS-compatibility component differently from the other components (it uses a 0-to-1 fraction where the others use 0-to-100 percentages). The declared `SCORE_WEIGHTS` setting is also not used by the aggregation function. Treat the overall score as experimental until this discrepancy is corrected and the score is recalibrated.

## File and Analysis Limitations

- Resume uploads are limited to 5 MB.
- PDF and DOCX are the supported resume formats. The interface offers `.doc`, but the backend rejects legacy DOC files; convert them to PDF or DOCX first.
- PDF parsing requires selectable text. Scanned/image-only PDFs are not OCR-processed.
- A job description can be pasted or supplied as a `.txt` file. PDF/DOCX job-description uploads are not supported in the interface.
- Analysis requires Groq access. Without `GROQ_API_KEY`, the resume cannot be parsed and analyzed.
- PDF export requires a working WeasyPrint installation and its native system dependencies. Text-summary export does not use WeasyPrint.
- The score and feedback are heuristic and model-generated; they may be incomplete or incorrect and should be reviewed by a person.

## Security and Deployment Notes

- Do not expose `.env`, Supabase service-role credentials, JWT signing secrets, or Groq keys in source control, client code, logs, or public deployments.
- Resume and job-description text are sent to Groq for parsing. Analysis results and filenames may be persisted in Supabase when storage is configured.
- The backend currently configures CORS with an empty allowed-origin list. The checked-in Streamlit configuration also disables CORS and XSRF protection; review these settings and deploy behind appropriate HTTPS, origin controls, and authentication before exposing the app beyond local development.
- The API binds to localhost in the commands above. Avoid binding to a public interface without a deployment-specific security review.

## Development Notes

- Backend entry point: `backend.main:app`.
- Frontend entry point: `frontend/streamlit_app.py`.
- The API loads spaCy and SentenceTransformer models during startup, so first startup can take time and can fail if the configured model is unavailable.
- No automated test suite is currently present in the repository.
- The `jupyter notebooks/` directory contains exploration/training notebooks, and `ml_model/` contains local artifacts; neither is automatically consumed by the default runtime configuration.
