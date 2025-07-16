import { WalletFeatures } from '@/types/analysis';
export interface PredictionResult {
  prediction: number; 
  confidence: number; 
}

/**
 * [MOCK] Hàm giả lập việc gọi API dự đoán.
 * Hàm này không thực hiện cuộc gọi mạng thực sự.
 * Thay vào đó, nó đợi 1 giây rồi trả về một kết quả ngẫu nhiên.
 * @param features - Các đặc điểm của ví (không được sử dụng trong bản mock này, nhưng vẫn giữ để đúng API).
 * @returns Một đối tượng PredictionResult giả.
 */
export async function getPrediction(features: WalletFeatures): Promise<PredictionResult> {
  console.log("⚠️  Sử dụng Prediction Service giả (mock). Đang mô phỏng cuộc gọi API...");

  await new Promise(resolve => setTimeout(resolve, 1000));
  const mockPrediction = Math.random() > 0.5 ? 1 : 0;
  const mockConfidence = Math.random() * (0.98 - 0.70) + 0.70;

  const mockResult: PredictionResult = {
    prediction: mockPrediction,
    confidence: mockConfidence,
  };

  console.log("✅  Đã tạo kết quả dự đoán giả:", mockResult);
  return mockResult;
}