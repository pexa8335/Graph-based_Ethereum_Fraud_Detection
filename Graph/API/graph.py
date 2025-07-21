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

# --- CẤU HÌNH ---
load_dotenv()

# URL API của bạn (đang chạy cục bộ)
FRAUD_API_URL = "http://127.0.0.1:8000/analyze"

# URL và API Key của Etherscan
ETHERSCAN_API_URL = "https://api.etherscan.io/api"
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

# Ngưỡng xác suất để phân loại màu sắc
PROB_FRAUD_THRESHOLD = 0.6
PROB_SUSPICIOUS_THRESHOLD = 0.4


# --- CÁC HÀM XỬ LÝ ---

async def get_fraud_prediction(session: aiohttp.ClientSession, address: str) -> Optional[Dict[str, Any]]:
    """Gọi API dự đoán cục bộ một cách bất đồng bộ để lấy kết quả phân tích."""
    payload = {"address": address}
    try:
        async with session.post(FRAUD_API_URL, json=payload, timeout=120) as response:
            if response.status == 200:
                return await response.json()
            else:
                if response.status != 500:
                    print(f"Lỗi khi dự đoán địa chỉ {address[:10]}...: Status {response.status}")
                return None
    except Exception:
        return None


def get_transactions(address: str) -> List[Dict[str, Any]]:
    """Lấy danh sách các giao dịch từ Etherscan API."""
    print(f"\n🔍 Đang lấy giao dịch cho địa chỉ: {address}")
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


def get_node_color(probability_fraud: float) -> str:
    """Xác định màu của node dựa trên xác suất gian lận."""
    if probability_fraud > PROB_FRAUD_THRESHOLD:
        return '#990000'
    elif probability_fraud > PROB_SUSPICIOUS_THRESHOLD:
        return '#F0E68C'
    elif probability_fraud >= 0:
        return '#000066'
    else:
        return 'grey'


def draw_transaction_graph_matplotlib(central_address: str, transactions: List[Dict[str, Any]],
                                      predictions: Dict[str, Dict]):
    """
    Vẽ biểu đồ đã loại bỏ viền của ô trung tâm.
    """
    print("\n🎨 Vẽ biểu đồ hoàn thiện...")
    central_address = central_address.lower()

    direct_transactions = [
        tx for tx in transactions
        if tx.get('from', '').lower() == central_address or tx.get('to', '').lower() == central_address
    ]

    G = nx.DiGraph()
    G.add_node(central_address)
    for tx in direct_transactions:
        from_addr = tx.get('from', '').lower()
        to_addr = tx.get('to', '').lower()
        if from_addr and to_addr:
            G.add_edge(from_addr, to_addr)

    if G.number_of_nodes() <= 1:
        print("Không đủ node liên quan trực tiếp để vẽ biểu đồ.")
        return

    shells = [[central_address], [node for node in G.nodes() if node != central_address]]
    pos = nx.shell_layout(G, nlist=shells)

    node_colors = [get_node_color(predictions.get(node, {}).get('probability_fraud', -1)) for node in G.nodes()]
    node_sizes = [3000 if node == central_address else 1800 for node in G.nodes()]

    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(13, 13))
    fig.set_facecolor('white')

    # ⭐ THAY ĐỔI 1: VẼ NODE KHÔNG CÓ THÔNG SỐ VIỀN
    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors,
                           node_size=node_sizes,
                           ax=ax)

    nx.draw_networkx_edges(G, pos,
                           arrows=True,
                           arrowstyle='->',
                           arrowsize=20,
                           edge_color='gray',
                           width=2,
                           ax=ax,
                           node_size=node_sizes)

    y_offset = 0.1
    pos_labels = {k: (v[0], v[1] - y_offset) for k, v in pos.items()}
    labels = {node: f"{node[:6]}...{node[-4:]}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos_labels, labels,
                            font_size=9,
                            font_color='black',
                            ax=ax)

    # ⭐ THAY ĐỔI 2: TẠO CHÚ THÍCH MÀ KHÔNG CÓ MỤC "ĐỊA CHỈ TRUNG TÂM"
    legend_elements = {
        'Gian lận (Illicit)': '#990000',
        'An toàn (Licit)': '#000066',
        'Nghi ngờ (Suspicious)': '#F0E68C',
        'Không xác định': 'grey'
    }
    legend_handles = [mlines.Line2D([], [], color=color, marker='o', linestyle='None',
                                    markersize=10, label=label)
                      for label, color in legend_elements.items()]

    ax.legend(handles=legend_handles, loc='upper right', title='Node Status', fontsize='medium', title_fontsize='large')

    ax.set_title(f"Transaction Flow Graph of Address: {central_address}", fontsize=18, color='black')

    ax.axis('off')
    ax.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()


async def main():
    """Hàm chính điều phối toàn bộ quy trình."""
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

    unique_addresses = {central_address.lower()}
    for tx in transactions:
        from_addr = tx.get('from', '').lower()
        to_addr = tx.get('to', '').lower()
        if from_addr: unique_addresses.add(from_addr)
        if to_addr: unique_addresses.add(to_addr)

    print(f"\n🔬 Tìm thấy {len(unique_addresses)} địa chỉ duy nhất. Bắt đầu dự đoán...")

    predictions = {}
    async with aiohttp.ClientSession() as session:
        tasks = [get_fraud_prediction(session, addr) for addr in unique_addresses]
        results = await tqdm.gather(*tasks, desc="Đang dự đoán")

    for res in results:
        if res and 'address' in res:
            predictions[res['address'].lower()] = res

    draw_transaction_graph_matplotlib(central_address, transactions, predictions)


if __name__ == "__main__":
    asyncio.run(main())