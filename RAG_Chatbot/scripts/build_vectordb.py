# scripts/build_vectordb.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoTokenizer

# 1. Xác định đường dẫn gốc của module RAG_chatbot
# __file__ là đường dẫn đến chính file này (build_vectordb.py)
# os.path.abspath(__file__) -> Lấy đường dẫn tuyệt đối
# os.path.dirname(...) -> Lấy thư mục chứa file đó (tức là thư mục 'scripts')
# os.path.dirname(...) một lần nữa -> Đi lên một cấp, ra thư mục 'RAG_chatbot'
RAG_CHATBOT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(RAG_CHATBOT_ROOT, 'backend', '.env')

print(f"Đang tải biến môi trường từ: {DOTENV_PATH}")
if not os.path.exists(DOTENV_PATH):
    raise FileNotFoundError(f"Lỗi: Không tìm thấy file .env tại đường dẫn mong muốn: {DOTENV_PATH}")
load_dotenv(dotenv_path=DOTENV_PATH)


# --- KIỂM TRA TỪNG BIẾN MÔI TRƯỜNG ---
# Mục đích: Đảm bảo chương trình không chạy với cấu hình rỗng và báo lỗi sớm.

def get_env_var(var_name: str) -> str:
    """Hàm này lấy một biến môi trường và báo lỗi nếu không tìm thấy."""
    value = os.getenv(var_name)
    if value is None:
        # Báo lỗi ngay lập tức, chỉ rõ biến nào bị thiếu.
        raise ValueError(f"Lỗi: Biến môi trường '{var_name}' chưa được thiết lập trong file .env")
    return value

# Lấy các biến một cách an toàn
EMBEDDING_MODEL_NAME = get_env_var("EMBEDDING_MODEL_NAME")
vector_db_rel_path = get_env_var("VECTOR_DB_PATH")
knowledge_docs_rel_path = get_env_var("KNOWLEDGE_DOCS_PATH")
data_rel_path = get_env_var("DATA_PATH")

# Chỉ khi đã chắc chắn có giá trị, ta mới xây dựng đường dẫn tuyệt đối.
# Bây giờ sẽ không còn gạch đỏ nữa vì Linter biết các biến này chắc chắn là string.
VECTOR_DB_PATH = os.path.join(RAG_CHATBOT_ROOT, vector_db_rel_path)
KNOWLEDGE_DOCS_PATH = os.path.join(RAG_CHATBOT_ROOT, knowledge_docs_rel_path)
DATA_PATH = os.path.join(RAG_CHATBOT_ROOT, data_rel_path)


def build_knowledge_base():
    """
    Hàm này đọc tất cả dữ liệu nguồn (CSV, Markdown), xử lý,
    tạo embedding và lưu trữ thành một FAISS vector database.
    """
    print("Bắt đầu xây dựng Knowledge Base...")
    source_docs = []

    # 1. Tải dữ liệu từ CSV
    print(f"Đang tải dữ liệu từ {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    for _, row in df.iterrows():
        # Mày có thể tạo mô tả chi tiết hơn ở đây, giống như trong notebook
        content = f"Thông tin địa chỉ ví: {row.get('Address', 'N/A')}. Trạng thái: {'bất thường' if row['FLAG'] == 1 else 'hợp lệ'}..."
        metadata = {"source": "csv_data", "address": row.get('Address', 'N/A')}
        source_docs.append(Document(page_content=content, metadata=metadata))

    # 2. Tải tài liệu từ Markdown
    print(f"Đang tải tài liệu từ {KNOWLEDGE_DOCS_PATH}...")
    loader = DirectoryLoader(
        KNOWLEDGE_DOCS_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    md_docs = loader.load()
    source_docs.extend(md_docs)
    print(f"Tổng cộng có {len(source_docs)} tài liệu nguồn.")

    # 3. Chia nhỏ văn bản (Chunking)
    print("Đang chia nhỏ tài liệu...")
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(EMBEDDING_MODEL_NAME),
        chunk_size=500,
        chunk_overlap=100,
    )
    docs_processed = text_splitter.split_documents(source_docs)
    print(f"Đã chia thành {len(docs_processed)} chunks.")

    # 4. Tạo Embeddings và xây dựng FAISS
    print(f"Đang tạo embeddings với model: {EMBEDDING_MODEL_NAME}...")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    vector_db = FAISS.from_documents(
        documents=docs_processed,
        embedding=embedding_model
    )
    print("Đã xây dựng Vector DB.")

    # 5. Lưu Vector DB
    vector_db.save_local(VECTOR_DB_PATH)
    print(f"Đã lưu Vector Database thành công vào: {VECTOR_DB_PATH}")

if __name__ == "__main__":
    build_knowledge_base()