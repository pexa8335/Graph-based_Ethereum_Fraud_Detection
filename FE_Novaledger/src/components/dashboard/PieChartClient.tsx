'use client';

const MOCK_PIE_DATA = [
  { name: 'Safe', value: 75, color: 'bg-green-500' },
  { name: 'Review Needed', value: 17, color: 'bg-yellow-500' },
  { name: 'High Risk', value: 8, color: 'bg-red-500' },
];

export default function PieChartClient() {
  const gradientString = `conic-gradient(#16a34a 0% 75%, #f59e0b 75% 92%, #ef4444 92% 100%)`;
  
  return (
    <div className="h-full w-full flex flex-col lg:flex-row items-center justify-around gap-6">
      {/* Donut chart section */}
      <div className="relative">
        <div 
          className="h-40 w-40 rounded-full"
          style={{ backgroundImage: gradientString }}
        />
        
        {/* Center hole for donut effect */}
        <div className="absolute inset-4 rounded-full bg-slate-800 flex items-center justify-center flex-col">
           <span className="text-3xl font-bold">1482</span>
           <span className="text-xs text-slate-400">Transactions</span>
        </div>
      </div>
      
      {/* Legend section */}
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
