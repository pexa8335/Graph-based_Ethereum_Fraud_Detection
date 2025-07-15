# AI Giải thích được (Explainable AI - xAI) trong Phát hiện Bất thường Blockchain

## 1. Tại sao xAI lại quan trọng trong lĩnh vực Blockchain/Fintech?

Trong các lĩnh vực nhạy cảm như tài chính và blockchain, nơi các quyết định của AI có thể ảnh hưởng lớn đến tài sản của người dùng hoặc các quy định pháp lý, việc chỉ đưa ra một dự đoán "bất thường" là chưa đủ. xAI cung cấp khả năng hiểu và tin tưởng vào các quyết định của AI:
*   **Minh bạch và Tin cậy:** Người dùng và các nhà quản lý cần hiểu tại sao một giao dịch lại bị gắn cờ. Điều này xây dựng niềm tin vào hệ thống.
*   **Tuân thủ quy định:** Nhiều quy định (ví dụ: GDPR, các quy định tài chính) yêu cầu các quyết định tự động phải có khả năng giải thích.
*   **Gỡ lỗi và Cải thiện mô hình:** Nếu mô hình đưa ra dự đoán sai, xAI giúp các nhà phát triển hiểu nguyên nhân và cải thiện mô hình.
*   **Hỗ trợ điều tra:** Khi một giao dịch được đánh dấu là bất thường, giải thích của xAI cung cấp manh mối quan trọng cho các nhà phân tích để điều tra sâu hơn.
*   **Giảm thiểu sai sót (False Positives/Negatives):** Hiểu được lý do giúp tinh chỉnh ngưỡng và giảm thiểu các cảnh báo sai.

## 2. Các phương pháp xAI phổ biến

Có nhiều kỹ thuật xAI khác nhau, được chia thành hai loại chính:
*   **Giải thích toàn cục (Global Explanations):** Giải thích cách mô hình hoạt động tổng thể.
*   **Giải thích cục bộ (Local Explanations):** Giải thích lý do cho một dự đoán cụ thể.

Các phương pháp phổ biến bao gồm:

*   **SHAP (SHapley Additive exPlanations):**
    *   **Định nghĩa:** Một phương pháp xAI dựa trên lý thuyết trò chơi, gán một "giá trị" cho mỗi đặc trưng (feature) thể hiện mức độ đóng góp của nó vào dự đoán của mô hình. Giá trị SHAP có thể là dương (tăng khả năng bất thường) hoặc âm (giảm khả năng bất thường).
    *   **Ứng dụng trong Blockchain:** Với output SHAP như `(0.238, 'ERC20 most sent token type_label')`, nó cho biết đặc trưng 'ERC20 most sent token type_label' đã đóng góp một giá trị 0.238 vào việc xác định giao dịch là bất thường. Giá trị dương cho thấy đặc trưng này đẩy dự đoán về phía "bất thường".
    *   **Ưu điểm:** Có nền tảng lý thuyết vững chắc, đảm bảo tính công bằng (fairness), có thể giải thích cho bất kỳ mô hình học máy nào.
*   **LIME (Local Interpretable Model-agnostic Explanations):**
    *   **Định nghĩa:** Xây dựng một mô hình đơn giản, dễ hiểu xung quanh một điểm dữ liệu cụ thể để giải thích dự đoán của mô hình phức tạp tại điểm đó.
    *   **Ưu điểm:** Dễ hiểu, model-agnostic (không phụ thuộc vào loại mô hình).
*   **Feature Importance (Đối với các mô hình cây):**
    *   Các mô hình dựa trên cây như RandomForest (mô hình của bạn) có thể cung cấp trực tiếp độ quan trọng của các đặc trưng, cho biết đặc trưng nào được sử dụng nhiều nhất trong quá trình ra quyết định của cây.

## 3. Tích hợp xAI vào RAG Chatbot

*   **Lưu trữ giải thích:** Các giải thích xAI (đặc biệt là các giá trị SHAP đã được chuyển đổi thành văn bản tự nhiên) sẽ được lưu trữ trong Knowledge Base của RAG, liên kết với ID địa chỉ hoặc giao dịch tương ứng.
*   **Truy vấn bởi Chatbot:** Khi người dùng hỏi "Tại sao địa chỉ X bất thường?", RAG chatbot sẽ truy xuất giải thích xAI liên quan từ Knowledge Base và trình bày cho người dùng.
*   **Cung cấp ngữ cảnh:** Chatbot có thể kết hợp giải thích xAI với các thông tin khác về giao dịch/địa chỉ để đưa ra một cái nhìn toàn diện.