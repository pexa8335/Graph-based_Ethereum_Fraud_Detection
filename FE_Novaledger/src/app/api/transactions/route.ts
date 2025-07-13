import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const COVALENT_API_KEY = process.env.COVALENT_API_KEY!;
const CHAIN_NAME = 'eth-mainnet';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const address = searchParams.get('address');
  const page = searchParams.get('page') || '0';

  if (!address) {
    return NextResponse.json({ error: 'Missing address parameter' }, { status: 400 });
  }

  const url = `https://api.covalenthq.com/v1/${CHAIN_NAME}/address/${address}/transactions_v3/?page-number=${page}&page-size=5`;

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${COVALENT_API_KEY}`
      }
    });

    return NextResponse.json(response.data?.data?.items ?? []);
  } catch (error: any) {
    console.error('Covalent API error:', error.response?.data || error.message);
    return NextResponse.json({ error: 'Failed to fetch transactions' }, { status: 500 });
  }
}
