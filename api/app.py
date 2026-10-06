from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from baiter_app.ml.text_model import generate_headlines

app = FastAPI(
    title="Baiter ML API",
    description="API для генерации кликбейтных заголовков на основе ML-модели T5",
    version="1.0.0",
)


class HeadlineRequest(BaseModel):
    keywords: str


class HeadlineResponse(BaseModel):
    keywords: str
    headlines: list[str]


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Baiter ML API запущен и готов к работе"}


@app.post("/api/generate-headlines", response_model=HeadlineResponse)
def api_generate_headlines(payload: HeadlineRequest):
    if not payload.keywords.strip():
        raise HTTPException(
            status_code=400, detail="Ключевые слова не могут быть пустыми"
        )

    try:
        results = generate_headlines(payload.keywords)
        return HeadlineResponse(keywords=payload.keywords, headlines=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
