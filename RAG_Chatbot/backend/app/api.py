# backend/app/api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from RAG_Chatbot.backend.app.services.chatbot_service import chatbot_service
# Pydantic model để xác thực dữ liệu đầu vào. Luôn làm điều này.
class ChatRequest(BaseModel):
    question: str

# Tạo một router riêng cho API, để code gọn gàng
router = APIRouter()

@router.post("/chat", tags=["Chatbot"])
def handle_chat(request: ChatRequest):
    """
    Nhận câu hỏi từ người dùng và trả về câu trả lời từ chatbot.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống.")
    
    try:
        answer = chatbot_service.ask(request.question)
        return {"answer": answer}
    except Exception as e:
        # Bắt lỗi chung để API không bị sập
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")