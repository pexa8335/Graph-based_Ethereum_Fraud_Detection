import json
import os

# Danh sách các cột chính xác từ input của bạn
model_columns = [
    'Index', 'Avg min between sent tnx', 'Avg min between received tnx',
    'Time Diff between first and last (Mins)', 'Sent tnx', 'Received Tnx',
    'Number of Created Contracts', 'Unique Received From Addresses',
    'Unique Sent To Addresses', 'min value received', 'max value received',
    'avg val received', 'min val sent', 'max val sent', 'avg val sent',
    'min value sent to contract', 'max val sent to contract',
    'avg value sent to contract',
    'total transactions (including tnx to create contract', # Chú ý lỗi typo
    'total Ether sent', 'total ether received',
    'total ether sent contracts', 'total ether balance', 'Total ERC20 tnxs',
    'ERC20 total Ether received', 'ERC20 total ether sent',
    'ERC20 total Ether sent contract', 'ERC20 uniq sent addr',
    'ERC20 uniq rec addr', 'ERC20 uniq sent addr.1',
    'ERC20 uniq rec contract addr', 'ERC20 avg time between sent tnx',
    'ERC20 avg time between rec tnx', 'ERC20 avg time between rec 2 tnx',
    'ERC20 avg time between contract tnx', 'ERC20 min val rec',
    'ERC20 max val rec', 'ERC20 avg val rec', 'ERC20 min val sent',
    'ERC20 max val sent', 'ERC20 avg val sent',
    'ERC20 min val sent contract', 'ERC20 max val sent contract',
    'ERC20 avg val sent contract', 'ERC20 uniq sent token name',
    'ERC20 uniq rec token name', 'ERC20 most sent token type_label',
    'ERC20_most_rec_token_type_label'
]

# Tạo thư mục Model nếu chưa tồn tại
if not os.path.exists('Model'):
    os.makedirs('Model')

# Lưu vào file JSON
file_path = 'Model/model_columns.json'
with open(file_path, 'w') as f:
    json.dump(model_columns, f, indent=4)

print(f"Đã tạo file '{file_path}' thành công với {len(model_columns)} cột.")
