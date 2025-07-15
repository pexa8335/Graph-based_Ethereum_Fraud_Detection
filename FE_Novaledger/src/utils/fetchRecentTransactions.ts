import { CovalentTransaction } from "@/types/analysis";
export async function fetchRecentTransactions(address: string): Promise<CovalentTransaction[]> {
  try {
    const res = await fetch(`/api/transactions?address=${address}&page=0`);
    if (!res.ok) throw new Error('Lỗi khi gọi API lịch sử giao dịch');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('fetchRecentTransactions error:', err);
    return [];
  }
}
