// src/app/api/analyze/route.ts - PHIÊN BẢN ĐÃ SỬA LỖI TYPES (Gọi song song 2 API)

import { NextResponse } from 'next/server';
import { AnalysisApiResponse } from '@/types/analysis'; 

const FASTAPI_URL = process.env.FASTAPI_URL; 

export async function POST(request: Request) {
  try {
    if (!FASTAPI_URL) {
      throw new Error("URL của API phân tích chưa được cấu hình trên server.");
    }
    const { address } = await request.json();
    if (!address) {
      return NextResponse.json({ error: 'Địa chỉ ví là bắt buộc' }, { status: 400 });
    }

    console.log(`[API Route] Bắt đầu phân tích cho ví: ${address}`);
    const [analyzeResponse, explainResponse] = await Promise.all([
      fetch(`${FASTAPI_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: address }), 
      }),
      fetch(`${FASTAPI_URL}/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: address }), 
      })
    ]);
    const analyzeData = await analyzeResponse.json();
    if (!analyzeResponse.ok) {
      console.error("[API Route] Lỗi từ /analyze:", analyzeData);
      throw new Error(analyzeData.detail || 'Lỗi từ dịch vụ dự đoán AI');
    }

    const explainData = await explainResponse.json();
    if (!explainResponse.ok) {
      console.error("[API Route] Lỗi từ /explain:", explainData);
      throw new Error(explainData.detail || 'Lỗi từ dịch vụ giải thích AI');
    }
    const combinedResult: AnalysisApiResponse = {
      address: analyzeData.address,
      prediction: analyzeData.prediction ?? null, 
      probability_fraud: analyzeData.probability_fraud ?? null, 
      
      features: explainData.features, 
      lime_explanation: explainData.lime_explanation, 
      shap_force_plot_base64: explainData.shap_force_plot_base64, 
      shap_values: explainData.shap_values, 
    };

    console.log(`[API Route] Phân tích hoàn tất, trả về kết quả.`);
    return NextResponse.json(combinedResult);

  } catch (error) {
    console.error('[API Route] Lỗi tổng quát:', error);
    const errorMessage = error instanceof Error ? error.message : 'Đã có lỗi không xác định xảy ra';
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}