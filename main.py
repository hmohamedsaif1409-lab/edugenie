from pathlib import Path
import asyncio

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import TextRequest, QuizRequest, LearningPathRequest
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "ai_provider": settings.ai_provider,
        "gemini_configured": bool(settings.gemini_api_key),
    }


def _validate_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    if len(value) > settings.max_input_chars:
        raise HTTPException(
            status_code=413,
            detail=f"Input is too long. Maximum is {settings.max_input_chars} characters.",
        )
    return value


@app.post("/qa")
async def qa(payload: TextRequest):
    text = _validate_text(payload.text)
    return {"answer": await asyncio.to_thread(answer_question, text)}


@app.post("/explain")
async def explain(payload: TextRequest):
    text = _validate_text(payload.text)
    return {"explanation": await asyncio.to_thread(explain_concept, text)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    text = _validate_text(payload.text)
    return await asyncio.to_thread(generate_quiz, text)


@app.post("/summarize")
async def summarize(payload: TextRequest):
    text = _validate_text(payload.text)
    return {"summary": await asyncio.to_thread(summarize_text, text)}


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    topic = _validate_text(payload.topic)
    return {
        "recommendations": await asyncio.to_thread(
            get_learning_recommendations, topic, payload.level
        )
    }
