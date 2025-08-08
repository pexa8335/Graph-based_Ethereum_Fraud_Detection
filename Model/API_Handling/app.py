import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import load_artifacts, predict_address, explain_address
from feature_engineering_api import analyze_wallet_address

app = FastAPI()

model, pipeline, feat_names = load_artifacts()

class AddressRequest(BaseModel):
    address: str

@app.post("/analyze")
async def analyze(req: AddressRequest):
    features = await analyze_wallet_address(req.address)
    if features is None:
        raise HTTPException(status_code=404, detail=f"Không lấy được dữ liệu cho địa chỉ {req.address}")
    status, confidence, percent = predict_address(model, pipeline, features)
    return {
        "status": status,
        "percent": round(percent, 2),
        "address": req.address,
        "confidence_score": confidence
    }

@app.post("/explain")
async def explain(req: AddressRequest):
    features = await analyze_wallet_address(req.address)
    if features is None:
        raise HTTPException(status_code=404, detail=f"Không lấy được dữ liệu cho địa chỉ {req.address}")
    explanation = explain_address(model, pipeline, features, feat_names, topk=5)
    explanation["address"] = req.address
    return explanation
