import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import joblib
import numpy as np
import pandas as pd
import json
import os

class ImprovedFraudGNN(torch.nn.Module):
    def __init__(self, num_features):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.conv2 = GCNConv(64, 32)
        self.conv3 = GCNConv(32, 16)
        self.classifier = torch.nn.Linear(32, 2)
        self.dropout = torch.nn.Dropout(0.5)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = F.relu(self.conv2(x, edge_index))
        return self.classifier(x)

def load_artifacts(artifacts_dir: str):
    """
    Tải các thành phần của mô hình từ một thư mục được chỉ định.
    Sửa lỗi: Chấp nhận một đối số là đường dẫn thư mục.
    """
    pipeline_path = os.path.join(artifacts_dir, 'preprocessing_pipeline.pkl')
    metadata_path = os.path.join(artifacts_dir, 'metadata.json')
    weights_path = os.path.join(artifacts_dir, 'fraud_gnn_weights.pth')

    if not all(os.path.exists(p) for p in [pipeline_path, metadata_path, weights_path]):
        raise FileNotFoundError(f"Một hoặc nhiều file mô hình không được tìm thấy trong thư mục: {artifacts_dir}. Vui lòng kiểm tra lại đường dẫn.")

    pipeline = joblib.load(pipeline_path)
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    final_features_list = metadata['features']['final_features_list']
    num_features = len(final_features_list)

    model = ImprovedFraudGNN(num_features)
    model.load_state_dict(torch.load(weights_path, map_location='cpu'))
    model.eval()

    # Trả về cả danh sách các đặc trưng mong muốn để tái sử dụng
    return model, pipeline, final_features_list

def predict_address(model, pipeline, features_dict: dict, expected_columns: list):
    """
    Dự đoán một địa chỉ.
    Tối ưu: Nhận 'expected_columns' trực tiếp thay vì đọc lại file metadata mỗi lần gọi.
    """
    df = pd.DataFrame([features_dict])

    # Sắp xếp lại và điền các cột bị thiếu để khớp với đầu vào của mô hình
    missing_cols = set(expected_columns) - set(df.columns)
    for col in missing_cols:
        df[col] = 0.0
    df = df[expected_columns]

    x_proc = pipeline.transform(df)
    x_tensor = torch.tensor(x_proc, dtype=torch.float32)
    edge_index = torch.tensor([], dtype=torch.long).reshape(2, 0)

    with torch.no_grad():
        logits = model(x_tensor, edge_index)
        probs = torch.softmax(logits, dim=1)[0]
        pred_index = int(torch.argmax(probs))
        confidence_percent = float(probs[pred_index]) * 100

    status = "fraud" if pred_index == 1 else "non-fraud"
    return status, (confidence_percent / 100), confidence_percent

def explain_address(model, pipeline, features_dict, feat_names, topk=None):  # Thêm topk optional để khớp với app.py, nhưng bỏ qua nó
    # Tương tự, thêm reorder cho hàm này để tránh lỗi nếu gọi
    with open('../Model/metadata.json', 'r') as f:
        metadata = json.load(f)
    expected_columns = metadata['features']['final_features_list']  # Giữ key như attachment

    df = pd.DataFrame([features_dict])

    # Debug: In để kiểm tra trước reorder
    print("🔍 Explain features columns before reorder:", df.columns.tolist())

    # Reorder và fill default
    missing_cols = set(expected_columns) - set(df.columns)
    for col in missing_cols:
        df[col] = 0.0
    df = df[expected_columns]

    # Debug: In sau reorder
    print("✅ Explain features columns after reorder:", df.columns.tolist())

    x_proc = pipeline.transform(df)
    x_tensor = torch.tensor(x_proc, dtype=torch.float32)
    importance = model.conv1.lin.weight.abs().sum(dim=0).detach().numpy()
    feat_names_aligned = feat_names if len(feat_names) == len(importance) else [f"f{i}" for i in range(len(importance))]

    # Sắp xếp tất cả features theo importance giảm dần (bỏ qua topk)
    idx = importance.argsort()[::-1]  # Từ cao đến thấp
    all_features = np.array(feat_names_aligned)[idx]
    all_importance = importance[idx].round(3)

    # Convert numpy.float32 sang float để serialize JSON
    feature_importance = {feat: float(value) for feat, value in zip(all_features, all_importance)}

    return {
        "explanation": "Giải thích importance của tất cả các đặc trưng (sắp xếp từ ảnh hưởng cao nhất đến thấp nhất)",
        "feature_importance": feature_importance
    }
