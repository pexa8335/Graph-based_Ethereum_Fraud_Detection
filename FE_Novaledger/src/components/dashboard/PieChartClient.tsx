'use client';

const MOCK_PIE_DATA = [
  { name: 'An toàn', value: 75, color: 'bg-green-500' },
  { name: 'Cần xem xét', value: 17, color: 'bg-yellow-500' },
  { name: 'Rủi ro cao', value: 8, color: 'bg-red-500' },
];

export default function PieChartClient() {
  // Tạo giá trị cho conic-gradient
  const gradientString = `conic-gradient(#16a34a 0% 75%, #f59e0b 75% 92%, #ef4444 92% 100%)`;
  
  return (
    <div className="h-full w-full flex flex-col lg:flex-row items-center justify-around gap-6">
      {/* Phần biểu đồ tròn */}
      <div className="relative">
        <div 
          className="h-40 w-40 rounded-full"
          style={{ backgroundImage: gradientString }}
        >
        </div>
        {/* Lỗ ở giữa để tạo thành Donut Chart */}
        <div className="absolute inset-4 rounded-full bg-slate-800 flex items-center justify-center flex-col">
           <span className="text-3xl font-bold">1482</span>
           <span className="text-xs text-slate-400">Giao dịch</span>
        </div>
      </div>
      
      {/* Phần chú thích (Legend) */}
      <div className="flex flex-col gap-3">
        {MOCK_PIE_DATA.map(item => (
          <div key={item.name} className="flex items-center gap-3 text-sm">
            <div className={`h-3 w-3 rounded-sm ${item.color}`}></div>
            <div className="flex justify-between w-full gap-4">
              <span className="text-slate-300">{item.name}</span>
              <span className="font-semibold text-slate-200">{item.value}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}