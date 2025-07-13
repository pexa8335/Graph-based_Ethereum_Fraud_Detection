import { AnalysisApiResponse } from '@/types/analysis';
export interface AnalysisServiceResponse extends AnalysisApiResponse {
}
export async function fetchAnalysisData(address: string): Promise<AnalysisServiceResponse> {
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
        return result as AnalysisServiceResponse;

    } catch (error) {
        if (error instanceof Error) {
            throw new Error(error.message);
        }
        throw new Error('Đã có lỗi không xác định xảy ra.');
    }
}