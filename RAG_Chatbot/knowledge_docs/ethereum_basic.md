# Kiến thức cơ bản về Blockchain Ethereum và Giao dịch

Ethereum là một nền tảng blockchain phi tập trung, mã nguồn mở với chức năng hợp đồng thông minh. Ether (ETH) là tiền điện tử gốc của Ethereum, được sử dụng để thanh toán phí giao dịch (gas fees) và là tài sản chính trong mạng lưới.

## 1. Địa chỉ ví Ethereum (Ethereum Addresses)

*   **Định nghĩa:** Một địa chỉ ví Ethereum là một chuỗi ký tự chữ và số (ví dụ: `0x00009277775ac7d0d59eaad8fee3d10ac6c805e8`) đại diện cho một tài khoản trên blockchain Ethereum. Các địa chỉ này có thể là tài khoản thuộc sở hữu bên ngoài (EOA - External Owned Account), được kiểm soát bởi khóa riêng tư, hoặc tài khoản hợp đồng (Contract Account), được kiểm soát bởi mã code.
*   **Vai trò:** Địa chỉ ví được sử dụng để gửi, nhận Ether và các token khác, cũng như tương tác với các hợp đồng thông minh.

## 2. Giao dịch (Transactions)

*   **Định nghĩa:** Một giao dịch trên Ethereum là một bản ghi được ký điện tử về một tương tác trên blockchain. Mỗi giao dịch đều được ghi lại vĩnh viễn trên sổ cái phân tán.
*   **Các loại giao dịch chính:**
    *   **Giao dịch chuyển Ether:** Chuyển một lượng Ether từ địa chỉ này sang địa chỉ khác.
    *   **Giao dịch tạo hợp đồng:** Triển khai một hợp đồng thông minh mới lên blockchain.
    *   **Giao dịch tương tác hợp đồng:** Gọi một hàm (function) trong một hợp đồng thông minh đã tồn tại.
*   **Các thuộc tính quan trọng của giao dịch:**
    *   **Địa chỉ gửi (From Address):** Địa chỉ ví khởi tạo giao dịch.
    *   **Địa chỉ nhận (To Address):** Địa chỉ ví đích hoặc địa chỉ hợp đồng.
    *   **Giá trị (Value):** Lượng Ether được chuyển (nếu có).
    *   **Phí Gas (Gas Fee):** Chi phí để thực hiện giao dịch trên mạng lưới.
    *   **Dữ liệu đầu vào (Input Data):** Dữ liệu tùy chọn được gửi cùng với giao dịch, thường được sử dụng khi tương tác với hợp đồng thông minh.

## 3. Hợp đồng thông minh (Smart Contracts)

*   **Định nghĩa:** Hợp đồng thông minh là các chương trình máy tính tự thực thi được lưu trữ và chạy trên blockchain. Chúng tự động hóa việc thực hiện các thỏa thuận mà không cần bên trung gian.
*   **Tạo hợp đồng:** Khi một địa chỉ tạo một hợp đồng thông minh, một địa chỉ hợp đồng mới sẽ được sinh ra. Các giao dịch sau đó có thể tương tác với địa chỉ hợp đồng này.

## 4. Phí Gas (Gas Fees)

*   **Định nghĩa:** Gas là đơn vị đo lường công việc tính toán cần thiết để thực hiện một giao dịch hoặc hợp đồng thông minh trên Ethereum. Phí gas được trả bằng Ether và được dùng để khuyến khích các thợ đào (miners) xác nhận giao dịch.
*   **Tầm quan trọng:** Phí gas giúp ngăn chặn các cuộc tấn công spam mạng và phân bổ tài nguyên tính toán một cách hiệu quả.