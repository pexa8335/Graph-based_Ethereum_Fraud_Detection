# FILE: app.py (PHIÊN BẢN ĐÃ SỬA LỖI TypeError VÀ CẬP NHẬT CÁC LỆNH GỌI HÀM)

import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import load_artifacts, predict_address, explain_address
from feature_engineering_api import analyze_wallet_address

app = FastAPI(
    title="Ethereum Address Analysis API (Simple)",
    description="Một API đơn giản để phân tích và giải thích dự đoán cho một địa chỉ ví Ethereum.",
    version="1.2.0"  # Cập nhật phiên bản
)

# Chỉ định đường dẫn và gọi hàm load_artifacts đúng cách
MODEL_ARTIFACTS_DIR = '../Model/'
model, pipeline, feat_names = load_artifacts(MODEL_ARTIFACTS_DIR)
print("✅ Tải mô hình và pipeline cho app.py thành công.")


class AddressRequest(BaseModel):
    address: str


@app.post("/analyze")
async def analyze(req: AddressRequest):
    """Phân tích một địa chỉ và trả về dự đoán gian lận."""
    features = await analyze_wallet_address(req.address)
    if features is None:
        raise HTTPException(status_code=404, detail=f"Không lấy được dữ liệu cho địa chỉ {req.address}")

    # <<< THAY ĐỔI QUAN TRỌNG: Thêm `feat_names` vào lệnh gọi hàm >>>
    status, confidence, percent = predict_address(model, pipeline, features, feat_names)

    return {
        "status": status,
        "percent": round(percent, 2),
        "address": req.address,
        "confidence_score": round(confidence, 4)
    }


@app.post("/explain")
async def explain(req: AddressRequest):
    """Giải thích các đặc trưng quan trọng nhất cho dự đoán của một địa chỉ."""
    features = await analyze_wallet_address(req.address)
    if features is None:
        raise HTTPException(status_code=404, detail=f"Không lấy được dữ liệu cho địa chỉ {req.address}")

    # <<< THAY ĐỔI QUAN TRỌNG: Cập nhật lệnh gọi hàm explain_address, bỏ tham số `topk` không còn dùng >>>
    explanation = explain_address(model, pipeline, features, feat_names)

    explanation["address"] = req.address
    return explanation


if __name__ == "__main__":
    import uvicorn

    # Lệnh để chạy ứng dụng này: uvicorn app:app --reload --port 8000
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)