# Token ERC20: Tiêu chuẩn cho Token trên Ethereum

## 1. ERC20 là gì?

*   **Định nghĩa:** ERC20 (Ethereum Request for Comment 20) là một tiêu chuẩn kỹ thuật được sử dụng để phát hành và triển khai các token có thể thay thế (fungible tokens) trên blockchain Ethereum. "Fungible" có nghĩa là mỗi đơn vị của token đó có giá trị tương đương và có thể hoán đổi cho nhau (ví dụ: 1 đồng USD luôn có giá trị như 1 đồng USD khác).
*   **Vai trò:** Tiêu chuẩn ERC20 đảm bảo rằng tất cả các token được tạo ra theo nó đều tương thích với nhau và có thể tương tác dễ dàng với các ví điện tử, sàn giao dịch và các hợp đồng thông minh khác trên mạng Ethereum. Điều này thúc đẩy sự phát triển của hệ sinh thái DeFi (Tài chính phi tập trung) và các ứng dụng blockchain.

## 2. Các chức năng cơ bản của Token ERC20

Một token ERC20 phải triển khai một tập hợp các hàm cụ thể, bao gồm:
*   `totalSupply()`: Tổng số lượng token đang lưu hành.
*   `balanceOf(address account)`: Số dư token của một địa chỉ cụ thể.
*   `transfer(address recipient, uint256 amount)`: Chuyển token từ địa chỉ gọi hàm sang một địa chỉ khác.
*   `transferFrom(address sender, address recipient, uint256 amount)`: Chuyển token từ một địa chỉ khác (đã được cấp quyền) sang một địa chỉ mới.
*   `approve(address spender, uint256 amount)`: Cấp quyền cho một địa chỉ khác (spender) được phép chuyển một lượng token nhất định từ tài khoản của bạn.
*   `allowance(address owner, address spender)`: Kiểm tra số lượng token mà một spender được phép chuyển từ tài khoản của owner.

## 3. Giao dịch Token ERC20 (ERC20 Transactions)

*   **Cách thức:** Giao dịch token ERC20 không giống như giao dịch Ether. Khi bạn gửi token ERC20, bạn thực chất đang tương tác với hợp đồng thông minh của token đó (gọi hàm `transfer()` hoặc `transferFrom()`). Giao dịch này vẫn tốn phí gas bằng Ether.
*   **Đặc điểm:** Các giao dịch ERC20 có thể được sử dụng cho nhiều mục đích:
    *   **Đại diện cho tài sản:** Ví dụ: stablecoins (USDT, USDC), token chứng khoán.
    *   **Quản trị:** Quyền biểu quyết trong các dự án phi tập trung (governance tokens).
    *   **Tiện ích:** Truy cập các dịch vụ hoặc tính năng trong một ứng dụng phi tập trung (utility tokens).
    *   **Phần thưởng:** Token được phát hành như phần thưởng cho người dùng.

## 4. Phân biệt với Ether và các tiêu chuẩn Token khác

*   **ERC20 vs. Ether:** Ether là tiền tệ gốc của mạng Ethereum, được sử dụng để thanh toán phí giao dịch và là tài sản chính. ERC20 là một tiêu chuẩn cho các token được xây dựng *trên* mạng Ethereum, chúng không phải là tiền tệ gốc và yêu cầu Ether để thực hiện giao dịch.
*   **ERC20 vs. ERC721 (NFTs):** ERC20 là token có thể thay thế (fungible), mỗi đơn vị đều giống nhau. ERC721 là tiêu chuẩn cho các token không thể thay thế (non-fungible tokens - NFTs), mỗi token là duy nhất và không thể thay thế bằng token khác.