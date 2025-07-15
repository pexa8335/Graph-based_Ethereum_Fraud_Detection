# Câu hỏi thường gặp (FAQ) về Phát hiện Giao dịch Bất thường trên Blockchain

## 1. Hệ thống này phát hiện loại bất thường nào?
Hệ thống này được thiết kế để phát hiện các giao dịch và địa chỉ ví có hành vi đáng ngờ trên blockchain Ethereum. Các loại bất thường có thể bao gồm các hoạt động liên quan đến rửa tiền, lừa đảo, ví bị hack, hoặc các mẫu giao dịch không điển hình khác dựa trên các đặc trưng được trích xuất từ dữ liệu.

## 2. Dữ liệu đầu vào cho mô hình là gì?
Mô hình sử dụng các đặc trưng tổng hợp của địa chỉ ví và giao dịch, bao gồm các chỉ số về thời gian (ví dụ: thời gian trung bình giữa các giao dịch), số lượng giao dịch (gửi, nhận, tạo hợp đồng), giá trị Ether được chuyển (min, max, avg, tổng), và các hoạt động liên quan đến token ERC20 (tổng số giao dịch, giá trị token, số lượng địa chỉ token duy nhất, loại token phổ biến nhất).

## 3. "FLAG 0" và "FLAG 1" có nghĩa là gì?
*   **FLAG 0:** Chỉ ra rằng địa chỉ ví hoặc giao dịch được phân loại là **hợp lệ** hoặc **bình thường**.
*   **FLAG 1:** Chỉ ra rằng địa chỉ ví hoặc giao dịch được phân loại là **bất thường** hoặc **có rủi ro cao**.

## 4. Làm thế nào để hệ thống giải thích lý do một giao dịch bất thường?
Hệ thống sử dụng các kỹ thuật AI giải thích được (xAI), cụ thể là phương pháp SHAP. Khi một địa chỉ được đánh dấu là bất thường, SHAP sẽ phân tích và chỉ ra những đặc trưng nào (ví dụ: "ERC20 most sent token type_label", "Time Diff between first and last (Mins)") đã đóng góp nhiều nhất vào quyết định đó, và mức độ ảnh hưởng của chúng. Điều này giúp người dùng hiểu rõ nguyên nhân.

## 5. Hệ thống có thể cung cấp thông tin về các mối quan hệ giữa các địa chỉ không?
Có, hệ thống có thể cung cấp thông tin về các mối quan hệ đồ thị giữa các địa chỉ. Mặc dù không hiển thị sơ đồ trực tiếp, chatbot có thể tóm tắt các thông tin như số lượng địa chỉ duy nhất đã gửi/nhận Ether hoặc token ERC20, hoặc các đặc trưng đồ thị đã được tính toán trước (ví dụ: điểm PageRank, Betweenness Centrality) để mô tả vai trò của một địa chỉ trong mạng lưới.

## 6. Tôi có thể hỏi về các khái niệm blockchain chung không?
Có. Nếu câu hỏi của bạn nằm ngoài phạm vi dữ liệu nội bộ của hệ thống (ví dụ: "Blockchain là gì?", "Cách hoạt động của dApp?"), chatbot sẽ sử dụng công cụ tìm kiếm web (Google Search) để truy xuất thông tin và cung cấp câu trả lời.

## 7. Hệ thống có thể dự đoán tương lai của một địa chỉ không?
Không, hệ thống hiện tại chỉ phân tích dữ liệu lịch sử và các đặc trưng hiện có để đưa ra dự đoán về trạng thái bất thường. Nó không có khả năng dự đoán hành vi tương lai của một địa chỉ.

## 8. Độ chính xác của hệ thống là bao nhiêu?
Mô hình phát hiện bất thường đã được huấn luyện và đánh giá với độ chính xác cao trên bộ dữ liệu kiểm thử. Tuy nhiên, không có hệ thống nào là hoàn hảo và luôn có khả năng xảy ra sai sót (False Positives hoặc False Negatives). Các giải thích xAI giúp bạn đánh giá và tin tưởng hơn vào các dự đoán.

## 9. Tôi có thể sử dụng hệ thống này để đưa ra quyết định tài chính không?
Hệ thống này chỉ cung cấp thông tin phân tích và cảnh báo. Các kết quả dự đoán không nên được coi là lời khuyên tài chính hoặc pháp lý. Mọi quyết định tài chính cần được đưa ra sau khi nghiên cứu kỹ lưỡng và tham khảo ý kiến chuyên gia.