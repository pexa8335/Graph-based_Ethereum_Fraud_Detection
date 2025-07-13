import { WalletFeatures } from '@/types/analysis';
export interface AnalysisResult {
    prediction: 'Fraud' | 'Non-Fraud';
    probability_fraud: number;
    features: WalletFeatures; 
    explanation: Array<[string, number]>;
}

export async function fetchAnalysisData(address: string): Promise<AnalysisResult> {
    console.log(`[Service] Bắt đầu phân tích cho: ${address}`);
    const apiUrl = `${process.env.NEXT_PUBLIC_APP_URL}/api/analyze`;

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address }),
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Lỗi từ dịch vụ phân tích.');
        }
        console.log(`[Service] Nhận được kết quả phân tích thành công.`);
        return result as AnalysisResult;

    } catch (error) {
        console.error("[Service] Lỗi nghiêm trọng khi fetch dữ liệu phân tích:", error);
        if (error instanceof Error) {
            throw new Error(error.message);
        }
        throw new Error('Đã có lỗi không xác định xảy ra.');
    }
}