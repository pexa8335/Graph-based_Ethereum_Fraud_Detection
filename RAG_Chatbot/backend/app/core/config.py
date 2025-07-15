# RAG_chatbot/backend/app/core/config.py
import os
from dotenv import load_dotenv

# ==============================================================================
# XÂY DỰNG ĐƯỜNG DẪN TUYỆT ĐỐI - LÀM MỘT LẦN, DÙNG MỌI NƠI
# ==============================================================================

# 1. Xác định đường dẫn gốc của module RAG_chatbot
# Từ file này (config.py) đi lên 3 cấp sẽ ra thư mục RAG_chatbot
# app/core/ -> app/ -> backend/ -> RAG_chatbot/
RAG_CHATBOT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Xây dựng đường dẫn đến file .env
DOTENV_PATH = os.path.join(RAG_CHATBOT_ROOT, 'backend', '.env')

# 3. Tải .env
if not os.path.exists(DOTENV_PATH):
    print(f"CẢNH BÁO: Không tìm thấy file .env tại {DOTENV_PATH}. Các cấu hình có thể bị thiếu.")
load_dotenv(dotenv_path=DOTENV_PATH)

# ==============================================================================
# HÀM HELPER VÀ CÁC BIẾN CẤU HÌNH
# ==============================================================================

def get_env_var(var_name: str, is_path: bool = False) -> str:
    """
    Lấy biến môi trường. Nếu là đường dẫn, xây dựng đường dẫn tuyệt đối.
    Báo lỗi nếu không tìm thấy.
    """
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Lỗi: Biến môi trường '{var_name}' chưa được thiết lập trong file .env")
    
    if is_path:
        # Nối đường dẫn tương đối từ .env với đường dẫn gốc của dự án
        return os.path.join(RAG_CHATBOT_ROOT, value)
    
    return value

# Lấy các cấu hình bằng hàm helper
# is_path=True sẽ tự động biến nó thành đường dẫn tuyệt đối
HF_TOKEN = get_env_var("HF_TOKEN")
LLM_MODEL_NAME = get_env_var("LLM_MODEL_NAME")
EMBEDDING_MODEL_NAME = get_env_var("EMBEDDING_MODEL_NAME")

VECTOR_DB_PATH = get_env_var("VECTOR_DB_PATH", is_path=True)
KNOWLEDGE_DOCS_PATH = get_env_var("KNOWLEDGE_DOCS_PATH", is_path=True)
DATA_PATH = get_env_var("DATA_PATH", is_path=True)

ANOMALY_API_URL = get_env_var("ANOMALY_API_URL")
GRAPH_API_URL = get_env_var("GRAPH_API_URL")