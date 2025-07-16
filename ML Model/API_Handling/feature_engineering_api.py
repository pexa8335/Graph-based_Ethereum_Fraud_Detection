# feature_engineering_api.py (Phiên bản đầy đủ - Đã sửa lỗi)

import asyncio
import os
import httpx
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import Counter
import statistics
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# --- Cấu hình ---
COVALENT_API_KEY = os.environ.get('COVALENT_API_KEY')
CHAIN_NAME = 'eth-mainnet'
MAX_PAGES_TO_FETCH = 50

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if COVALENT_API_KEY:
    logging.info("Đã tải Covalent API Key.")
else:
    logging.warning("COVALENT_API_KEY không được thiết lập.")

HEADERS = {
    "Authorization": f"Bearer {COVALENT_API_KEY}",
}

# --- Các hàm gọi API ---
async def fetch_all_transactions(address: str, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    """Lấy tất cả giao dịch, xử lý phân trang và lỗi timeout."""
    all_items: List[Dict[str, Any]] = []
    page_number = 0
    has_more = True

    while has_more and page_number < MAX_PAGES_TO_FETCH:
        url = f"https://api.covalenthq.com/v1/{CHAIN_NAME}/address/{address}/transactions_v3/?page-number={page_number}"
        try:
            res = await client.get(url, headers=HEADERS)
            res.raise_for_status()
            data = res.json().get("data", {})
            
            if items := data.get("items"):
                all_items.extend(items)
                has_more = data.get("pagination", {}).get("has_more", False)
            else:
                has_more = False
            
            page_number += 1
            await asyncio.sleep(0.2)
        except httpx.TimeoutException:
            logging.error(f"Lỗi Timeout khi lấy giao dịch trên trang {page_number} cho địa chỉ {address}.")
            has_more = False
        except httpx.HTTPStatusError as e:
            error_data = e.response.json()
            logging.error(f"Lỗi Covalent API trên trang {page_number}: {error_data.get('error_message', e.request.url)}")
            has_more = False
        except Exception as e:
            logging.error(f"Lỗi không mong muốn khi lấy giao dịch trên trang {page_number}: {type(e).__name__} - {e}")
            has_more = False
    return all_items

async def fetch_balance(address: str, client: httpx.AsyncClient) -> Dict[str, Any]:
    """Lấy số dư token, xử lý lỗi timeout."""
    url = f"https://api.covalenthq.com/v1/{CHAIN_NAME}/address/{address}/balances_v2/"
    try:
        res = await client.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.json().get("data", {"items": []})
    except httpx.TimeoutException:
        logging.error(f"Lỗi Timeout khi lấy số dư cho địa chỉ {address}.")
    except httpx.HTTPStatusError as e:
        error_data = e.response.json()
        logging.error(f"Lỗi API khi lấy số dư: {error_data.get('error_message', e.request.url)}")
    except Exception as e:
        logging.error(f"Lỗi không mong muốn khi lấy số dư: {type(e).__name__} - {e}")
    return {"items": []}


# --- Logic tính toán ---
def calculate_all_features(address: str, all_txs: List[Dict[str, Any]], balance_data: Dict[str, Any]) -> Dict[str, Any]:
    addr = address.lower()
    features: Dict[str, Any] = {}

    def to_ether(wei: Optional[str]) -> float:
        return float(int(wei)) / 1e18 if wei else 0.0

    def get_stats(arr: List[float]) -> Dict[str, float]:
        if not arr:
            return {"min": 0.0, "max": 0.0, "avg": 0.0}
        return {"min": min(arr), "max": max(arr), "avg": statistics.mean(arr)}

    def get_time_diffs(txs: List[Dict[str, Any]]) -> List[float]:
        if len(txs) < 2:
            return []
        ts = sorted([datetime.fromisoformat(tx['block_signed_at'].replace('Z', '+00:00')) for tx in txs])
        return [(ts[i+1] - ts[i]).total_seconds() / 60 for i in range(len(ts) - 1)]

    def get_avg(arr: List[float]) -> float:
        return statistics.mean(arr) if arr else 0.0

    def get_most_common(arr: List[Optional[str]]) -> Optional[str]:
        clean_arr = [item for item in arr if item]
        if not clean_arr:
            return None
        return Counter(clean_arr).most_common(1)[0][0]

    sent_txs = [tx for tx in all_txs if tx['from_address'].lower() == addr]
    received_txs = [tx for tx in all_txs if tx.get('to_address') and tx['to_address'].lower() == addr]
    contract_creation_txs = [tx for tx in sent_txs if tx['to_address'] is None]
    sent_to_contract_txs = [tx for tx in sent_txs if tx.get('to_address_is_contract')]

    token_transfers = []
    for tx in all_txs:
        for log in tx.get('log_events', []):
            decoded = log.get('decoded')
            if decoded and decoded.get('name') == "Transfer" and decoded.get('params'):
                params = {p['name']: p for p in decoded['params']}
                from_addr = params.get('from', {}).get('value')
                to_addr = params.get('to', {}).get('value')
                value = params.get('value', {}).get('value')
                
                if from_addr and to_addr:
                    token_transfers.append({
                        "block_signed_at": log['block_signed_at'],
                        "from_address": from_addr,
                        "to_address": to_addr,
                        "to_address_is_contract": params.get('to', {}).get('is_contract'),
                        "token_symbol": log.get('sender_contract_ticker_symbol'),
                        "value_quote": float(value) if value is not None else 0.0
                    })

    sent_tokens = [t for t in token_transfers if t['from_address'].lower() == addr]
    received_tokens = [t for t in token_transfers if t['to_address'].lower() == addr]
    sent_tokens_to_contract = [t for t in sent_tokens if t.get('to_address_is_contract')]
    
    all_timestamps_dt = [datetime.fromisoformat(tx['block_signed_at'].replace('Z', '+00:00')) for tx in all_txs]
    first_tx_time = min(all_timestamps_dt) if all_timestamps_dt else None
    last_tx_time = max(all_timestamps_dt) if all_timestamps_dt else None

    # Các cột này sẽ bị xóa ở cuối, nhưng cần được tạo ra để tham chiếu
    features['Index'] = 0
    features['Address'] = address
    
    # Các đặc trưng chính
    features['Avg min between sent tnx'] = get_avg(get_time_diffs(sent_txs))
    features['Avg min between received tnx'] = get_avg(get_time_diffs(received_txs))
    features['Time Diff between first and last (Mins)'] = (last_tx_time - first_tx_time).total_seconds() / 60 if first_tx_time and last_tx_time else 0
    features['Sent tnx'] = len(sent_txs)
    features['Received Tnx'] = len(received_txs)
    features['Number of Created Contracts'] = len(contract_creation_txs)
    features['Unique Received From Addresses'] = len(set(tx['from_address'] for tx in received_txs))
    features['Unique Sent To Addresses'] = len(set(tx['to_address'] for tx in sent_txs if tx['to_address']))

    sent_values = [to_ether(tx['value']) for tx in sent_txs]
    rec_values = [to_ether(tx['value']) for tx in received_txs]
    sent_contract_values = [to_ether(tx['value']) for tx in sent_to_contract_txs]

    sent_stats = get_stats(sent_values)
    rec_stats = get_stats(rec_values)
    sent_contract_stats = get_stats(sent_contract_values)

    features['min value received'] = rec_stats['min']
    features['max value received'] = rec_stats['max']
    features['avg val received'] = rec_stats['avg']
    features['min val sent'] = sent_stats['min']
    features['max val sent'] = sent_stats['max']
    features['avg val sent'] = sent_stats['avg']
    features['min value sent to contract'] = sent_contract_stats['min']
    features['max val sent to contract'] = sent_contract_stats['max']
    features['avg value sent to contract'] = sent_contract_stats['avg']
    
    # Chú ý: Giữ nguyên lỗi typo để khớp với model đã huấn luyện
    features['total transactions (including tnx to create contract'] = len(all_txs)
    features['total Ether sent'] = sum(sent_values)
    features['total ether received'] = sum(rec_values)
    features['total ether sent contracts'] = sum(sent_contract_values)

    eth_token = next((token for token in balance_data.get('items', []) if token.get('native_token')), None)
    features['total ether balance'] = (float(eth_token['balance']) / (10 ** eth_token['contract_decimals'])) if eth_token else 0.0

    features['Total ERC20 tnxs'] = len(token_transfers)
    features['ERC20 total Ether received'] = sum(t['value_quote'] for t in received_tokens)
    features['ERC20 total ether sent'] = sum(t['value_quote'] for t in sent_tokens)
    features['ERC20 total Ether sent contract'] = sum(t['value_quote'] for t in sent_tokens_to_contract)
    
    # --- PHẦN SỬA LỖI QUAN TRỌNG ---
    # Tạo tất cả các cột cần thiết, bao gồm cả các cột "bẩn" từ dữ liệu training
    
    # Cặp 1: Uniq Sent Addr
    features['ERC20 uniq sent addr'] = len(set(t['to_address'] for t in sent_tokens))
    features['ERC20 uniq sent addr.1'] = features['ERC20 uniq sent addr'] # Tạo bản sao

    features['ERC20 uniq rec addr'] = len(set(t['from_address'] for t in received_tokens))
    features['ERC20 uniq rec contract addr'] = len(set(t['from_address'] for t in received_tokens if t.get('to_address_is_contract')))

    # Cặp 2: Avg Time
    features['ERC20 avg time between sent tnx'] = get_avg(get_time_diffs(sent_tokens))
    features['ERC20 avg time between rec tnx'] = get_avg(get_time_diffs(received_tokens))
    features['ERC20 avg time between rec 2 tnx'] = features['ERC20 avg time between rec tnx'] # Tạo bản sao
    
    features['ERC20 avg time between contract tnx'] = get_avg(get_time_diffs(sent_tokens_to_contract))
    # --- KẾT THÚC PHẦN SỬA LỖI ---

    erc20_sent_stats = get_stats([t['value_quote'] for t in sent_tokens])
    erc20_rec_stats = get_stats([t['value_quote'] for t in received_tokens])
    erc20_sent_contract_stats = get_stats([t['value_quote'] for t in sent_tokens_to_contract])

    features['ERC20 min val rec'] = erc20_rec_stats['min']
    features['ERC20 max val rec'] = erc20_rec_stats['max']
    features['ERC20 avg val rec'] = erc20_rec_stats['avg']
    features['ERC20 min val sent'] = erc20_sent_stats['min']
    features['ERC20 max val sent'] = erc20_sent_stats['max']
    features['ERC20 avg val sent'] = erc20_sent_stats['avg']
    features['ERC20 min val sent contract'] = erc20_sent_contract_stats['min']
    features['ERC20 max val sent contract'] = erc20_sent_contract_stats['max']
    features['ERC20 avg val sent contract'] = erc20_sent_contract_stats['avg']
    
    features['ERC20 uniq sent token name'] = len(set(t['token_symbol'] for t in sent_tokens if t['token_symbol']))
    features['ERC20 uniq rec token name'] = len(set(t['token_symbol'] for t in received_tokens if t['token_symbol']))
    
    # Các cột này sẽ được dùng để tạo label hoặc bị xóa đi
    features['ERC20 most sent token type'] = get_most_common([t.get('token_symbol') for t in sent_tokens])
    features['ERC20_most_rec_token_type'] = get_most_common([t.get('token_symbol') for t in received_tokens])
    
    # Loại bỏ các cột không cần thiết cho mô hình trước khi trả về
    columns_to_remove = [
        'Index', 
        'Address', 
        'ERC20 most sent token type', 
        'ERC20_most_rec_token_type'
    ]
    
    for col in columns_to_remove:
        features.pop(col, None) # Sử dụng pop để tránh lỗi nếu key không tồn tại

    return features


# --- Hàm chính để điều phối ---
async def analyze_wallet_address(address: str) -> Optional[Dict[str, Any]]:
    if not COVALENT_API_KEY:
        logging.error("Không thể phân tích: COVALENT_API_KEY chưa được đặt.")
        return None
        
    logging.info(f"Bắt đầu phân tích địa chỉ: {address}")
    
    timeout = httpx.Timeout(30.0, connect=60.0)
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            tasks = [
                fetch_all_transactions(address, client),
                fetch_balance(address, client)
            ]
            all_txs, balance_data = await asyncio.gather(*tasks)

        if not all_txs and not balance_data.get('items'):
             logging.warning(f"Không tìm thấy dữ liệu giao dịch hoặc số dư cho {address}.")
             return None

        features = calculate_all_features(address, all_txs, balance_data)
        logging.info(f"Phân tích hoàn tất cho {address}")
        return features

    except Exception as e:
        logging.error(f"Lỗi nghiêm trọng trong quá trình phân tích ví {address}: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        return None