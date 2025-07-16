'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Trash2 } from 'lucide-react';
import { CovalentTransaction } from '@/types/analysis';
import { fetchRecentTransactions } from '@/utils/fetchRecentTransactions';
const TEST_ADDRESS = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045';
export default function HistoryClient() {
  const router = useRouter();
  const [transactions, setTransactions] = useState<CovalentTransaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setIsLoading(true);
      const data : CovalentTransaction[] = await fetchRecentTransactions(TEST_ADDRESS);
      setTransactions(data);
      setIsLoading(false);
    }
    load();
  }, []);

  return (
    <main className="p-4 sm:p-6 lg:p-8 bg-slate-900 text-white min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Lịch sử Giao dịch</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-red-500/10 text-red-400 rounded-lg font-semibold hover:bg-red-500/20 transition-colors">
          <Trash2 size={20} /> Xóa lịch sử
        </button>
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-lg">
        {isLoading ? (
          <p className="p-4 text-slate-400">Đang tải dữ liệu...</p>
        ) : (
          <ul className="divide-y divide-slate-700">
            {transactions.map((tx) => (
              <li
                key={tx.tx_hash}
                onClick={() => router.push(`/transaction/${tx.tx_hash}`)}
                className="p-4 flex justify-between items-center cursor-pointer hover:bg-slate-700/50"
              >
                <div>
                  <p className="font-mono text-cyan-400 truncate w-[300px]">
                    {tx.tx_hash}
                  </p>
                  <p className="text-xs text-slate-400">
                    {new Date(tx.block_signed_at).toLocaleString()}
                  </p>
                  <p className="text-xs text-slate-500">
                    Từ: {tx.from_address.slice(0, 6)}... → Đến: {tx.to_address?.slice(0, 6) || '0x...'}
                  </p>
                </div>
                <span className="text-sm text-slate-400">Xem chi tiết →</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
}
