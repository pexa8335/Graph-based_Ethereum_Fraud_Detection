# ML Model/API_Handling/main_api.py (Phiên bản đã sửa lỗi thứ tự cột)
import os
import asyncio
import joblib
import pandas as pd
import numpy as np
import shap
from lime.lime_tabular import LimeTabularExplainer
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import các file cần thiết
from feature_engineering_api import analyze_wallet_address
from ml_transformers import ColumnDropper, ControlCharacterCleaner, IntelligentImputer

# --- Cấu hình đường dẫn ---
API_HANDLING_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(API_HANDLING_DIR, '..', 'Model')
PIPELINE_PATH = os.path.join(MODEL_DIR, "full_pipeline.pkl") 

# --- Cấu hình ứng dụng FastAPI ---
app = FastAPI(
    title="Fraud Detection API (XGBoost Pipeline)",
    description="API để phân tích địa chỉ ví Ethereum, dự đoán và giải thích.",
    version="2.1.0", # Nâng cấp phiên bản
)

# --- Các biến toàn cục ---
pipeline = None
explainer_shap = None
explainer_lime = None
# <<< THÊM BIẾN NÀY ĐỂ LƯU THỨ TỰ CỘT CHUẨN >>>
MODEL_FEATURE_ORDER = None

# --- Pydantic Models ---
class WalletRequest(BaseModel):
    address: str = Field(..., example="0x83b23b86551Ac259345915d3A395183344e80387")

class SimpleAnalyzeResponse(BaseModel):
    address: str
    prediction: str
    probability_fraud: float

class ExplainResponse(BaseModel):
    address: str
    lime_explanation: List[List]
    shap_values: Dict[str, float]

# --- Sự kiện Startup ---
@app.on_event("startup")
async def startup_event():
    global pipeline, explainer_shap, explainer_lime, MODEL_FEATURE_ORDER
    
    print("--- Tải pipeline và các tài nguyên cần thiết ---")
    
    if not os.path.exists(PIPELINE_PATH):
        raise FileNotFoundError(f"Không tìm thấy file pipeline tại: {PIPELINE_PATH}.")

    print(f"Đang tải pipeline từ: {PIPELINE_PATH}")
    pipeline = joblib.load(PIPELINE_PATH)
    print(f"Pipeline '{type(pipeline).__name__}' đã được tải.")

    model_from_pipeline = pipeline.named_steps['classifier']
    
    # <<< THAY ĐỔI 1: LẤY VÀ LƯU LẠI THỨ TỰ CỘT CHUẨN TỪ MODEL >>>
    # Đây là thứ tự mà XGBoost đã học và yêu cầu
    MODEL_FEATURE_ORDER = pipeline.named_steps['classifier'].feature_names_in_.tolist()
    print(f"Đã tải {len(MODEL_FEATURE_ORDER)} tên đặc trưng theo đúng thứ tự.")

    print("Khởi tạo SHAP Explainer...")
    explainer_shap = shap.TreeExplainer(model_from_pipeline)
    
    print("Khởi tạo LIME Explainer...")
    X_train_sample_for_lime = np.zeros((100, len(MODEL_FEATURE_ORDER)))
    
    explainer_lime = LimeTabularExplainer(
        training_data=X_train_sample_for_lime,
        feature_names=MODEL_FEATURE_ORDER, # Sử dụng thứ tự chuẩn
        class_names=[str(c) for c in model_from_pipeline.classes_],
        mode='classification'
    )
    print("--- Sẵn sàng nhận request ---")

async def get_and_prepare_dataframe(address: str) -> pd.DataFrame:
    """
    Hàm trợ giúp: Lấy dữ liệu, tạo DataFrame và SẮP XẾP LẠI CỘT cho đúng.
    """
    features_dict = await analyze_wallet_address(address)
    if not features_dict:
        raise HTTPException(status_code=404, detail=f"Không thể lấy dữ liệu cho địa chỉ: {address}")
    
    input_df = pd.DataFrame([features_dict])
    
    # <<< THAY ĐỔI 2: DÒNG CODE QUAN TRỌNG NHẤT >>>
    # Sắp xếp lại các cột của DataFrame mới theo đúng thứ tự mà model mong đợi.
    # Thao tác này sẽ giải quyết lỗi "feature_names mismatch".
    return input_df.reindex(columns=MODEL_FEATURE_ORDER)


@app.post("/analyze", response_model=SimpleAnalyzeResponse)
async def analyze(request: WalletRequest):
    """
    Nhận địa chỉ ví, chạy qua pipeline và trả về dự đoán.
    """
    try:
        # 1. Lấy và chuẩn bị DataFrame với thứ tự cột chính xác
        ordered_df = await get_and_prepare_dataframe(request.address)
        
        # 2. Dự đoán bằng TOÀN BỘ pipeline
        prediction_val = pipeline.predict(ordered_df)[0]
        probabilities = pipeline.predict_proba(ordered_df)[0]
        
        prediction_label = "Fraud" if prediction_val == 1 else "Non-Fraud"
        
        return {
            "address": request.address,
            "prediction": prediction_label,
            "probability_fraud": float(probabilities[1])
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Trả về thông báo lỗi cụ thể hơn từ exception
        raise HTTPException(status_code=500, detail=f"Lỗi trong quá trình phân tích: {e}")


@app.post("/explain", response_model=ExplainResponse)
async def explain(request: WalletRequest):
    """
    Giải thích dự đoán bằng LIME và SHAP.
    """
    try:
        # 1. Lấy và chuẩn bị DataFrame với thứ tự cột chính xác
        ordered_df = await get_and_prepare_dataframe(request.address)

        # 2. Lấy dữ liệu đã được xử lý bởi pipeline (trừ bước classifier)
        processed_df = pipeline[:-1].transform(ordered_df)

        # 3. Giải thích LIME
        lime_explanation = explainer_lime.explain_instance(
            data_row=processed_df.iloc[0].values,
            predict_fn=lambda x: pipeline.predict_proba(pd.DataFrame(x, columns=MODEL_FEATURE_ORDER)),
            num_features=10,
            labels=(1,)
        )

        # 4. Giải thích SHAP
        shap_values = explainer_shap.shap_values(processed_df)
        shap_row = shap_values[0]
        if isinstance(shap_row, np.ndarray):
            shap_row = shap_row.flatten().tolist()
        shap_result = dict(zip(MODEL_FEATURE_ORDER, map(float, shap_row)))

        # 5. Trả kết quả
        return {
            "address": request.address,
            "lime_explanation": lime_explanation.as_list(label=1),
            "shap_values": shap_result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi trong quá trình giải thích: {e}")


if __name__ == "__main__":
    import uvicorn
    if not os.getenv("COVALENT_API_KEY"):
        print("CẢNH BÁO: Biến môi trường COVALENT_API_KEY chưa được thiết lập.")
    uvicorn.run(app, host="0.0.0.0", port=8000)