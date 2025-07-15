# backend/app/tools/retriever_tool.py
from smolagents import Tool
from langchain_community.vectorstores import FAISS

class RetrieverTool(Tool):
    name = "knowledge_base_retriever"
    description = "Truy xuất thông tin từ cơ sở dữ liệu nội bộ về địa chỉ ví, giao dịch và các tài liệu kiến thức chung."
    inputs = {
        "query": {
            "type": "string",
            "description": "Câu truy vấn để tìm kiếm thông tin liên quan trong kho kiến thức.",
        }
    }
    output_type = "string"

    def __init__(self, vectordb: FAISS):
        # Tool này cần VectorDB để hoạt động, nên ta truyền nó vào đây.
        # Đây gọi là Dependency Injection. Ghi nhớ thuật ngữ này.
        super().__init__()
        if not isinstance(vectordb, FAISS):
            raise TypeError("vectordb phải là một instance của FAISS.")
        self.vectordb = vectordb

    def forward(self, query: str) -> str:
        print(f"--- RetrieverTool nhận query: {query} ---")
        # Tìm kiếm các tài liệu tương tự
        docs = self.vectordb.similarity_search(query, k=3)

        if not docs:
            return "Không tìm thấy thông tin liên quan trong cơ sở dữ liệu nội bộ."

        # Định dạng kết quả cho đẹp
        retrieved_content = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source', 'Không rõ')
            content = doc.page_content
            retrieved_content.append(f"Trích đoạn {i+1} (Nguồn: {source}):\n{content}\n")
        
        return "\n---\n".join(retrieved_content)