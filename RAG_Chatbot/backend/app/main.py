# backend/app/main.py
from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="RAG Chatbot API",
    description="API cho chatbot phát hiện giao dịch bất thường trên blockchain.",
    version="1.0.0"
)

@app.get("/", tags=["Status"])
def read_root():
    return {"status": "API is running"}

# Gắn router API vào ứng dụng chính
app.include_router(api_router, prefix="/api/v1")