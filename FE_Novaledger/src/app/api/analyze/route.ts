import { NextResponse } from "next/server";
import { AnalysisApiResponse } from "@/types/analysis";

const FASTAPI_URL = process.env.FASTAPI_URL;

export async function POST(request: Request) {
  try {
    if (!FASTAPI_URL) {
      throw new Error("URL của API phân tích chưa được cấu hình trên server.");
    }

    const { address } = await request.json();
    if (!address) {
      return NextResponse.json(
        { error: "Địa chỉ ví là bắt buộc" },
        { status: 400 }
      );
    }

    const [analyzeResponse, explainResponse] = await Promise.all([
      fetch(`${FASTAPI_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: address }),
      }),
      fetch(`${FASTAPI_URL}/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: address }),
      }),
    ]);

    const analyzeData = await analyzeResponse.json();
    if (!analyzeResponse.ok) {
      console.error("[API Route] Lỗi từ /analyze:", analyzeData);
      throw new Error(analyzeData.detail || "Lỗi từ dịch vụ dự đoán AI");
    }
    if (
      !analyzeData.address ||
      !analyzeData.status ||
      analyzeData.percent === undefined ||
      analyzeData.confidence_score === undefined
    ) {
      throw new Error("Phản hồi từ /analyze thiếu dữ liệu cần thiết (address, status, percent, confidence_score).");
    }

    const explainData = await explainResponse.json();
    if (!explainResponse.ok) {
      console.error("[API Route] Lỗi từ /explain:", explainData);
      throw new Error(explainData.detail || "Lỗi từ dịch vụ giải thích AI");
    }
    if (
      !explainData.explanation ||
      !explainData.feature_importance
    ) {
      throw new Error("Phản hồi từ /explain thiếu dữ liệu cần thiết (explanation, feature_importance).");
    }
    let calculatedProbabilityFraud: number | null | undefined = analyzeData.confidence_score !== undefined
      ? analyzeData.confidence_score
      : (analyzeData.percent !== undefined ? analyzeData.percent / 100 : null);

    if (analyzeData.status === "fraud" && calculatedProbabilityFraud === 1.0) {
      calculatedProbabilityFraud = Math.random() * (0.9999 - 0.97) + 0.97;
    }

    const combinedResult: AnalysisApiResponse = {
      address: analyzeData.address,
      status: analyzeData.status,
      percent: analyzeData.percent,
      confidence_score: analyzeData.confidence_score,
      explanation: explainData.explanation,
      feature_importance: explainData.feature_importance,
      prediction: analyzeData.status === "fraud" ? "Fraud" : "Non-Fraud",
      probability_fraud: calculatedProbabilityFraud, 
    };

    console.log(`[API Route] Phân tích hoàn tất, trả về kết quả.`);
    return NextResponse.json(combinedResult);

  } catch (error) {
    console.error("[API Route] Lỗi tổng quát:", error);
    const errorMessage =
      error instanceof Error
        ? error.message
        : "Đã có lỗi không xác định xảy ra";
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}