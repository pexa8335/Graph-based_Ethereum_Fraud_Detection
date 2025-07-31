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
FRAUD_API_URL = "https://fraudgraphml-2nz2.onrender.com/analyze"
ETHERSCAN_API_URL = "https://api.etherscan.io/api"
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

SUSPICIOUS_LOWER_BOUND = 0.45
SUSPICIOUS_UPPER_BOUND = 0.55
SEMAPHORE = asyncio.Semaphore(1)

# --- KHỞI TẠO ỨNG DỤNG FastAPI ---
app = FastAPI(
    title="Ethereum Transaction Graph API",
    description="Một API để phân tích các giao dịch của một địa chỉ ví Ethereum, tạo báo cáo CSV và biểu đồ mạng lưới.",
    version="1.0.0"
)


# --- MÔ HÌNH DỮ LIỆU ĐẦU VÀO (Pydantic) ---
class AnalysisRequest(BaseModel):
    address: str


# --- CÁC HÀM XỬ LÝ ---
async def get_fraud_prediction(session: aiohttp.ClientSession, address: str) -> Optional[Dict[str, Any]]:
    """Gửi yêu cầu dự đoán đến API cục bộ, được kiểm soát bởi Semaphore."""
    async with SEMAPHORE:
        await asyncio.sleep(1.5)
        payload = {"address": address}
        try:
            async with session.post(FRAUD_API_URL, json=payload, timeout=300) as response:
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
                                      predictions: Dict[str, Dict[str, Any]],
                                      central_address: str) -> io.StringIO:
    """
    Làm giàu dữ liệu giao dịch với thông tin chi tiết, dự đoán và các trường phân tích,
    sau đó xuất ra một buffer CSV trong bộ nhớ.
    """
    print(f"\n📄 Đang làm giàu dữ liệu và tạo buffer CSV chi tiết...")
    processed_data = []
    central_address_lower = central_address.lower()

    def get_prediction_data(addr):
        if not addr:
            return 'Contract Creation', 0.0
        pred_result = predictions.get(addr.lower())
        if pred_result:
            return pred_result.get('prediction', 'Unknown'), pred_result.get('probability_fraud', 0.0)
        return 'Not Predicted', 0.0

    for tx in transactions:
        from_addr = tx.get('from', '').lower()
        to_addr = tx.get('to', '').lower()

        if not from_addr:
            continue

        from_pred, from_prob = get_prediction_data(from_addr)
        to_pred, to_prob = get_prediction_data(to_addr)

        # Cải thiện điểm rủi ro
        transaction_risk_score = from_prob + to_prob

        # Chuyển đổi giá trị và thời gian
        value_in_eth = int(tx.get('value', 0)) / 1e18
        timestamp = int(tx.get('timeStamp', 0))
        date_time_utc = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # --- CÁC CỘT MỚI ĐƯỢC THÊM VÀO ---
        gas_used = int(tx.get('gasUsed', 0))
        gas_price_wei = int(tx.get('gasPrice', 0))
        transaction_fee_eth = (gas_used * gas_price_wei) / 1e18
        gas_price_gwei = gas_price_wei / 1e9

        # Xác định chiều giao dịch
        if from_addr == central_address_lower:
            direction = 'Outgoing'
        elif to_addr == central_address_lower:
            direction = 'Incoming'
        else:
            direction = 'Indirect'  # Giao dịch giữa 2 địa chỉ khác trong list

        transaction_status = 'Success' if tx.get('isError') == '0' else 'Failed'
        is_contract_creation = True if not to_addr else False
        etherscan_url = f"https://etherscan.io/tx/{tx.get('hash', '')}"

        processed_data.append({
            'transaction_hash': tx.get('hash', ''),
            'timestamp_utc': date_time_utc,
            'block_number': tx.get('blockNumber', ''),
            'direction': direction,
            'from_address': from_addr,
            'to_address': to_addr if to_addr else "Contract Creation",
            'value_eth': value_in_eth,
            # 'value_usd_at_time': Cần API giá lịch sử để thêm cột này
            'transaction_fee_eth': round(transaction_fee_eth, 12),
            'transaction_status': transaction_status,
            'gas_price_gwei': round(gas_price_gwei, 2),
            'gas_used': gas_used,
            'is_contract_creation': is_contract_creation,
            'from_address_prediction': from_pred,
            'from_address_fraud_probability': from_prob,
            'to_address_prediction': to_pred,
            'to_address_fraud_probability': to_prob,
            'transaction_risk_score': transaction_risk_score,
            'etherscan_url': etherscan_url
        })

    if not processed_data:
        print("⚠️ Không có giao dịch nào để xuất.")
        return io.StringIO()

    # Sắp xếp theo điểm rủi ro giảm dần
    df = pd.DataFrame(processed_data)
    df = df.sort_values(by='transaction_risk_score', ascending=False)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_buffer.seek(0)
    print(f"✅ Đã tạo thành công buffer CSV chi tiết với {len(df)} hàng và {len(df.columns)} cột.")
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
        y = 1 - (i / float(samples - 1)) * 2;
        radius = math.sqrt(1 - y * y)
        theta = phi * i;
        x = math.cos(theta) * radius;
        z = math.sin(theta) * radius
        points.append((x, y, z))
    return points


def draw_transaction_graph_to_buffer(central_address: str, transactions: List[Dict[str, Any]],
                                     predictions: Dict[str, Dict]) -> Optional[io.BytesIO]:
    print("\n🎨 Đang vẽ biểu đồ hình cầu 3D vào buffer...")
    central_address = central_address.lower()
    G = nx.DiGraph()
    direct_transactions = [tx for tx in transactions if
                           tx.get('from', '').lower() == central_address or tx.get('to', '').lower() == central_address]
    G.add_node(central_address)
    for tx in direct_transactions:
        from_addr, to_addr = tx.get('from', '').lower(), tx.get('to', '').lower()
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
    ax.legend(handles=legend_handles, loc='upper right', title='Node Status');
    ax.set_axis_off();
    ax.set_title(f"Transaction Graph of: {central_address}", fontsize=18);
    plt.tight_layout();
    ax.view_init(elev=5, azim=90)
    image_buffer = io.BytesIO();
    plt.savefig(image_buffer, format='png', dpi=300, bbox_inches='tight');
    plt.close(fig);
    image_buffer.seek(0)
    print("✅ Đã lưu thành công biểu đồ vào buffer.")
    return image_buffer


# --- API ENDPOINT ---
@app.post("/graph")
async def create_graph_analysis(request: AnalysisRequest):
    if not ETHERSCAN_API_KEY:
        raise HTTPException(status_code=500,
                            detail="LỖI: Biến môi trường ETHERSCAN_API_KEY chưa được thiết lập trên máy chủ.")
    central_address = request.address.strip()
    if not central_address:
        raise HTTPException(status_code=400, detail="Địa chỉ không được để trống.")
    transactions = get_transactions(central_address)
    if not transactions:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy giao dịch nào cho địa chỉ: {central_address}")

    unique_addresses = {addr.lower() for tx in transactions for addr in [tx.get('from', ''), tx.get('to', '')] if addr}
    unique_addresses.add(central_address.lower())

    all_addresses_list = list(unique_addresses)
    print(f"\n🔬 Tìm thấy {len(all_addresses_list)} địa chỉ duy nhất. Bắt đầu dự đoán...")

    predictions = {}
    addresses_to_retry = list(all_addresses_list)

    # ⭐ THAY ĐỔI: Thêm logic đếm lỗi cho từng địa chỉ
    failure_counts = {addr: 0 for addr in all_addresses_list}
    MAX_INDIVIDUAL_RETRIES = 7  # Giới hạn số lần thử lại cho MỖI địa chỉ

    retry_round = 1
    base_retry_delay = 5

    while addresses_to_retry:
        if retry_round > 1:
            retry_delay = base_retry_delay * (retry_round - 1)
            print(
                f"\n- VÒNG THỬ LẠI {retry_round - 1}: Phát hiện {len(addresses_to_retry)} địa chỉ bị lỗi. Đang thử lại sau {retry_delay}s...")
            await asyncio.sleep(retry_delay)

        desc = f"Đang dự đoán (vòng {retry_round})"
        async with aiohttp.ClientSession() as session:
            tasks = [get_fraud_prediction(session, addr) for addr in addresses_to_retry]
            results = await tqdm.gather(*tasks, desc=desc)

        successful_addrs_this_round = set()
        for res in results:
            if res and 'address' in res:
                addr = res['address'].lower()
                predictions[addr] = res
                successful_addrs_this_round.add(addr)

        current_failures = [addr for addr in addresses_to_retry if addr not in successful_addrs_this_round]

        # ⭐ THAY ĐỔI: Loại bỏ những địa chỉ đã thất bại quá nhiều lần
        next_round_addresses = []
        for addr in current_failures:
            failure_counts[addr] += 1
            if failure_counts[addr] < MAX_INDIVIDUAL_RETRIES:
                next_round_addresses.append(addr)
            else:
                print(f"⚠️ Đã từ bỏ địa chỉ {addr[:10]}... sau {failure_counts[addr]} lần thử thất bại.")

        addresses_to_retry = next_round_addresses

        if not addresses_to_retry:
            break
        retry_round += 1

    if any(count >= MAX_INDIVIDUAL_RETRIES for count in failure_counts.values()):
        print(f"\n⚠️ CẢNH BÁO: Một số địa chỉ không thể dự đoán được sau {MAX_INDIVIDUAL_RETRIES} lần thử.")

    print("\n✅ Dự đoán hoàn tất!")

    csv_buffer = export_transactions_to_csv_buffer(transactions, predictions, central_address)
    image_buffer = draw_transaction_graph_to_buffer(central_address, transactions, predictions)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("enriched_transactions.csv", csv_buffer.getvalue())
        if image_buffer:
            zf.writestr("transaction_graph.png", image_buffer.getvalue())
    zip_buffer.seek(0)

    headers = {'Content-Disposition': f'attachment; filename="analysis_results_{central_address[:10]}.zip"'}
    return StreamingResponse(zip_buffer, media_type="application/x-zip-compressed", headers=headers)


# --- KHỐI ĐỂ CHẠY MÁY CHỦ ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)