import { NextResponse } from 'next/server';
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

    console.log(`Chuyển tiếp yêu cầu phân tích cho ví: ${address} đến API FastAPI...`);
    const response = await fetch(`${FASTAPI_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ address: address }), 
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Lỗi từ dịch vụ phân tích AI');
    }
    return NextResponse.json(data);

  } catch (error) {
    console.error('Lỗi trong API Route /api/analyze:', error);
    const errorMessage = error instanceof Error ? error.message : 'Đã có lỗi không xác định xảy ra';
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}