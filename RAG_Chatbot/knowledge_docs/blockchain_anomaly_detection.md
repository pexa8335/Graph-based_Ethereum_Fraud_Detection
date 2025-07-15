# Phát hiện Giao dịch Bất thường trên Blockchain

## 1. Tại sao cần phát hiện bất thường trên Blockchain?

Việc phát hiện các hoạt động bất thường trên blockchain là cực kỳ quan trọng vì nhiều lý do:
*   **Ngăn chặn rửa tiền (Money Laundering):** Blockchain có thể bị lạm dụng để che giấu nguồn gốc của tiền bất hợp pháp.
*   **Chống tài trợ khủng bố (Terrorist Financing):** Ngăn chặn dòng tiền chảy vào các hoạt động khủng bố.
*   **Phát hiện gian lận và lừa đảo (Fraud and Scam Detection):** Xác định các giao dịch liên quan đến lừa đảo Ponzi, phishing, hoặc các hành vi gian lận khác.
*   **Bảo vệ người dùng:** Cảnh báo người dùng về các địa chỉ hoặc giao dịch có rủi ro cao.
*   **Tuân thủ quy định (Regulatory Compliance):** Giúp các tổ chức tài chính và sàn giao dịch tuân thủ các quy định AML/CFT (Chống rửa tiền/Chống tài trợ khủng bố).
*   **An ninh mạng:** Phát hiện các cuộc tấn công mạng như hack sàn giao dịch, tấn công flash loan, hoặc các lỗ hổng bảo mật.

## 2. Các loại hình bất thường phổ biến trên Blockchain

*   **Rửa tiền:** Chia nhỏ các khoản tiền lớn thành nhiều giao dịch nhỏ để che giấu nguồn gốc (smurfing), hoặc chuyển tiền qua nhiều địa chỉ/nền tảng khác nhau.
*   **Lừa đảo Ponzi/Kim tự tháp:** Các giao dịch liên quan đến việc trả lợi nhuận cho nhà đầu tư cũ bằng tiền của nhà đầu tư mới.
*   **Tấn công Phishing/Lừa đảo:** Các giao dịch chuyển tiền đến các địa chỉ lừa đảo do người dùng bị đánh lừa.
*   **Hack và trộm cắp:** Các giao dịch chuyển một lượng lớn tài sản ra khỏi các ví bị xâm nhập.
*   **Giao dịch Flash Loan:** Các khoản vay không cần tài sản thế chấp được thực hiện và trả lại trong cùng một khối, thường được sử dụng để thao túng thị trường hoặc tấn công DeFi.
*   **Hoạt động bất thường về tần suất/giá trị:** Một địa chỉ đột ngột có tần suất giao dịch hoặc giá trị giao dịch rất cao/thấp so với lịch sử.

## 3. Các phương pháp phát hiện bất thường

*   **Dựa trên Quy tắc (Rule-based):**
    *   Đặt ra các ngưỡng hoặc mẫu giao dịch cố định (ví dụ: "nếu một địa chỉ gửi hơn 100 giao dịch trong 1 giờ, đánh dấu là bất thường").
    *   **Ưu điểm:** Đơn giản, dễ hiểu, dễ triển khai.
    *   **Nhược điểm:** Khó mở rộng, dễ bị kẻ tấn công lách luật, không phát hiện được các mẫu bất thường mới.
*   **Dựa trên Học máy (Machine Learning/Deep Learning):**
    *   Sử dụng các thuật toán ML (ví dụ: RandomForest, SVM, Isolation Forest) hoặc DL (ví dụ: Autoencoders, GNN) để học các mẫu giao dịch bình thường và bất thường từ dữ liệu lịch sử.
    *   **Ưu điểm:** Khả năng phát hiện các mẫu phức tạp, tự động thích nghi.
    *   **Nhược điểm:** Cần dữ liệu huấn luyện lớn, khó giải thích kết quả (đặc biệt với DL), có thể bị tấn công đối kháng.
*   **Dựa trên Đồ thị (Graph-based):**
    *   Mô hình hóa các địa chỉ và giao dịch thành một đồ thị, sau đó sử dụng các thuật toán phân tích đồ thị (ví dụ: phát hiện cộng đồng, phân tích đường đi, centrality measures) để tìm các cấu trúc bất thường.
    *   **Ưu điểm:** Hiểu được mối quan hệ phức tạp giữa các thực thể, mạnh mẽ trong việc phát hiện các mạng lưới rửa tiền.
    *   **Nhược điểm:** Phức tạp trong việc xây dựng và phân tích đồ thị lớn.
*   **Kết hợp (Hybrid Approaches):** Sử dụng nhiều phương pháp cùng lúc để tận dụng ưu điểm của từng loại. Ví dụ: sử dụng đặc trưng đồ thị làm đầu vào cho mô hình học máy.