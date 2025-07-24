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


# --- CÁC HÀM XỬ LÝ ---

async def get_fraud_prediction(session: aiohttp.ClientSession, address: str) -> Optional[Dict[str, Any]]:
    """
    Gửi yêu cầu dự đoán đến API cục bộ, được kiểm soát bởi Semaphore.
    Hàm này sẽ trả về None nếu có lỗi, logic thử lại sẽ được xử lý bên ngoài.
    """
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

# ---- THAY ĐỔI 1: SỬA ĐỔI HOÀN TOÀN HÀM NÀY ----
def export_transactions_to_csv(transactions: List[Dict[str, Any]],
                               predictions: Dict[str, Dict[str, Any]],
                               filename: str):
    """
    Xuất các giao dịch ra file CSV, làm giàu dữ liệu với kết quả dự đoán
    và tính toán một điểm bất thường cho mỗi giao dịch.
    """
    print(f"\n📄 Đang làm giàu dữ liệu và xuất ra file CSV...")

    processed_data = []

    # Hàm trợ giúp để lấy kết quả dự đoán một cách an toàn
    def get_prediction_data(addr):
        if not addr: # Địa chỉ có thể rỗng (ví dụ: tạo hợp đồng)
            return 'Contract Creation', 0.0
        pred_result = predictions.get(addr.lower())
        if pred_result:
            return pred_result.get('prediction', 'Unknown'), pred_result.get('probability_fraud', 0.0)
        return 'Unknown', 0.0 # Trả về giá trị mặc định nếu không tìm thấy dự đoán

    for tx in transactions:
        from_addr = tx.get('from', '')
        to_addr = tx.get('to', '')

        # Bỏ qua nếu không có địa chỉ nguồn (hiếm gặp)
        if not from_addr:
            continue

        from_pred, from_prob = get_prediction_data(from_addr)
        to_pred, to_prob = get_prediction_data(to_addr)

        # Tính điểm bất thường: Tổng xác suất gian lận của hai bên
        abnormality_score = from_prob + to_prob

        value_in_eth = int(tx.get('value', 0)) / 1e18
        timestamp = int(tx.get('timeStamp', 0))
        date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        processed_data.append({
            'TxHash': tx.get('hash', ''),
            'DateTime': date_time,
            'From_Address': from_addr,
            'To_Address': to_addr if to_addr else "Contract Creation",
            'Value_ETH': value_in_eth,
            'From_Prediction': from_pred,
            'From_Probability': from_prob,
            'To_Prediction': to_pred,
            'To_Probability': to_prob,
            'Abnormality_Score': abnormality_score
        })

    if not processed_data:
        print("⚠️ Không có giao dịch nào để xuất ra file.")
        return

    df = pd.DataFrame(processed_data)

    # Sắp xếp theo điểm bất thường giảm dần để các giao dịch đáng ngờ nhất ở trên cùng
    df = df.sort_values(by='Abnormality_Score', ascending=False)

    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Đã xuất thành công {len(df)} giao dịch đã được làm giàu ra file: {filename}")
    except Exception as e:
        print(f"❌ Lỗi khi xuất file CSV: {e}")


def get_node_color(prediction_result: Optional[Dict[str, Any]]) -> str:
    if not prediction_result:
        return 'grey'
    prob = prediction_result.get('probability_fraud', -1.0)
    pred_text = prediction_result.get('prediction', '').lower().strip()
    if SUSPICIOUS_LOWER_BOUND < prob < SUSPICIOUS_UPPER_BOUND:
        return '#F0E68C'
    if pred_text == 'fraud' or pred_text == 'illicit':
        return '#990000'
    if pred_text == 'non-fraud' or pred_text == 'licit':
        return '#000066'
    return 'grey'


def fibonacci_sphere(samples: int):
    points = []
    phi = math.pi * (math.sqrt(5.) - 1.)
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        radius = math.sqrt(1 - y * y)
        theta = phi * i
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        points.append((x, y, z))
    return points


def draw_transaction_graph_matplotlib(central_address: str, transactions: List[Dict[str, Any]],
                                      predictions: Dict[str, Dict]):
    print("\n🎨 Vẽ biểu đồ hình cầu 3D với node trung tâm...")
    central_address = central_address.lower()

    G = nx.DiGraph()
    direct_transactions = [
        tx for tx in transactions
        if tx.get('from', '').lower() == central_address or tx.get('to', '').lower() == central_address
    ]
    G.add_node(central_address)
    for tx in direct_transactions:
        from_addr = tx.get('from', '').lower()
        to_addr = tx.get('to', '').lower()
        if from_addr and to_addr:
            G.add_edge(from_addr, to_addr)

    if G.number_of_nodes() <= 1:
        print("Không đủ node để vẽ biểu đồ hình cầu.")
        return

    num_nodes = G.number_of_nodes()
    other_nodes = [node for node in G.nodes() if node != central_address]
    nodes_in_order = [central_address] + other_nodes
    sphere_coords = fibonacci_sphere(num_nodes)
    pos = {node: sphere_coords[i] for i, node in enumerate(nodes_in_order)}

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    fig.set_facecolor('white')

    node_colors = [get_node_color(predictions.get(node)) for node in nodes_in_order]
    node_sizes = [500 if node == central_address else 150 for node in nodes_in_order]

    xyz = np.array([pos[v] for v in nodes_in_order])
    x_nodes, y_nodes, z_nodes = xyz[:, 0], xyz[:, 1], xyz[:, 2]

    ax.scatter(x_nodes, y_nodes, z_nodes, c=node_colors, s=node_sizes, edgecolors='black', linewidths=0.5, alpha=1.0)

    for edge in G.edges():
        start_pos = pos[edge[0]]
        end_pos = pos[edge[1]]
        ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], [start_pos[2], end_pos[2]], color='gray',
                alpha=0.5, linewidth=1.2)

    legend_elements = {
        'Gian lận (Illicit)': '#990000', 'An toàn (Licit)': '#000066',
        'Nghi ngờ (Suspicious)': '#F0E68C', 'Không xác định': 'grey'
    }
    legend_handles = [mlines.Line2D([], [], color=color, marker='o', linestyle='None',
                                    markersize=10, label=label)
                      for label, color in legend_elements.items()]
    ax.legend(handles=legend_handles, loc='upper right', title='Node Status')

    ax.set_axis_off()
    ax.set_title(f"Transaction Graph of: {central_address}", fontsize=18)
    plt.tight_layout()

    ax.view_init(elev=5, azim=90)
    output_filename = f"graph_2D_view_{central_address}.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\n✅ Biểu đồ đã được lưu với góc nhìn 2D vào file: {output_filename}")

    plt.show()


async def main():
    if not ETHERSCAN_API_KEY:
        print("LỖI: Biến môi trường ETHERSCAN_API_KEY chưa được thiết lập.")
        return

    print("--- Trình phân tích và trực quan hóa mạng lưới giao dịch Ethereum ---")
    central_address = input("Nhập địa chỉ ví Ethereum bạn muốn phân tích: ").strip()
    if not central_address:
        print("Địa chỉ không được để trống.")
        return

    transactions = get_transactions(central_address)
    if not transactions:
        print("Kết thúc chương trình do không có giao dịch để phân tích.")
        return

    # ---- THAY ĐỔI 2: XÓA LỜI GỌI XUẤT CSV Ở ĐÂY ----
    # csv_filename = f"transactions_{central_address[:10]}.csv"
    # export_transactions_to_csv(transactions, central_address, csv_filename)

    unique_addresses = {central_address.lower()}
    for tx in transactions:
        from_addr = tx.get('from', '').lower()
        to_addr = tx.get('to', '').lower()
        if from_addr: unique_addresses.add(from_addr)
        if to_addr: unique_addresses.add(to_addr)

    all_addresses_list = list(unique_addresses)
    print(f"\n🔬 Tìm thấy {len(all_addresses_list)} địa chỉ duy nhất. Bắt đầu dự đoán...")

    predictions = {}

    # 1. Thực hiện lượt dự đoán đầu tiên
    async with aiohttp.ClientSession() as session:
        tasks = [get_fraud_prediction(session, addr) for addr in all_addresses_list]
        results = await tqdm.gather(*tasks, desc="Đang dự đoán (lần đầu)")

    for res in results:
        if res and 'address' in res:
            predictions[res['address'].lower()] = res

    # 2. Xác định các địa chỉ bị lỗi và bắt đầu vòng lặp thử lại
    all_addresses_set = {addr.lower() for addr in all_addresses_list}
    successful_addresses_set = set(predictions.keys())
    failed_addresses = list(all_addresses_set - successful_addresses_set)

    retry_round = 1
    while failed_addresses:
        print(f"\n- VÒNG THỬ LẠI {retry_round}: Phát hiện {len(failed_addresses)} địa chỉ bị lỗi. Đang thử lại...")
        await asyncio.sleep(5)

        async with aiohttp.ClientSession() as retry_session:
            retry_tasks = [get_fraud_prediction(retry_session, addr) for addr in failed_addresses]
            retry_results = await tqdm.gather(*retry_tasks, desc=f"Đang thử lại (vòng {retry_round})")

        for res in retry_results:
            if res and 'address' in res:
                addr = res['address'].lower()
                predictions[addr] = res

        successful_addresses_set = set(predictions.keys())
        failed_addresses = list(all_addresses_set - successful_addresses_set)
        retry_round += 1

    print("\n✅ Tất cả các địa chỉ đã được dự đoán thành công!")

    # ---- THAY ĐỔI 3: GỌI HÀM XUẤT CSV SAU KHI CÓ ĐẦY ĐỦ DỰ ĐOÁN ----
    csv_filename = f"enriched_transactions_{central_address[:10]}.csv"
    export_transactions_to_csv(transactions, predictions, csv_filename)


    draw_transaction_graph_matplotlib(central_address, transactions, predictions)


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())