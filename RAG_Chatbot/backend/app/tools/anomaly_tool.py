# backend/app/tools/anomaly_tool.py
from smolagents import Tool
import httpx  # Dùng thư viện này để gọi API, kể cả khi giả lập

class AnomalyTool(Tool):
    name = "anomaly_status_checker"
    description = "Kiểm tra trạng thái bất thường của một địa chỉ ví Ethereum bằng cách gọi module chuyên dụng."
    inputs = {
        "address": {
            "type": "string",
            "description": "Địa chỉ ví Ethereum cần kiểm tra, ví dụ: '0x...'",
        }
    }
    output_type = "string"

    def __init__(self, api_url: str):
        # Tool này cần biết URL của API Module 1
        super().__init__()
        self.api_url = api_url

    def forward(self, address: str) -> str:
        print(f"--- AnomalyTool nhận địa chỉ: {address} ---")
        
        # *** PHẦN GIẢ LẬP - SAU NÀY SẼ THAY BẰNG API CALL THẬT ***
        # Bây giờ, nó chỉ trả về một chuỗi cứng.
        # Khi Module 1 sẵn sàng, mày sẽ thay phần này bằng code gọi API thật.
        if "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8" in address.lower():
             return (
                "Kết quả từ Module Phát hiện Bất thường: "
                "Địa chỉ 0x00009277775ac7d0d59eaad8fee3d10ac6c805e8 được xác định là **Bất thường** với độ tin cậy 92%. "
                "Nguyên nhân chính: Tần suất giao dịch gửi tiền quá cao trong thời gian ngắn, và có liên quan đến một địa chỉ đã bị báo cáo."
            )
        else:
            return (
                "Kết quả từ Module Phát hiện Bất thường: "
                f"Địa chỉ {address} được xác định là **Hợp lệ**."
            )
        # *** KẾT THÚC PHẦN GIẢ LẬP ***