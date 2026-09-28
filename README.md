# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project
documentation. It provides:

- Question answering (`/qa`)
- Beginner-friendly concept explanations (`/explain`)
- Three-question MCQ quiz generation (`/quiz`)
- Concise educational summaries (`/summarize`)
- Beginner/intermediate/advanced learning paths (`/learn/recommendations`)

The supplied documentation describes FastAPI, a simple HTML/CSS frontend,
Gemini-powered Q&A/quiz/summary/learning-path features, and a local
LaMini-Flan-T5 explanation module.

## Architecture

```text
Browser
  |
  v
FastAPI (main.py)
  |
  +--> qna.py --------------------+
  +--> explanation_module.py -----+--> gemini_client.py --> Google Gemini API
  +--> quiz_module.py ------------+
  +--> summary_module.py ---------+
  +--> learning_path.py ----------+
  |
  +--> templates/index.html + static/
```

The default explanation provider is Gemini so the project can be installed
with one normal Python dependency set. A local LaMini-Flan-T5 provider is
available through `requirements-local.txt`.

## Requirements

- Python 3.10+
- A Google Gemini API key
- VS Code (recommended, but not required)

## VS Code setup

1. Open this `EduGenie` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Upgrade pip:

```bash
python -m pip install --upgrade pip
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env`.
7. Put your Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_real_key
```

The project uses the current Google GenAI Python SDK and the model configured
by `GEMINI_MODEL`. The default in this project is `gemini-3.8-flash`.

## Run

```bash
uvicorn main:app --reload
```

Open:

- Web app: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Test

Run the automated tests:

```bash
pytest
```

The tests cover the homepage, health endpoint, request validation, and clear
failure behavior when the API key is absent. They do not consume Gemini API
quota.

For a manual end-to-end test, enter:

- Q&A: `Which is the largest ocean?`
- Explain: `Explain the Pythagoras theorem simply.`
- Quiz: paste a short educational paragraph.
- Summary: paste a long educational paragraph.
- Learning path: `SQL`

## Optional local LaMini explanation model

The original documentation identifies `LaMini-Flan-T5-783M` as the local
concept-explanation model. To enable that path:

```bash
pip install -r requirements-local.txt
```

Then change `.env`:

```env
EXPLANATION_PROVIDER=local
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local inference downloads the model from Hugging Face and can use
significant disk/RAM. If you want the smallest setup, leave
`EXPLANATION_PROVIDER=gemini`.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"What is photosynthesis?\"}"
```

### Explanation

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Explain Newton's first law.\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Water boils at 100 degrees Celsius at standard atmospheric pressure.\"}"
```

### Summary

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Paste your educational passage here.\"}"
```

### Learning path

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"topic\":\"SQL\",\"level\":\"beginner\"}"
```

## Project files

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── schemas.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_api.py
```

## Security notes

- Never commit `.env` or your Gemini API key.
- Keep API keys server-side; the browser never receives the key.
- For production deployment, add authentication, rate limiting, HTTPS,
  logging/monitoring, and a persistent user/progress store.
- AI-generated educational content should be reviewed for important academic
  or safety-critical decisions.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Create `.env` from `.env.example` and set the real key. Restart Uvicorn after
changing environment variables.

### Model not available

Set `GEMINI_MODEL` to a model currently enabled for your Gemini API project.
For example:

```env
GEMINI_MODEL=gemini-3.8-flash
```

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open http://127.0.0.1:8001.

### Local model is slow

Use the default Gemini explanation provider or a machine with enough RAM/CPU
for the local Transformers model.
