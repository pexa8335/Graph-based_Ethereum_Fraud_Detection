import os
import requests
import networkx as nx
import matplotlib.pyplot as plt
import asyncio
import aiohttp
from dotenv import load_dotenv
from tqdm.asyncio import tqdm
from typing import List, Dict, Any, Optional
import matplotlib.lines as mlines
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math
from datetime import datetime
import pandas as pd
import io
import zipfile

# --- FastAPI Imports ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse

# --- CẤU HÌNH ---
load_dotenv()
FRAUD_API_URL = "http://127.0.0.1:8000/analyze"
ETHERSCAN_API_URL = "https://api.etherscan.io/api"
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

# Khoảng xác suất được coi là "Nghi ngờ"
SUSPICIOUS_LOWER_BOUND = 0.45
SUSPICIOUS_UPPER_BOUND = 0.55

# ⭐ GIỚI HẠN TỶ LỆ: Giới hạn 4 yêu cầu đồng thời đến API dự đoán
SEMAPHORE = asyncio.Semaphore(4)

# --- KHỞI TẠO ỨNG DỤNG FastAPI ---
app = FastAPI(
    title="Ethereum Transaction Graph API",
    description="Một API để phân tích các giao dịch của một địa chỉ ví Ethereum, tạo báo cáo CSV và biểu đồ mạng lưới.",
    version="1.0.0"
)


# --- MÔ HÌNH DỮ LIỆU ĐẦU VÀO (Pydantic) ---
class AnalysisRequest(BaseModel):
    address: str


# --- CÁC HÀM XỬ LÝ (GIỮ NGUYÊN TỪ SCRIPT GỐC) ---
# Các hàm này không thay đổi so với phiên bản trước.

async def get_fraud_prediction(session: aiohttp.ClientSession, address: str) -> Optional[Dict[str, Any]]:
    """Gửi yêu cầu dự đoán đến API cục bộ, được kiểm soát bởi Semaphore."""
    async with SEMAPHORE:
        payload = {"address": address}
        try:
            async with session.post(FRAUD_API_URL, json=payload, timeout=180) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(
                        f"Lỗi khi dự đoán địa chỉ {address[:10]}...: Status {response.status}, Response: {error_text[:150]}")
                    return None
        except asyncio.TimeoutError:
            print(f"Timeout khi dự đoán địa chỉ {address[:10]}...")
            return None
        except Exception as e:
            print(f"Ngoại lệ không xác định khi dự đoán {address[:10]}: {e}")
            return None


def get_transactions(address: str) -> List[Dict[str, Any]]:
    """Lấy danh sách giao dịch từ Etherscan API."""
    print(f"\n🔍 Đang lấy giao dịch cho địa chỉ: {address}")
    params = {
        "module": "account", "action": "txlist", "address": address,
        "startblock": 0, "endblock": 99999999, "sort": "asc", "apikey": ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "1":
            print(f"✅ Tìm thấy {len(data['result'])} giao dịch.")
            return data["result"]
        else:
            print(f"⚠️ Không tìm thấy giao dịch hoặc có lỗi từ API: {data['message']}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi Etherscan API: {e}")
        return []


def export_transactions_to_csv_buffer(transactions: List[Dict[str, Any]],
                                      predictions: Dict[str, Dict[str, Any]]) -> io.StringIO:
    """Xuất các giao dịch ra một bộ đệm CSV trong bộ nhớ."""
    print(f"\n📄 Đang làm giàu dữ liệu và tạo buffer CSV...")
    processed_data = []

    def get_prediction_data(addr):
        if not addr: return 'Contract Creation', 0.0
        pred_result = predictions.get(addr.lower())
        if pred_result:
            return pred_result.get('prediction', 'Unknown'), pred_result.get('probability_fraud', 0.0)
        return 'Unknown', 0.0

    for tx in transactions:
        from_addr = tx.get('from', '')
        to_addr = tx.get('to', '')
        if not from_addr: continue

        from_pred, from_prob = get_prediction_data(from_addr)
        to_pred, to_prob = get_prediction_data(to_addr)
        abnormality_score = from_prob + to_prob
        value_in_eth = int(tx.get('value', 0)) / 1e18
        timestamp = int(tx.get('timeStamp', 0))
        date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        processed_data.append({
            'TxHash': tx.get('hash', ''), 'DateTime': date_time, 'From_Address': from_addr,
            'To_Address': to_addr if to_addr else "Contract Creation", 'Value_ETH': value_in_eth,
            'From_Prediction': from_pred, 'From_Probability': from_prob, 'To_Prediction': to_pred,
            'To_Probability': to_prob, 'Abnormality_Score': abnormality_score
        })

    if not processed_data:
        print("⚠️ Không có giao dịch nào để xuất.")
        return io.StringIO()

    df = pd.DataFrame(processed_data).sort_values(by='Abnormality_Score', ascending=False)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_buffer.seek(0)
    print(f"✅ Đã tạo thành công buffer CSV với {len(df)} giao dịch.")
    return csv_buffer


def get_node_color(prediction_result: Optional[Dict[str, Any]]) -> str:
    if not prediction_result: return 'grey'
    prob = prediction_result.get('probability_fraud', -1.0)
    pred_text = prediction_result.get('prediction', '').lower().strip()
    if SUSPICIOUS_LOWER_BOUND < prob < SUSPICIOUS_UPPER_BOUND: return '#F0E68C'
    if pred_text == 'fraud' or pred_text == 'illicit': return '#990000'
    if pred_text == 'non-fraud' or pred_text == 'licit': return '#000066'
    return 'grey'


def fibonacci_sphere(samples: int):
    points = [];
    phi = math.pi * (math.sqrt(5.) - 1.)
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        radius = math.sqrt(1 - y * y)
        theta = phi * i;
        x = math.cos(theta) * radius;
        z = math.sin(theta) * radius
        points.append((x, y, z))
    return points


def draw_transaction_graph_to_buffer(central_address: str, transactions: List[Dict[str, Any]],
                                     predictions: Dict[str, Dict]) -> Optional[io.BytesIO]:
    """Vẽ biểu đồ hình cầu 3D và lưu nó vào một bộ đệm trong bộ nhớ."""
    print("\n🎨 Đang vẽ biểu đồ hình cầu 3D vào buffer...")
    central_address = central_address.lower()

    G = nx.DiGraph()
    direct_transactions = [tx for tx in transactions if
                           tx.get('from', '').lower() == central_address or tx.get('to', '').lower() == central_address]
    G.add_node(central_address)
    for tx in direct_transactions:
        from_addr = tx.get('from', '').lower();
        to_addr = tx.get('to', '').lower()
        if from_addr and to_addr: G.add_edge(from_addr, to_addr)

    if G.number_of_nodes() <= 1:
        print("Không đủ node để vẽ biểu đồ.");
        return None

    num_nodes = G.number_of_nodes()
    other_nodes = [node for node in G.nodes() if node != central_address]
    nodes_in_order = [central_address] + other_nodes
    pos = {node: fibonacci_sphere(num_nodes)[i] for i, node in enumerate(nodes_in_order)}

    fig = plt.figure(figsize=(15, 15));
    ax = fig.add_subplot(111, projection='3d');
    fig.set_facecolor('white')
    node_colors = [get_node_color(predictions.get(node)) for node in nodes_in_order]
    node_sizes = [500 if node == central_address else 150 for node in nodes_in_order]
    xyz = np.array([pos[v] for v in nodes_in_order])
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c=node_colors, s=node_sizes, edgecolors='black', linewidths=0.5,
               alpha=1.0)

    for edge in G.edges():
        start_pos, end_pos = pos[edge[0]], pos[edge[1]]
        ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], [start_pos[2], end_pos[2]], color='gray',
                alpha=0.5, linewidth=1.2)

    legend_handles = [mlines.Line2D([], [], color=color, marker='o', linestyle='None', markersize=10, label=label)
                      for label, color in {'Gian lận (Illicit)': '#990000', 'An toàn (Licit)': '#000066',
                                           'Nghi ngờ (Suspicious)': '#F0E68C', 'Không xác định': 'grey'}.items()]
    ax.legend(handles=legend_handles, loc='upper right', title='Node Status')
    ax.set_axis_off();
    ax.set_title(f"Transaction Graph of: {central_address}", fontsize=18);
    plt.tight_layout()
    ax.view_init(elev=5, azim=90)

    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    image_buffer.seek(0)
    print("✅ Đã lưu thành công biểu đồ vào buffer.")
    return image_buffer


# --- API ENDPOINT (ĐÃ THAY ĐỔI) ---
@app.post("/graph")
async def create_graph_analysis(request: AnalysisRequest):
    """
    Phân tích một địa chỉ Ethereum: lấy giao dịch, dự đoán gian lận cho các địa chỉ liên quan,
    và trả về một file zip chứa báo cáo CSV và biểu đồ mạng lưới.
    """
    if not ETHERSCAN_API_KEY:
        raise HTTPException(status_code=500,
                            detail="LỖI: Biến môi trường ETHERSCAN_API_KEY chưa được thiết lập trên máy chủ.")

    central_address = request.address.strip()
    if not central_address:
        raise HTTPException(status_code=400, detail="Địa chỉ không được để trống.")

    transactions = get_transactions(central_address)
    if not transactions:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy giao dịch nào cho địa chỉ: {central_address}")

    # Lấy và dự đoán các địa chỉ duy nhất
    unique_addresses = {addr.lower() for tx in transactions for addr in [tx.get('from', ''), tx.get('to', '')] if addr}
    unique_addresses.add(central_address.lower())

    all_addresses_list = list(unique_addresses)
    print(f"\n🔬 Tìm thấy {len(all_addresses_list)} địa chỉ duy nhất. Bắt đầu dự đoán...")

    predictions = {}
    failed_addresses = list(all_addresses_list)
    retry_round = 1

    while failed_addresses:
        if retry_round > 1:
            print(
                f"\n- VÒNG THỬ LẠI {retry_round - 1}: Phát hiện {len(failed_addresses)} địa chỉ bị lỗi. Đang thử lại sau 5s...")
            await asyncio.sleep(5)

        desc = f"Đang dự đoán (vòng {retry_round})"
        async with aiohttp.ClientSession() as session:
            tasks = [get_fraud_prediction(session, addr) for addr in failed_addresses]
            results = await tqdm.gather(*tasks, desc=desc)

        newly_successful_addrs = set()
        for res in results:
            if res and 'address' in res:
                addr = res['address'].lower()
                predictions[addr] = res
                newly_successful_addrs.add(addr)

        failed_addresses = [addr for addr in failed_addresses if addr not in newly_successful_addrs]

        if not failed_addresses:
            break
        retry_round += 1

    print("\n✅ Tất cả các địa chỉ đã được dự đoán thành công!")

    # Tạo file CSV và biểu đồ trong bộ nhớ
    csv_buffer = export_transactions_to_csv_buffer(transactions, predictions)
    image_buffer = draw_transaction_graph_to_buffer(central_address, transactions, predictions)

    # Nén các file trong bộ nhớ vào một file zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("enriched_transactions.csv", csv_buffer.getvalue())
        if image_buffer:
            zf.writestr("transaction_graph.png", image_buffer.getvalue())
    zip_buffer.seek(0)

    # Trả về file zip
    headers = {
        'Content-Disposition': f'attachment; filename="analysis_results_{central_address[:10]}.zip"'
    }
    return StreamingResponse(zip_buffer, media_type="application/x-zip-compressed", headers=headers)


# --- KHỐI ĐỂ CHẠY MÁY CHỦ ---
if __name__ == "__main__":
    import uvicorn

    # Chạy trên port 8001 để tránh xung đột với API dự đoán (port 8000)
    uvicorn.run(app, host="127.0.0.1", port=8001)