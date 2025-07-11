# ML Model/API_Handling/main_api.py (Phiên bản cuối cùng - Đã sửa lỗi dấu cách)

import os
import asyncio
import joblib
import json
import pandas as pd
import numpy as np
import shap
import lime
from lime.lime_tabular import LimeTabularExplainer
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import hàm từ file cùng thư mục
from feature_engineering_api import analyze_wallet_address

# --- Cấu hình đường dẫn ---
API_HANDLING_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(API_HANDLING_DIR, '..', 'Model')

# --- Cấu hình ứng dụng FastAPI ---
app = FastAPI(
    title="Fraud Detection API (Random Forest)",
    description="API để phân tích địa chỉ ví Ethereum, dự đoán và giải thích.",
    version="1.4.0",
)

# --- Các biến toàn cục ---
model = None
model_columns = None
encoders = None 
explainer_shap = None
explainer_lime = None

# --- Pydantic Models ---
class WalletRequest(BaseModel):
    address: str = Field(..., example="0x83b23b86551Ac259345915d3A395183344e80387")

class AnalyzeResponse(BaseModel):
    address: str
    prediction: str
    probability_fraud: float
    features: dict
# <<< THÊM CLASS MỚI NÀY >>>
class SimpleAnalyzeResponse(BaseModel):
    address: str
    prediction: str
    probability_fraud: float

class ExplainResponse(BaseModel):
    address: str
    features: dict
    lime_explanation: list
    shap_force_plot_base64: str
    shap_values: Dict[str, float]


# --- Sự kiện Startup ---
@app.on_event("startup")
async def startup_event():
    global model, model_columns, encoders, explainer_shap, explainer_lime
    
    print("--- Tải model và các tài nguyên cần thiết ---")
    
    model_path = os.path.join(MODEL_DIR, "trained_model.pkl")
    encoders_path = os.path.join(MODEL_DIR, "label_encoders.pkl")
    columns_path = os.path.join(MODEL_DIR, "model_columns.json")
    
    print(f"Đang tải model từ: {model_path}")
    model = joblib.load(model_path)
    print(f"Đang tải encoders từ: {encoders_path}")
    encoders = joblib.load(encoders_path)
    print(f"Đang tải columns từ: {columns_path}")
    with open(columns_path, 'r') as f:
        model_columns = json.load(f)
        
    print(f"Model '{type(model).__name__}', {len(encoders)} encoders, và {len(model_columns)} cột đã được tải.")

    explainer_shap = shap.TreeExplainer(model)
    X_train_sample_for_lime = pd.DataFrame(np.zeros((100, len(model_columns))), columns=model_columns).values
    explainer_lime = LimeTabularExplainer(
        training_data=X_train_sample_for_lime,
        feature_names=model_columns,
        class_names=[str(c) for c in model.classes_],
        mode='classification'
    )
    print("--- Sẵn sàng nhận request ---")

# --- Các hàm xử lý và endpoints ---
def handle_unknown_token(encoder, token_value):
    """An toàn chuyển đổi token thành label, xử lý token chưa từng thấy."""
    # Chuyển đổi giá trị đầu vào thành chuỗi để đảm bảo tính nhất quán
    token_str = str(token_value) if token_value is not None else 'None'
    try:
        # LabelEncoder cần một array-like input
        return encoder.transform([token_str])[0]
    except ValueError:
        # Token này không có trong "sổ tay" (encoder)
        # Trả về -1 để biểu thị "không xác định" hoặc "khác"
        return -1

# main_api.py - phiên bản cuối cùng, tự xử lý dấu cách

# main_api.py - phiên bản cuối cùng, sạch sẽ

async def process_wallet(address: str) -> pd.DataFrame:
    # 1. Lấy dữ liệu thô với tên cột chuẩn (không có dấu cách)
    features_dict = await analyze_wallet_address(address)
    if not features_dict:
        raise HTTPException(status_code=404, detail=f"Không thể lấy dữ liệu cho địa chỉ: {address}")

    # 2. Xử lý các cột categorical
    sent_token_type = features_dict.get('ERC20 most sent token type')
    rec_token_type = features_dict.get('ERC20_most_rec_token_type')
    
    # Lấy encoder bằng key chuẩn (không có dấu cách)
    le_sent = encoders['ERC20 most sent token type']
    le_rec = encoders['ERC20_most_rec_token_type']
    
    # Tạo các cột label mới với tên chuẩn
    features_dict['ERC20 most sent token type_label'] = handle_unknown_token(le_sent, sent_token_type)
    features_dict['ERC20_most_rec_token_type_label'] = handle_unknown_token(le_rec, rec_token_type)

    # 3. Tạo DataFrame và chuẩn hóa
    input_df = pd.DataFrame([features_dict])
    
    # reindex sẽ hoạt động hoàn hảo vì mọi thứ đều chuẩn
    final_df = input_df.reindex(columns=model_columns, fill_value=0)
    
    return final_df


@app.post("/analyze", response_model=SimpleAnalyzeResponse)
async def analyze(request: WalletRequest):
    try:
        input_df = await process_wallet(request.address)
        prediction_val = model.predict(input_df)[0]
        prediction_label = "Fraud" if prediction_val == 1 else "Non-Fraud"
        probabilities = model.predict_proba(input_df)[0]
        return {
            "address": request.address,
            "prediction": prediction_label,
            "probability_fraud": float(probabilities[1])
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain", response_model=ExplainResponse)
async def explain(request: WalletRequest):
    try:
        input_df = await process_wallet(request.address)
        # 2. LIME explanation
        lime_explanation = explainer_lime.explain_instance(
            data_row=input_df.iloc[0].values,
            predict_fn=lambda x: model.predict_proba(pd.DataFrame(x, columns=model_columns)),
            num_features=10,
            labels=(1,)
        )

        # 3. SHAP explanation (trả về giá trị thay vì vẽ ảnh)
        shap_values = explainer_shap.shap_values(input_df)

        if isinstance(shap_values, list) and len(shap_values) > 1:
            shap_used = shap_values[1]
        elif isinstance(shap_values, list):
            shap_used = shap_values[0]
        else:
            shap_used = shap_values

        shap_row = shap_used[0]
        if isinstance(shap_row, np.ndarray):
            shap_row = shap_row.flatten().tolist()
        shap_result = dict(zip(model_columns, map(float, shap_row)))



        # 4. Trả kết quả
        return {
            "address": request.address,
            "features": input_df.iloc[0].to_dict(),
            "lime_explanation": lime_explanation.as_list(label=1),
            "shap_force_plot_base64": "",  # bỏ ảnh
            "shap_values": shap_result     # thêm shap theo cột
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    import uvicorn
    if not os.getenv("COVALENT_API_KEY"):
        print("CẢNH BÁO: Biến môi trường COVALENT_API_KEY chưa được thiết lập.")
    uvicorn.run(app, host="0.0.0.0", port=8000)