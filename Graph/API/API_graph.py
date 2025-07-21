import os
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from pyvis.network import Network
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

# --- CẤU HÌNH ---
load_dotenv()

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Trình phân tích mạng lưới giao dịch Ethereum",
    description="Sử dụng endpoint /graph và cung cấp một địa chỉ ví để tạo biểu đồ mạng lưới giao dịch tương tác.",
    version="1.2.0"  # Đã cập nhật phiên bản
)

# URL API dự đoán (đang chạy cục bộ)
FRAUD_API_URL = "http://127.0.0.1:8000/analyze"

# URL và API Key của Etherscan
ETHERSCAN_API_URL = "https://api.etherscan.io/api"
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

# Ngưỡng xác suất để phân loại màu sắc
PROB_FRAUD_THRESHOLD = 0.6
PROB_SUSPICIOUS_THRESHOLD = 0.4


# --- CÁC HÀM XỬ LÝ (Không thay đổi) ---

async def get_fraud_prediction(session: aiohttp.ClientSession, address: str) -> Optional[Dict[str, Any]]:
    """Gọi API dự đoán cục bộ một cách bất đồng bộ để lấy kết quả phân tích."""
    payload = {"address": address}
    try:
        async with session.post(FRAUD_API_URL, json=payload, timeout=120) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Lỗi khi dự đoán địa chỉ {address[:10]}...: Status {response.status}")
                return None
    except Exception as e:
        print(f"Không thể kết nối đến API dự đoán cho địa chỉ {address[:10]}...: {e}")
        return None


async def get_transactions(session: aiohttp.ClientSession, address: str) -> List[Dict[str, Any]]:
    """
    Lấy danh sách các giao dịch từ Etherscan API một cách bất đồng bộ.
    Phiên bản này được điều chỉnh để có logic giống hệt với tệp graph.py đang hoạt động.
    """
    print(f"🔍 Đang lấy giao dịch cho địa chỉ: {address}")
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        async with session.get(ETHERSCAN_API_URL, params=params) as response:
            # Kiểm tra nếu request không thành công (vd: 500 server error)
            response.raise_for_status()
            data = await response.json()

            # Logic xử lý response giống hệt graph.py
            if data.get("status") == "1":
                print(f"✅ Tìm thấy {len(data['result'])} giao dịch.")
                return data["result"]
            else:
                # In ra thông báo lỗi từ Etherscan để dễ dàng debug
                print(f"⚠️ Không tìm thấy giao dịch hoặc có lỗi từ API: {data.get('message', 'Unknown Error')}")
                return []
    except aiohttp.ClientError as e:
        # Bắt lỗi cụ thể của aiohttp
        print(f"Lỗi khi gọi Etherscan API: {e}")
        raise HTTPException(status_code=503, detail=f"Không thể lấy dữ liệu từ Etherscan: {e}")
    except Exception as e:
        # Bắt các lỗi chung khác
        print(f"Lỗi không xác định trong get_transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi server không xác định: {e}")


def get_node_color(probability_fraud: float) -> str:
    """Xác định màu của node dựa trên xác suất gian lận."""
    if probability_fraud > PROB_FRAUD_THRESHOLD:
        return 'red'
    elif probability_fraud > PROB_SUSPICIOUS_THRESHOLD:
        return 'orange'
    elif probability_fraud >= 0:
        return 'green'
    else:
        return 'grey'


# --- HÀM VẼ BIỂU ĐỒ ĐÃ ĐƯỢC CẬP NHẬT HOÀN TOÀN ---
# Logic giờ đây giống hệt với tệp graph.py đang hoạt động của bạn.

def draw_transaction_graph_to_html(central_address: str, transactions: List[Dict[str, Any]],
                                   predictions: Dict[str, Dict]) -> str:
    """
    Vẽ biểu đồ mạng lưới bằng PyVis và trả về chuỗi HTML của biểu đồ.
    Logic được sao chép từ phiên bản hoạt động trong graph.py.
    """
    print("\n🎨 Bắt đầu tạo mã HTML cho biểu đồ PyVis...")
    net = Network(height="95vh", width="100%", bgcolor="#222222", font_color="white", directed=True)

    unique_addresses = {addr.lower() for tx in transactions for addr in [tx.get('from'), tx.get('to')] if addr}
    unique_addresses.add(central_address.lower())

    for address in unique_addresses:
        prediction = predictions.get(address, {})
        prob = prediction.get('probability_fraud', -1)
        color = get_node_color(prob)
        status_from_model = prediction.get('prediction', 'Unknown')
        short_label = f"{address[:6]}...{address[-4:]}"
        etherscan_url = f"https://etherscan.io/address/{address}"

        # Quyết định chuỗi hiển thị cho xác suất TRƯỚC KHI đưa vào f-string lớn.
        prob_display_string = f"{prob:.2%}" if prob >= 0 else "N/A"

        title_html = (
            f"<b>Address:</b> {address}<br>"
            f"<b>Model Status:</b> <b style='color: {color};'>{status_from_model.capitalize()}</b><br>"
            f"<b>Fraud Probability:</b> {prob_display_string}<br><br>"
            f"<a href='{etherscan_url}' target='_blank' style='color: #87CEEB;'>Click to view on Etherscan</a>"
        )
        node_size = 25 if address == central_address.lower() else 15
        net.add_node(address, label=short_label, size=node_size, color=color, title=title_html)

    for tx in transactions:
        from_addr = tx.get('from', '').lower()
        to_addr = tx.get('to', '').lower()
        if not from_addr or not to_addr: continue
        try:
            value_eth = int(tx.get('value', 0)) / 1e18
            edge_title = f"Value: {value_eth:.6f} ETH"
            net.add_edge(source=from_addr, to=to_addr, title=edge_title, value=value_eth * 0.1 + 1)
        except (ValueError, TypeError):
            net.add_edge(source=from_addr, to=to_addr, title="Invalid value")

    # --- SỬA LỖI CHÍNH TẠI ĐÂY ---
    # Khôi phục chuỗi options gốc từ tệp graph.py bao gồm cả "const options ="
    # Đây là nguyên nhân chính gây ra sự khác biệt.
    net.set_options("""
    const options = {
      "nodes": {
        "font": {
          "size": 12,
          "face": "Tahoma"
        }
      },
      "edges": {
        "color": {"inherit": "from"},
        "smooth": {
          "type": "dynamic",
          "forceDirection": "none",
          "roundness": 0.5
        },
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 1.4
          }
        },
        "arrowStrikethrough": false
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 230,
          "springConstant": 0.08,
          "avoidOverlap": 0.5
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "tooltipDelay": 200
      }
    }
    """)
    # --- KẾT THÚC PHẦN SỬA LỖI ---

    html_content = net.generate_html()
    print("✅ Đã tạo xong mã HTML.")
    return html_content


# --- ENDPOINT CỦA API (Không thay đổi) ---

@app.get("/graph", response_class=HTMLResponse)
async def analyze_address_and_get_graph(
        address: str = Query(..., title="Địa chỉ ví Ethereum",
                             description="Địa chỉ ví cần phân tích, ví dụ: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
                             regex="^0x[a-fA-F0-9]{40}$")
):
    """
    Phân tích một địa chỉ ví Ethereum và trả về một biểu đồ mạng lưới giao dịch tương tác.

    Cung cấp địa chỉ ví dưới dạng một query parameter `?address=...`
    """
    if not ETHERSCAN_API_KEY:
        raise HTTPException(status_code=500,
                            detail="LỖI: Biến môi trường ETHERSCAN_API_KEY chưa được thiết lập trên server.")

    central_address = address.lower().strip()

    async with aiohttp.ClientSession() as session:
        transactions = await get_transactions(session, central_address)
        if not transactions:
            return HTMLResponse(content=f"<h3>Không tìm thấy giao dịch nào cho địa chỉ: {central_address}</h3>",
                                status_code=404)

        unique_addresses = {addr.lower() for tx in transactions for addr in [tx.get('from'), tx.get('to')] if addr}
        unique_addresses.add(central_address)
        print(f"\n🔬 Tìm thấy {len(unique_addresses)} địa chỉ duy nhất. Bắt đầu dự đoán...")

        predictions = {}
        prediction_tasks = [get_fraud_prediction(session, addr) for addr in unique_addresses]
        results = await asyncio.gather(*prediction_tasks)

        for res in results:
            if res and 'address' in res:
                predictions[res['address'].lower()] = res

        html_graph = draw_transaction_graph_to_html(central_address, transactions, predictions)
        return HTMLResponse(content=html_graph)