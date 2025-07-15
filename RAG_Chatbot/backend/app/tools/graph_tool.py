# backend/app/tools/graph_tool.py
from smolagents import Tool

class GraphTool(Tool):
    name = "graph_relationship_explorer"
    description = "Truy vấn các mối quan hệ (luồng tiền, tương tác) của một địa chỉ ví bằng cách gọi module đồ thị."
    inputs = {
        "address": {
            "type": "string",
            "description": "Địa chỉ ví Ethereum cần khám phá mối quan hệ.",
        }
    }
    output_type = "string"

    def __init__(self, api_url: str):
        super().__init__()
        self.api_url = api_url

    def forward(self, address: str) -> str:
        print(f"--- GraphTool nhận địa chỉ: {address} ---")
        
        # *** PHẦN GIẢ LẬP ***
        return (
            "Kết quả từ Module Xử lý Đồ thị: "
            f"Địa chỉ {address} đã tương tác với 15 địa chỉ khác. "
            "Trong đó, 3 địa chỉ nhận tiền là các sàn giao dịch lớn. "
            "Phát hiện 1 luồng tiền đáng ngờ đi qua 4 ví trung gian trước khi đến một địa chỉ không xác định."
        )
        # *** KẾT THÚC PHẦN GIẢ LẬP ***