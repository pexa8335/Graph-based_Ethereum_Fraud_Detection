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

    console.log(`[API Route] Bắt đầu phân tích cho ví: ${address}`);

    // 3. Thực hiện 2 cuộc gọi song song đến FastAPI
    const [analyzeResponse, explainResponse] = await Promise.all([
      // Gọi endpoint /analyze để lấy dự đoán và xác suất
      fetch(`${FASTAPI_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: address }),
      }),
      // Gọi endpoint /explain để lấy giải thích LIME và SHAP
      fetch(`${FASTAPI_URL}/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address: address }),
      }),
    ]);

    // 4. Xử lý kết quả từ cuộc gọi /analyze
    const analyzeData = await analyzeResponse.json();

    if (!analyzeResponse.ok) {
      console.error("[API Route] Lỗi từ /analyze:", analyzeData);
      throw new Error(analyzeData.detail || "Lỗi từ dịch vụ dự đoán AI");
    }
    // Sau khi nhận được analyzeData:
    if (
      !analyzeData.address ||
      !analyzeData.prediction ||
      analyzeData.probability_fraud === undefined
    ) {
      throw new Error("Phản hồi từ /analyze thiếu dữ liệu cần thiết.");
    }

    // 5. Xử lý kết quả từ cuộc gọi /explain
    const explainData = await explainResponse.json();

    if (!explainResponse.ok) {
      console.error("[API Route] Lỗi từ /explain:", explainData);
      throw new Error(explainData.detail || "Lỗi từ dịch vụ giải thích AI");
    }
    if (
      !explainData.lime_explanation ||
      !explainData.shap_values
    ) {
      throw new Error("Phản hồi từ /explain thiếu dữ liệu cần thiết.");
    }

    // 6. Kết hợp dữ liệu từ cả hai cuộc gọi
    const combinedResult: AnalysisApiResponse = {
      address: analyzeData.address,
      prediction: analyzeData.prediction,
      probability_fraud: analyzeData.probability_fraud,
      lime_explanation: explainData.lime_explanation,
      shap_values: explainData.shap_values,
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