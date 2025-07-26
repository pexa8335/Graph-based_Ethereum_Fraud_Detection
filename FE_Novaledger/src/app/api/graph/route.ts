import { NextResponse } from "next/server";
const GRAPHAPI_URL = process.env.GRAPHAPI_URL;
export async function POST(request : Request){
    try {
        if(!GRAPHAPI_URL){
            throw new Error("URL của API phân tích chưa được cấu hình trên server.");
        }
        const { address} = await request.json();
        if(!address){
            return NextResponse.json({ error: 'Địa chỉ ví là bắt buộc' }, { status: 400 });
        }
        console.log(`[API Route] Yêu cầu HTML graph cho ví: ${address} từ FastAPI...`);
        const response = await fetch(`${GRAPHAPI_URL}/graph`, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: address }), 
        });
        const htmlContent = await response.text();
        if (!response.ok) {
            console.error("[API Route] Lỗi từ /graph:", htmlContent);
            throw new Error(htmlContent || 'Lỗi từ dịch vụ tạo sơ đồ.');
        }
        return new NextResponse(htmlContent, {
            headers: { 'Content-Type': 'text/html' },
            status: 200,
        });
    } catch (error : any) {
        console.error('[API Route] Lỗi tổng quát khi lấy graph:', error);
        const errorMessage = error instanceof Error ? error.message : 'Đã có lỗi không xác định xảy ra';
        return NextResponse.json({ error: errorMessage }, { status: 500 });
    }
}