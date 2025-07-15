# backend/app/services/chatbot_service.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama.llms import OllamaLLM
from langchain.tools import tool
from app.core import config
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent

# ==============================================================================
# --- ĐỊNH NGHĨA CÁC TOOL BÊN NGOÀI CLASS ---
# Các tool này là các hàm độc lập.
# ==============================================================================

@tool
def knowledge_base_retriever(query: str) -> str:
    """
    Truy xuất thông tin từ cơ sở dữ liệu nội bộ về địa chỉ ví, giao dịch và các tài liệu kiến thức chung.
    Rất hữu ích để trả lời các câu hỏi về định nghĩa, khái niệm hoặc thông tin có trong tài liệu.
    """
    print(f"--- [Tool Call] knowledge_base_retriever với query: {query} ---")
    # --- TRUY CẬP INSTANCE chatbot_service ĐỂ LẤY VECTORDB ---
    # Đây là một "trick" nhỏ: vì chatbot_service là một instance toàn cục trong module này,
    # tool có thể gọi nó để truy cập các thuộc tính như vectordb.
    docs = chatbot_service.vectordb.similarity_search(query, k=3)
    if not docs:
        return "Không tìm thấy thông tin liên quan."
    return "\n---\n".join([doc.page_content for doc in docs])

@tool
def anomaly_status_checker(address: str) -> str:
    """
    Kiểm tra trạng thái bất thường của một địa chỉ ví Ethereum cụ thể.
    Sử dụng công cụ này khi người dùng hỏi một địa chỉ có phải là lừa đảo, gian lận, hay bất thường không.
    """
    print(f"--- [Tool Call] anomaly_status_checker với địa chỉ: {address} ---")
    # Logic giả lập
    if "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8" in address.lower():
        return "Kết quả từ Module Phát hiện Bất thường: Địa chỉ được xác định là Bất thường."
    else:
        return "Kết quả từ Module Phát hiện Bất thường: Địa chỉ được xác định là Hợp lệ."

@tool
def graph_relationship_explorer(address: str) -> str:
    """
    Truy vấn và khám phá các mối quan hệ (luồng tiền, tương tác) của một địa chỉ ví Ethereum.
    Sử dụng khi người dùng hỏi một địa chỉ đã gửi tiền cho ai, nhận tiền từ đâu, hoặc có liên quan đến các địa chỉ nào khác.
    """
    print(f"--- [Tool Call] graph_relationship_explorer với địa chỉ: {address} ---")
    # Logic giả lập
    return "Kết quả từ Module Xử lý Đồ thị: Địa chỉ đã tương tác với 15 địa chỉ khác, trong đó có 1 luồng tiền đáng ngờ."

# ==============================================================================
# --- CLASS CHATBOT SERVICE ---
# Class này bây giờ chỉ chịu trách nhiệm khởi tạo và quản lý agent.
# ==============================================================================

class ChatbotService:
    def __init__(self):
        print("Đang khởi tạo ChatbotService...")
        
        # 1. Lấy cấu hình trực tiếp từ module config
        self.llm = OllamaLLM(model=config.LLM_MODEL_NAME)
        self.embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
        
        # 2. Tải VectorDB bằng đường dẫn tuyệt đối đã được xử lý sẵn
        print(f"Đang tải VectorDB từ: {config.VECTOR_DB_PATH}")
        self.vectordb = FAISS.load_local(
            config.VECTOR_DB_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )
        
        # 3. Gom các tool đã định nghĩa ở trên vào một danh sách
        self.tools = [
            knowledge_base_retriever,
            anomaly_status_checker,
            graph_relationship_explorer
        ]

        # 4. Lấy prompt
        prompt = hub.pull("hwchase17/react")

        # 5. Tạo Agent
        agent = create_react_agent(self.llm, self.tools, prompt)

        # 6. Tạo Agent Executor
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        print("ChatbotService với Ollama (ReAct Agent) đã sẵn sàng.")

    def ask(self, question: str) -> str:
        print(f"Nhận câu hỏi: {question}")
        try:
            response = self.agent_executor.invoke({"input": question})
            return response.get("output", "Không có output.")
        except Exception as e:
            print(f"LỖI KHI CHẠY AGENT: {e}")
            return "Xin lỗi, đã có lỗi xảy ra trong quá trình xử lý. Vui lòng thử lại."

# --- TẠO INSTANCE DUY NHẤT ---
# Dòng này phải nằm cuối cùng, sau khi tất cả các class và tool đã được định nghĩa.
chatbot_service = ChatbotService()