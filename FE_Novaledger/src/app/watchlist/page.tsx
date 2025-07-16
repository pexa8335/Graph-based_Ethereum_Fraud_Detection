'use client';
import { useRouter } from 'next/navigation';
import { Star, AlertTriangle, ShieldCheck, PlusCircle } from 'lucide-react';
const MOCK_WATCHLIST = [
  { address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045', name: 'Vitalik Buterin', riskScore: 15, status: 'Safe' },
  { address: '0x1a2b3c...d4e5', name: 'Ví Rủi ro cao', riskScore: 98, status: 'High' },
  { address: '0xFEb4...c3dF', name: 'Ví Cá voi', riskScore: 45, status: 'Medium' },
];

export default function WatchlistClient() {
  const router = useRouter();
  const watchlist = MOCK_WATCHLIST;

  const getStatusColor = (status: string) => {
    if (status === 'High') return 'text-red-400';
    if (status === 'Medium') return 'text-yellow-400';
    return 'text-green-400';
  };

  return (
    <main className="p-4 sm:p-6 lg:p-8 bg-slate-900 text-white min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Danh sách Theo dõi</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-cyan-500 text-black rounded-lg font-semibold hover:bg-cyan-400 transition-colors">
          <PlusCircle size={20} /> Thêm mới
        </button>
      </div>

      {watchlist.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {watchlist.map(item => (
            <div 
              key={item.address} 
              onClick={() => router.push(`/analysis/${item.address}`)}
              className="bg-slate-800 border border-slate-700 rounded-lg p-6 cursor-pointer hover:border-cyan-400 transition-all"
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-lg font-semibold">{item.name}</p>
                  <p className="text-sm text-slate-400 font-mono">{item.address.slice(0, 6)}...{item.address.slice(-4)}</p>
                </div>
                <Star className="text-yellow-500" />
              </div>
              <div className="mt-4 pt-4 border-t border-slate-700 flex items-center gap-3">
                <p className={`text-3xl font-bold ${getStatusColor(item.status)}`}>{item.riskScore}</p>
                <p className="text-slate-300">Điểm rủi ro</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-slate-800 rounded-lg border border-dashed border-slate-700">
          <Star size={48} className="mx-auto text-slate-500" />
          <h2 className="mt-4 text-xl font-semibold">Watchlist của bạn đang trống</h2>
          <p className="text-slate-400 mt-2">Thêm một địa chỉ để bắt đầu theo dõi rủi ro của họ.</p>
        </div>
      )}
    </main>
  );
}