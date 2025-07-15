# Hướng dẫn chi tiết các đặc trưng (Features) trong Bộ dữ liệu Giao dịch Ethereum

Bộ dữ liệu này cung cấp các đặc trưng tổng hợp ở cấp độ địa chỉ ví, được sử dụng để phát hiện giao dịch bất thường. Hiểu rõ ý nghĩa của từng đặc trưng là chìa khóa để phân tích và giải thích các dự đoán của mô hình.

## 1. Các trường nhận diện và mục tiêu

*   **Index:** Mã định danh duy nhất cho mỗi bản ghi/địa chỉ ví. (Không phải là đặc trưng dùng để huấn luyện mô hình, chỉ để nhận diện).
*   **Address:** Địa chỉ ví Ethereum thực tế. (Không phải là đặc trưng dùng để huấn luyện mô hình, chỉ để nhận diện).
*   **FLAG:** Biến mục tiêu.
    *   `0`: Giao dịch/Địa chỉ được phân loại là **hợp lệ (normal)**.
    *   `1`: Giao dịch/Địa chỉ được phân loại là **bất thường (illicit/anomaly)**.

## 2. Các đặc trưng liên quan đến thời gian và tần suất giao dịch

*   **Avg min between sent tnx:** Thời gian trung bình (tính bằng phút) giữa các giao dịch gửi đi liên tiếp từ địa chỉ ví.
    *   *Ý nghĩa:* Cho biết tần suất các giao dịch gửi đi. Giá trị thấp có thể gợi ý hoạt động cao bất thường (ví dụ: bot, spam).
*   **Avg min between received tnx:** Thời gian trung bình (tính bằng phút) giữa các giao dịch nhận vào liên tiếp của địa chỉ ví.
    *   *Ý nghĩa:* Cho biết tần suất các giao dịch nhận vào.
*   **Time Diff between first and last (Mins):** Khoảng thời gian (tính bằng phút) giữa giao dịch đầu tiên và giao dịch cuối cùng của địa chỉ ví.
    *   *Ý nghĩa:* Tổng thời gian hoạt động của địa chỉ. Địa chỉ bất thường có thể có thời gian hoạt động rất ngắn (ví dụ: giao dịch chớp nhoáng) hoặc rất dài (ví dụ: ví rửa tiền lâu năm).

## 3. Các đặc trưng về số lượng giao dịch và tương tác

*   **Sent tnx:** Tổng số giao dịch gửi đi từ địa chỉ ví.
*   **Received Tnx:** Tổng số giao dịch nhận vào của địa chỉ ví.
*   **Number of Created Contracts:** Số lượng hợp đồng thông minh được tạo bởi địa chỉ ví.
    *   *Ý nghĩa:* Địa chỉ tạo nhiều hợp đồng có thể là nhà phát triển, nhưng cũng có thể là kẻ lừa đảo tạo ra các hợp đồng độc hại.
*   **Unique Received From Addresses:** Số lượng địa chỉ duy nhất đã gửi Ether đến địa chỉ ví này.
*   **Unique Sent To Addresses:** Số lượng địa chỉ duy nhất mà địa chỉ ví này đã gửi Ether đến.
    *   *Ý nghĩa:* Số lượng địa chỉ tương tác có thể chỉ ra hoạt động mạng lưới của ví. Ví rửa tiền có thể tương tác với rất nhiều địa chỉ duy nhất.
*   **total transactions (including tnx to create contract):** Tổng số giao dịch (bao gồm cả giao dịch tạo hợp đồng).

## 4. Các đặc trưng về giá trị Ether

*   **min value received:** Giá trị Ether tối thiểu nhận được trong một giao dịch.
*   **max value received:** Giá trị Ether tối đa nhận được trong một giao dịch.
*   **avg val received:** Giá trị Ether trung bình nhận được trong một giao dịch.
*   **min val sent:** Giá trị Ether tối thiểu gửi đi trong một giao dịch.
*   **max val sent:** Giá trị Ether tối đa gửi đi trong một giao dịch.
*   **avg val sent:** Giá trị Ether trung bình gửi đi trong một giao dịch.
*   **min value sent to contract:** Giá trị Ether tối thiểu gửi đến một hợp đồng thông minh.
*   **max val sent to contract:** Giá trị Ether tối đa gửi đến một hợp đồng thông minh.
*   **avg value sent to contract:** Giá trị Ether trung bình gửi đến một hợp đồng thông minh.
    *   *Ý nghĩa các trường giá trị:* Các giá trị min/max/avg có thể chỉ ra các mẫu giao dịch bất thường (ví dụ: nhiều giao dịch nhỏ để rửa tiền, hoặc một giao dịch rất lớn từ một vụ hack).
*   **total Ether sent:** Tổng lượng Ether đã gửi đi.
*   **total ether received:** Tổng lượng Ether đã nhận vào.
*   **total ether sent contracts:** Tổng lượng Ether đã gửi đến các hợp đồng thông minh.
*   **total ether balance:** Số dư Ether cuối cùng của địa chỉ ví (tổng nhận - tổng gửi).
    *   *Ý nghĩa:* Số dư âm có thể chỉ ra ví đã gửi nhiều hơn nhận, thường là ví chuyển tiền đi hoặc ví trung gian.

## 5. Các đặc trưng liên quan đến Token ERC20

*   **Total ERC20 tnxs:** Tổng số giao dịch token ERC20.
*   **ERC20 total Ether received:** Tổng giá trị Ether của các token ERC20 đã nhận (lưu ý: đây thường là giá trị token, không phải Ether).
*   **ERC20 total ether sent:** Tổng giá trị Ether của các token ERC20 đã gửi (lưu ý: đây thường là giá trị token, không phải Ether).
*   **ERC20 total Ether sent contract:** Tổng giá trị Ether của các token ERC20 đã gửi đến hợp đồng thông minh.
*   **ERC20 uniq sent addr:** Số lượng địa chỉ duy nhất đã gửi token ERC20.
*   **ERC20 uniq rec addr:** Số lượng địa chỉ duy nhất đã nhận token ERC20.
*   **ERC20 uniq sent addr.1:** Có thể là một trường trùng lặp hoặc lỗi đánh máy của "ERC20 uniq sent addr". Cần kiểm tra dữ liệu thực tế để xác nhận.
*   **ERC20 uniq rec contract addr:** Số lượng địa chỉ hợp đồng duy nhất đã nhận token ERC20.
*   **ERC20 avg time between sent tnx:** Thời gian trung bình (phút) giữa các giao dịch gửi token ERC20.
*   **ERC20 avg time between rec tnx:** Thời gian trung bình (phút) giữa các giao dịch nhận token ERC20.
*   **ERC20 avg time between rec 2 tnx:** Thời gian trung bình (phút) giữa hai giao dịch nhận token ERC20 liên tiếp.
*   **ERC20 avg time between contract tnx:** Thời gian trung bình (phút) giữa các giao dịch token ERC20 liên quan đến hợp đồng.
*   **ERC20 min val rec:** Giá trị token ERC20 tối thiểu nhận được.
*   **ERC20 max val rec:** Giá trị token ERC20 tối đa nhận được.
*   **ERC20 avg val rec:** Giá trị token ERC20 trung bình nhận được.
*   **ERC20 min val sent:** Giá trị token ERC20 tối thiểu gửi đi.
*   **ERC20 max val sent:** Giá trị token ERC20 tối đa gửi đi.
*   **ERC20 avg val sent:** Giá trị token ERC20 trung bình gửi đi.
*   **ERC20 min val sent contract:** Giá trị token ERC20 tối thiểu gửi đến hợp đồng.
*   **ERC20 max val sent contract:** Giá trị token ERC20 tối đa gửi đến hợp đồng.
*   **ERC20 avg val sent contract:** Giá trị token ERC20 trung bình gửi đến hợp đồng.
    *   *Ý nghĩa các trường ERC20:* Các đặc trưng này rất quan trọng vì nhiều hoạt động bất hợp pháp (ví dụ: lừa đảo, rug pulls) thường liên quan đến các token ERC20. Các giá trị min/max/avg, số lượng địa chỉ duy nhất tương tác, và tần suất giao dịch token có thể là chỉ báo mạnh mẽ.
*   **ERC20 uniq sent token name:** Số lượng tên token ERC20 duy nhất đã gửi.
*   **ERC20 uniq rec token name:** Số lượng tên token ERC20 duy nhất đã nhận.
    *   *Ý nghĩa:* Số lượng token đa dạng có thể chỉ ra hoạt động phức tạp.
*   **ERC20 most sent token type_label / ERC20 most sent token type:** Loại token ERC20 được gửi nhiều nhất (có thể là tên token hoặc ID phân loại).
*   **ERC20_most_rec_token_type_label / ERC20_most_rec_token_type:** Loại token ERC20 được nhận nhiều nhất (có thể là tên token hoặc ID phân loại).
    *   *Ý nghĩa:* Loại token phổ biến nhất có thể liên quan đến các chiến dịch lừa đảo hoặc các hoạt động cụ thể.

## 6. Các đặc trưng đồ thị (Graph Features - Giả định nếu có)

Nếu có các đặc trưng đồ thị được tính toán từ NetworkX và thêm vào bộ dữ liệu, chúng sẽ bao gồm:
*   **PageRank Score:** Chỉ số ảnh hưởng của địa chỉ trong mạng lưới giao dịch. Địa chỉ có PageRank cao có thể là trung tâm của một mạng lưới lớn.
*   **Betweenness Centrality:** Mức độ một địa chỉ nằm trên các con đường ngắn nhất giữa các cặp địa chỉ khác. Địa chỉ có Betweenness Centrality cao thường là cầu nối quan trọng.
*   **Clustering Coefficient:** Mức độ các hàng xóm của một địa chỉ cũng là hàng xóm của nhau. Giá trị thấp có thể gợi ý các giao dịch phân tán.
*   **Community ID:** ID của cộng đồng (cluster) mà địa chỉ thuộc về, được phát hiện bởi các thuật toán phân cụm đồ thị.