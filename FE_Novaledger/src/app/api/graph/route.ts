import { NextRequest, NextResponse } from 'next/server';

const GRAPHAPI_URL = process.env.GRAPHAPI_URL;

export async function POST(request: NextRequest) {
  try {
    if (!GRAPHAPI_URL) throw new Error("GRAPHAPI_URL chưa được cấu hình");

    const { address } = await request.json();
    if (!address) return NextResponse.json({ error: 'Địa chỉ ví là bắt buộc' }, { status: 400 });

    console.log(`[API Route] Gửi địa chỉ đến FastAPI: ${address}`);

    const response = await fetch(`${GRAPHAPI_URL}/graph`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error('[API Route] Lỗi từ FastAPI:', errText);
      return NextResponse.json({ error: errText || 'Lỗi không xác định' }, { status: 500 });
    }

    const buffer = await response.arrayBuffer(); 
    return new NextResponse(Buffer.from(buffer), {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="analysis_results.zip"`,
      },
    });
  } catch (error: any) {
    console.error('[API Route] Lỗi tổng quát:', error);
    return NextResponse.json({ error: error.message || 'Lỗi không xác định' }, { status: 500 });
  }
}
