# RAG_chatbot/backend/app/services/chatbot_service.py
import httpx
import re
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.tools import tool
from duckduckgo_search import DDGS
from RAG_Chatbot.backend.app.core import config

# ==============================================================================
# --- ĐỊNH NGHĨA CÁC TOOL BÊN NGOÀI CLASS ---
# Các tool này là các hàm độc lập.
# ==============================================================================
# Trong chatbot_service.py

@tool
def internet_search(query: str) -> str:
    """
    Sử dụng để tìm kiếm thông tin mới nhất trên Internet về các sự kiện, tin tức, giá cả, hoặc kiến thức chung.
    """
    print(f"--- [Tool Call] internet_search với query: {query} ---")
    try:
        with DDGS(timeout=20) as ddgs:
            results = ddgs.text(query, region='us-en', max_results=7) # Lấy nhiều hơn một chút để có cái mà lọc
            
            if not results:
                return "Không tìm thấy kết quả nào."

            # --- LỚP LỌC KẾT QUẢ ---
            # Chỉ giữ lại các kết quả có chứa các từ khóa liên quan trong tiêu đề hoặc tóm tắt
            keywords = query.lower().split()
            filtered_results = []
            for res in results:
                content_lower = (res['title'] + res['body']).lower()
                # Nếu ít nhất một từ khóa có trong nội dung, ta coi nó là liên quan
                if any(keyword in content_lower for keyword in keywords):
                    filtered_results.append(res)
            
            if not filtered_results:
                return "Không tìm thấy kết quả liên quan sau khi lọc."

            # Chỉ lấy 3 kết quả tốt nhất sau khi lọc
            final_results = filtered_results[:3]
            
            # Định dạng lại kết quả
            formatted_results = []
            for i, res in enumerate(final_results):
                formatted_results.append(f"Kết quả {i+1}:\n- Tiêu đề: {res['title']}\n- Tóm tắt: {res['body']}")
            
            return "\n".join(formatted_results)

    except Exception as e:
        return f"Lỗi khi thực hiện tìm kiếm trên web: {e}"


@tool
def knowledge_base_retriever(query: str) -> str:
    """
    CHỈ SỬ DỤNG KHI cần truy xuất thông tin kỹ thuật về các khái niệm của blockchain Ethereum,
    hoặc thông tin chi tiết về các giao dịch, địa chỉ ví CÓ SẴN trong cơ sở dữ liệu nội bộ.
    KHÔNG dùng để hỏi về tin tức, giá cả, hoặc các sự kiện mới.
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
    CHỈ SỬ DỤNG để kiểm tra trạng thái bất thường của một ĐỊA CHỈ VÍ ETHEREUM cụ thể.
    Đầu vào BẮT BUỘC phải là một chuỗi địa chỉ ví, ví dụ: '0x...'.
    """
    print(f"--- [Tool Call] anomaly_status_checker với địa chỉ: {address} ---")
    # Logic giả lập
    if "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8" in address.lower():
        return "Kết quả từ Module Phát hiện Bất thường: Địa chỉ được xác định là Bất thường."
    else:
        return "Kết quả từ Module Phát hiện Bất thường: Địa chỉ được xác định là Hợp lệ."

# Dùng khi có API thật
# @tool
# def anomaly_status_checker(address: str) -> str:
#     """
#     Kiểm tra trạng thái bất thường của một địa chỉ ví Ethereum cụ thể.
#     Sử dụng công cụ này khi người dùng hỏi một địa chỉ có phải là lừa đảo, gian lận, hay bất thường không.
#     CHỈ SỬ DỤNG để kiểm tra trạng thái bất thường của một ĐỊA CHỈ VÍ ETHEREUM cụ thể.
#     Đầu vào BẮT BUỘC phải là một chuỗi địa chỉ ví, ví dụ: '0x...'.
#     """
#     print(f"--- [Tool Call] anomaly_status_checker với địa chỉ: {address} ---")
    
#     # Lấy URL thật từ config
#     api_url = config.ANOMALY_API_URL
    
#     try:
#         # Dùng httpx để gọi API. `with` sẽ tự động đóng kết nối.
#         with httpx.Client(timeout=10.0) as client:
#             # Gửi request POST với payload là JSON
#             response = client.post(api_url, json={"address": address})
            
#             # Ném ra lỗi nếu server trả về mã 4xx hoặc 5xx
#             response.raise_for_status() 
            
#             data = response.json()
#             # Trả về một chuỗi mô tả kết quả cho LLM
#             is_anomaly = data.get("is_anomaly", False)
#             explanation = data.get("explanation", "Không có giải thích.")
#             status = "Bất thường" if is_anomaly else "Hợp lệ"
            
#             return f"Kết quả từ Module Phát hiện Bất thường: Địa chỉ được xác định là **{status}**. Giải thích: {explanation}"

#     except httpx.HTTPStatusError as e:
#         # Bắt lỗi cụ thể từ server (ví dụ: 404 Not Found, 500 Internal Server Error)
#         return f"API phát hiện bất thường báo lỗi: {e.response.status_code}. Chi tiết: {e.response.text}"
#     except httpx.RequestError as e:
#         # Bắt lỗi kết nối mạng (ví dụ: không kết nối được server, timeout)
#         return f"Lỗi kết nối đến API phát hiện bất thường. Vui lòng kiểm tra xem module đó đã chạy chưa. Chi tiết: {e}"
#     except Exception as e:
#         # Bắt các lỗi không mong muốn khác
#         return f"Đã có lỗi không xác định xảy ra khi gọi API: {e}"

@tool
def graph_relationship_explorer(address: str) -> str:
    """
    Truy vấn và khám phá các mối quan hệ (luồng tiền, tương tác) của một địa chỉ ví Ethereum.
    Sử dụng khi người dùng hỏi một địa chỉ đã gửi tiền cho ai, nhận tiền từ đâu, hoặc có liên quan đến các địa chỉ nào khác.
    CHỈ SỬ DỤNG để khám phá các mối quan hệ của một ĐỊA CHỈ VÍ ETHEREUM cụ thể.
    Đầu vào BẮT BUỘC phải là một chuỗi địa chỉ ví, ví dụ: '0x...'.
    """
    print(f"--- [Tool Call] graph_relationship_explorer với địa chỉ: {address} ---")
    # Logic giả lập
    return "Kết quả từ Module Xử lý Đồ thị: Địa chỉ đã tương tác với 15 địa chỉ khác, trong đó có 1 luồng tiền đáng ngờ."

# Dùng khi có API thật
# @tool
# def graph_relationship_explorer(address: str) -> str:
#     """
#     Truy vấn và khám phá các mối quan hệ (luồng tiền, tương tác) của một địa chỉ ví Ethereum bằng cách gọi API của module đồ thị.
#     CHỈ SỬ DỤNG để khám phá các mối quan hệ của một ĐỊA CHỈ VÍ ETHEREUM cụ thể.
#     Đầu vào BẮT BUỘC phải là một chuỗi địa chỉ ví, ví dụ: '0x...'.   
#     """
#     print(f"--- [Tool Call] graph_relationship_explorer với địa chỉ: {address} ---")
    
#     # Bước 1: Lấy URL thật của Module 3 từ config
#     api_url = config.GRAPH_API_URL
    
#     # Kiểm tra xem URL có được cấu hình không
#     if not api_url or "placeholder" in api_url:
#         return "Lỗi cấu hình: URL của Graph Handling API chưa được thiết lập."

#     try:
#         # Bước 2: Gọi API bằng httpx
#         with httpx.Client(timeout=15.0) as client: # Có thể cho timeout dài hơn một chút vì truy vấn đồ thị có thể phức tạp
            
#             # Bước 3: Gửi đúng Payload theo API Contract đã thống nhất với team Module 3
#             response = client.post(api_url, json={"address": address})
            
#             # Ném ra lỗi nếu server trả về mã 4xx hoặc 5xx
#             response.raise_for_status() 
            
#             # Bước 4: Xử lý Response JSON
#             data = response.json()
            
#             # Rút ra các thông tin cần thiết từ JSON trả về
#             # Giả sử API trả về các key 'interaction_count' và 'summary'
#             interaction_count = data.get("interaction_count", 0)
#             summary = data.get("summary", "Không có tóm tắt chi tiết.")
            
#             # Bước 5: Định dạng Output thành một câu trả lời tự nhiên
#             return f"Kết quả từ Module Xử lý Đồ thị: Địa chỉ này đã tương tác với {interaction_count} địa chỉ khác. Tóm tắt: {summary}"

#     # Bước 6: Xử lý Lỗi (y hệt như tool kia)
#     except httpx.HTTPStatusError as e:
#         return f"API xử lý đồ thị báo lỗi: {e.response.status_code}. Chi tiết: {e.response.text}"
#     except httpx.RequestError as e:
#         return f"Lỗi kết nối đến API xử lý đồ thị. Vui lòng kiểm tra xem module đó đã chạy chưa. Chi tiết: {e}"
#     except Exception as e:
#         return f"Đã có lỗi không xác định xảy ra khi gọi API đồ thị: {e}"


# ==============================================================================
# --- CLASS CHATBOT SERVICE ---
# Class này bây giờ chỉ chịu trách nhiệm khởi tạo và quản lý agent.
# ==============================================================================

# --- VÒNG LẶP AGENT TỰ XÂY DỰNG ---
class ManualAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.prompt_template = self._build_prompt_template()

# Trong ManualAgent

    def _build_prompt_template(self):
            # Xây dựng phần mô tả tools cho prompt
        tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools.values()])
        tool_names = ", ".join(self.tools.keys())

            # Đây là một ví dụ mẫu (few-shot example) để dạy cho LLM
        example = """
        Question: Địa chỉ 0x123... có phải là lừa đảo không và có tin tức gì về nó không?
        Thought: Người dùng muốn làm hai việc: kiểm tra trạng thái bất thường của một địa chỉ và tìm kiếm tin tức liên quan. Tôi sẽ bắt đầu bằng việc kiểm tra trạng thái trước.
        Action: anomaly_status_checker
        Action Input: 0x123...
        Observation: Kết quả từ Module Phát hiện Bất thường: Địa chỉ được xác định là Bất thường. Giải thích: Tương tác với các địa chỉ trong danh sách đen.
        Thought: OK, địa chỉ này là bất thường. Bây giờ tôi cần tìm tin tức về nó để cung cấp thêm ngữ cảnh cho người dùng. Tôi sẽ dùng công cụ tìm kiếm web.
        Action: internet_search
        Action Input: "địa chỉ lừa đảo 0x123..."
        Observation: Kết quả 1: Tiêu đề: Cảnh báo về địa chỉ lừa đảo 0x123... trên diễn đàn CryptoScamAlert...
        Thought: Tôi đã có đủ thông tin. Địa chỉ này được xác nhận là bất thường bởi hệ thống nội bộ và cũng có các báo cáo công khai trên internet. Bây giờ tôi sẽ tổng hợp và trả lời.
        Final Answer: Có, địa chỉ 0x123... được xác định là bất thường. Hệ thống của chúng tôi phát hiện nó có tương tác với các địa chỉ trong danh sách đen. Ngoài ra, một tìm kiếm trên internet cũng cho thấy các cảnh báo về địa chỉ này trên diễn đàn CryptoScamAlert.
        """

            # Prompt cuối cùng, kết hợp tất cả các yếu tố
        return f"""
        Bạn là một Trợ lý Phân tích Blockchain chuyên nghiệp. Nhiệm vụ của bạn là sử dụng các công cụ một cách logic và hiệu quả để trả lời câu hỏi của người dùng một cách chính xác.

        **QUY TẮC VÀNG:**
        1.  **PHÂN TÍCH & LẬP KẾ HOẠCH:** Luôn bắt đầu bằng `Thought` để phân tích câu hỏi và vạch ra kế hoạch hành động từng bước.
        2.  **HÀNH ĐỘNG CHÍNH XÁC:** Chọn một công cụ (Action) và cung cấp đầu vào (Action Input) phù hợp.
        3.  **ĐÁNH GIÁ & QUYẾT ĐỊNH:** Sau mỗi `Observation`, hãy suy nghĩ xem thông tin đã đủ chưa.
            - NẾU CHƯA ĐỦ: Hãy suy nghĩ về bước tiếp theo (dùng tool khác hoặc dùng lại tool cũ với input khác).
            - NẾU ĐỦ: Dừng lại ngay lập tức và viết `Final Answer:`.
        4.  **TỔNG HỢP THÔNG MINH:** `Final Answer` PHẢI là một bản tóm tắt tổng hợp, mạch lạc, không phải là một bản sao chép của `Observation`.

        **CÁC CÔNG CỤ CỦA BẠN:**
        {tool_descriptions}

        **ĐỊNH DẠNG OUTPUT BẮT BUỘC (TUYỆT ĐỐI KHÔNG THAY ĐỔI):**
        Thought: [suy nghĩ và kế hoạch của bạn]
        Action: {tool_names}
        Action Input: [đầu vào cho công cụ]

        ---
        **VÍ DỤ MẪU HOÀN HẢO:**
        {example}
        ---

        **BẮT ĐẦU THỰC HIỆN NHIỆM VỤ:**

        **Lịch sử các bước đã thực hiện:**
        {{history}}

        **Câu hỏi mới của người dùng:** {{input}}
        Thought:
        """

    def _parse_llm_output(self, text: str):
        """
        Hàm phân tích output của LLM, được thiết kế để xử lý các biến thể định dạng.
        Nó sẽ tìm các cặp khóa-giá trị "Action" và "Action Input".
        """
        # Xóa các ký tự markdown (**, `) để làm sạch text
        cleaned_text = text.replace("`", "").replace("*", "")

        # Tìm Action
        action_match = re.search(r"Action:\s*(\S+)", cleaned_text, re.IGNORECASE)
        action = action_match.group(1).strip() if action_match else None

        # Tìm Action Input
        # Tìm kiếm mọi thứ nằm sau "Action Input:" cho đến hết dòng
        input_match = re.search(r"Action Input:\s*(.*)", cleaned_text, re.IGNORECASE)
        action_input = input_match.group(1).strip().strip('"') if input_match else None # Xóa luôn dấu "" ở đầu/cuối

        if not action or action_input is None: # Kiểm tra cả action_input is None vì nó có thể là chuỗi rỗng
            print(f"--- PARSER DEBUG ---")
            print(f"Text gốc: {text}")
            print(f"Text đã làm sạch: {cleaned_text}")
            print(f"Action tìm thấy: {action}")
            print(f"Action Input tìm thấy: {action_input}")
            print(f"--------------------")
            return None, None

        return action, action_input

 # Trong class ManualAgent

    # Trong class ManualAgent

# Trong class ManualAgent

    def run(self, user_input: str, max_loops=7):
        history = ""
        for i in range(max_loops):
            print(f"\n--- VÒNG LẶP {i+1} ---")

            full_prompt = self.prompt_template.format(history=history, input=user_input)
            
            llm_output = self.llm.invoke(full_prompt)
            print(f"LLM Output:\n{llm_output}")

            if "Final Answer:" in llm_output:
                # Logic xử lý Final Answer giữ nguyên
                answer_part = llm_output.split("Final Answer:", 1)[-1]
                stop_phrases = ["Thought:", "Action:", "Observation:", "Lịch sử", "Nhiệm vụ"]
                earliest_stop_pos = len(answer_part)
                for phrase in stop_phrases:
                    pos = answer_part.lower().find(phrase.lower())
                    if pos != -1 and pos < earliest_stop_pos:
                        earliest_stop_pos = pos
                final_answer = answer_part[:earliest_stop_pos].strip()
                if final_answer:
                    return final_answer

            # --- LOGIC MỚI: XỬ LÝ TRƯỜNG HỢP LLM TRẢ LỜI THẲNG ---
            action, action_input = self._parse_llm_output(llm_output)

            if not action:
                # Nếu không parse được Action, nhưng output có nội dung
                # thì rất có thể LLM đã trả lời thẳng.
                # Ta chấp nhận câu trả lời này.
                if len(llm_output.strip()) > 5: # Kiểm tra để chắc chắn nó không phải là một chuỗi rỗng vớ vẩn
                    print("--- Phát hiện LLM trả lời trực tiếp, không dùng tool. Chấp nhận câu trả lời. ---")
                    return llm_output.strip()
                else:
                    return "Lỗi: AI không đưa ra được hành động hoặc câu trả lời hợp lệ."

            if action not in self.tools:
                return f"Lỗi: AI đã chọn một công cụ không hợp lệ: {action}"

            # Phần còn lại của vòng lặp giữ nguyên
            print(f"Thực thi Tool: {action}, Input: {action_input}")
            tool_to_run = self.tools[action]
            try:
                observation = tool_to_run.run(action_input)
            except Exception as e:
                observation = f"Lỗi khi chạy tool: {e}"
            
            print(f"Observation:\n{observation}")

            history += f"{llm_output}\nObservation: {observation}\n"
        
        return "Agent đã dừng do đạt đến giới hạn số vòng lặp."

# --- CLASS CHATBOT SERVICE ---
class ChatbotService:
    def __init__(self):
        print("Đang khởi tạo ChatbotService (Manual Agent)...")
        # Dùng Ollama bản thường
        self.llm = Ollama(model=config.LLM_MODEL_NAME)
        
        self.embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
        self.vectordb = FAISS.load_local(
            config.VECTOR_DB_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        tools = [
            internet_search,
            knowledge_base_retriever,
            anomaly_status_checker,
            graph_relationship_explorer,
        ]

        # Khởi tạo Manual Agent của chúng ta
        self.agent = ManualAgent(self.llm, tools)
        print("ChatbotService (Manual Agent) đã sẵn sàng.")

    def ask(self, question: str) -> str:
        return self.agent.run(question)

# --- INSTANCE ---
chatbot_service = ChatbotService()