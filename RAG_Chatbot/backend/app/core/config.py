# RAG_chatbot/backend/app/core/config.py
import os
from pathlib import Path  # Dùng pathlib để xử lý đường dẫn cho chuyên nghiệp
from dotenv import load_dotenv

# ==============================================================================
# PHẦN DEBUG ĐƯỜNG DẪN - KHÔNG THỂ SAI ĐƯỢC
# ==============================================================================
print("\n" + "="*60)
print("--- KHỞI ĐỘNG MODULE CONFIG ---")

# Path(biến) sẽ tạo ra một đối tượng đường dẫn thông minh.
# __file__ là đường dẫn đến file này (config.py)
# .resolve() sẽ biến nó thành đường dẫn tuyệt đối, không có sai sót.
CONFIG_FILE_PATH = Path(__file__).resolve()
# .parent sẽ đi lên một thư mục.
# Đi lên 3 cấp từ config.py (core -> app -> backend) sẽ ra thư mục RAG_chatbot
RAG_CHATBOT_ROOT = CONFIG_FILE_PATH.parent.parent.parent.parent
# Đường dẫn đến file .env được xây dựng từ gốc đó
DOTENV_PATH = RAG_CHATBOT_ROOT / "backend" / ".env"

print(f"Thư mục làm việc hiện tại (CWD): {Path.cwd()}")
print(f"Đường dẫn file config.py được giải quyết: {CONFIG_FILE_PATH}")
print(f"Đường dẫn gốc RAG_CHATBOT_ROOT được tính toán: {RAG_CHATBOT_ROOT}")
print(f"Đường dẫn file .env đang tìm kiếm: {DOTENV_PATH}")
print(f"File .env có tồn tại ở đường dẫn trên không? {'CÓ' if DOTENV_PATH.exists() else 'KHÔNG. ĐÂY LÀ VẤN ĐỀ CHÍNH!'}")
print("="*60 + "\n")

# ==============================================================================
# TẢI BIẾN MÔI TRƯỜNG
# ==============================================================================
load_dotenv(dotenv_path=DOTENV_PATH)

def get_env_var(var_name: str, is_path: bool = False) -> str:
    value = os.getenv(var_name)
    if not value: # Kiểm tra cả None và chuỗi rỗng
        raise ValueError(f"Lỗi: Biến môi trường '{var_name}' chưa được thiết lập hoặc để trống trong file .env tại {DOTENV_PATH}")
    
    if is_path:
        # Nối đường dẫn bằng pathlib, an toàn hơn os.path.join
        return str(RAG_CHATBOT_ROOT / value)
    
    return value

# Lấy các cấu hình
try:
    HF_TOKEN = get_env_var("HF_TOKEN")
    LLM_MODEL_NAME = get_env_var("LLM_MODEL_NAME")
    EMBEDDING_MODEL_NAME = get_env_var("EMBEDDING_MODEL_NAME")
    VECTOR_DB_PATH = get_env_var("VECTOR_DB_PATH", is_path=True)
    KNOWLEDGE_DOCS_PATH = get_env_var("KNOWLEDGE_DOCS_PATH", is_path=True)
    DATA_PATH = get_env_var("DATA_PATH", is_path=True)
    ANOMALY_API_URL = get_env_var("ANOMALY_API_URL")
    GRAPH_API_URL = get_env_var("GRAPH_API_URL")
except ValueError as e:
    print(f"LỖI NGHIÊM TRỌNG KHI TẢI CẤU HÌNH: {e}")
    # Thoát tiến trình nếu cấu hình sai, để server không khởi động với trạng thái lỗi
    import sys
    sys.exit(1)