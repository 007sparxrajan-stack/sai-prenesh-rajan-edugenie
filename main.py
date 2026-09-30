from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    ExplainRequest, QARequest, QuizRequest, SummaryRequest,
    LearningPathRequest, QuizResponse, ErrorResponse
)
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from config import settings

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini-powered learning assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.app_name},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
        "local_explainer_enabled": settings.enable_local_explainer,
    }


@app.post("/qa")
async def qa(payload: QARequest):
    try:
        return {"answer": answer_question(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
async def explain(payload: ExplainRequest):
    try:
        return {"explanation": explain_concept(payload.topic, payload.level)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse, responses={502: {"model": ErrorResponse}} )
async def quiz(payload: QuizRequest):
    try:
        return generate_quiz(payload.text, payload.count)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    try:
        return {"summary": summarize_text(payload.text, payload.max_sentences)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
async def learning_recommendations(payload: LearningPathRequest):
    try:
        return {"recommendations": get_learning_recommendations(payload.topic, payload.level)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
